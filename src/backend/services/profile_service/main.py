from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
import os
from dotenv import load_dotenv

from ...shared.database import engine, get_db, Base
from ...shared.models import User, UserProfile, Resume
from ...shared.schemas import (
    ResumeUploadResponse,
    ResumeResponse,
    LinkedInProfileRequest,
    LinkedInProfileData,
    AutofillProfileRequest,
    AutofillProfileResponse,
    UserProfileCreate
)
from ..user_service.auth import get_current_user
from .resume_parser import ResumeParser
from .linkedin_scraper import LinkedInScraper
from .s3_client import S3Client

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Profile Service",
    description="Resume upload, parsing, and LinkedIn profile data extraction",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
linkedin_scraper = LinkedInScraper()
s3_client = S3Client()


# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "profile-service"}


# Upload Resume
@app.post("/api/resume/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and parse resume PDF"""
    # Validate file type
    if not file.filename.endswith(('.pdf', '.PDF')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Upload to S3
    s3_key = f"resumes/{current_user.id}/{file.filename}"
    s3_client.upload_file(file_content, s3_key)

    # Create resume record
    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        s3_key=s3_key,
        file_size=file_size,
        file_type="PDF",
        processing_status="processing"
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    # Parse resume asynchronously (in background)
    try:
        parsed_data = resume_parser.parse_pdf(file_content)

        # Update resume with parsed data
        resume.raw_text = parsed_data.get("raw_text")
        resume.parsed_data = parsed_data
        resume.extracted_name = parsed_data.get("name")
        resume.extracted_email = parsed_data.get("email")
        resume.extracted_phone = parsed_data.get("phone")
        resume.extracted_skills = parsed_data.get("skills")
        resume.extracted_education = parsed_data.get("education")
        resume.extracted_experience = parsed_data.get("experience")
        resume.processing_status = "completed"

        db.commit()
        db.refresh(resume)
    except Exception as e:
        resume.processing_status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse resume: {str(e)}"
        )

    return resume


# Get Resume
@app.get("/api/resume/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resume details"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    return resume


# Get All User Resumes
@app.get("/api/resume", response_model=List[ResumeResponse])
async def get_user_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for current user"""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes


# Extract LinkedIn Profile Data
@app.post("/api/linkedin/extract", response_model=LinkedInProfileData)
async def extract_linkedin_profile(
    request: LinkedInProfileRequest,
    current_user: User = Depends(get_current_user)
):
    """Extract data from LinkedIn profile URL"""
    try:
        profile_data = linkedin_scraper.extract_profile(request.linkedin_url)
        return profile_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to extract LinkedIn profile: {str(e)}"
        )


# Autofill Profile from LinkedIn and/or Resume
@app.post("/api/profile/autofill", response_model=AutofillProfileResponse)
async def autofill_profile(
    linkedin_url: Optional[str] = Form(None),
    resume_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Autofill user profile from LinkedIn URL and/or resume data.
    Combines data from both sources if both are provided.
    """
    linkedin_data = None
    resume_data = None
    combined_profile = {}

    # Extract LinkedIn data if URL provided
    if linkedin_url:
        try:
            linkedin_data = linkedin_scraper.extract_profile(linkedin_url)
            combined_profile.update({
                "first_name": linkedin_data.first_name,
                "last_name": linkedin_data.last_name,
                "headline": linkedin_data.headline,
                "summary": linkedin_data.summary,
                "location": linkedin_data.location,
                "current_position": linkedin_data.current_position,
                "current_company": linkedin_data.current_company,
                "industry": linkedin_data.industry,
                "skills": linkedin_data.skills,
                "linkedin_url": linkedin_url,
            })
        except Exception as e:
            return AutofillProfileResponse(
                success=False,
                message=f"Failed to extract LinkedIn data: {str(e)}"
            )

    # Extract resume data if resume_id provided
    if resume_id:
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        ).first()

        if not resume:
            return AutofillProfileResponse(
                success=False,
                message="Resume not found"
            )

        if resume.processing_status != "completed":
            return AutofillProfileResponse(
                success=False,
                message=f"Resume processing status: {resume.processing_status}"
            )

        # Use resume data to fill in missing fields
        if resume.extracted_name and not combined_profile.get("first_name"):
            name_parts = resume.extracted_name.split(" ", 1)
            combined_profile["first_name"] = name_parts[0]
            if len(name_parts) > 1:
                combined_profile["last_name"] = name_parts[1]

        if resume.extracted_email and not combined_profile.get("email"):
            combined_profile["email"] = resume.extracted_email

        if resume.extracted_phone and not combined_profile.get("phone"):
            combined_profile["phone"] = resume.extracted_phone

        if resume.extracted_skills and not combined_profile.get("skills"):
            combined_profile["skills"] = resume.extracted_skills

        # Extract education info
        if resume.extracted_education and len(resume.extracted_education) > 0:
            latest_education = resume.extracted_education[0]
            combined_profile["education_level"] = latest_education.get("degree")
            combined_profile["university"] = latest_education.get("institution")
            combined_profile["graduation_year"] = latest_education.get("year")
            combined_profile["major"] = latest_education.get("field_of_study")

        resume_data = {
            "name": resume.extracted_name,
            "email": resume.extracted_email,
            "phone": resume.extracted_phone,
            "skills": resume.extracted_skills,
            "education": resume.extracted_education,
            "experience": resume.extracted_experience,
        }

    if not linkedin_data and not resume_data:
        return AutofillProfileResponse(
            success=False,
            message="Please provide LinkedIn URL or resume ID"
        )

    # Create profile data schema
    profile_data = UserProfileCreate(**combined_profile)

    return AutofillProfileResponse(
        success=True,
        profile_data=profile_data,
        linkedin_data=linkedin_data,
        resume_data=resume_data,
        message="Profile data extracted successfully"
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PROFILE_SERVICE_PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
