from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# User Profile Schemas
class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str
    headline: Optional[str] = None
    summary: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    current_position: Optional[str] = None
    current_company: Optional[str] = None
    industry: Optional[str] = None
    years_of_experience: Optional[int] = None
    education_level: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    major: Optional[str] = None
    grade: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    current_position: Optional[str] = None
    current_company: Optional[str] = None
    industry: Optional[str] = None
    years_of_experience: Optional[int] = None
    education_level: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    major: Optional[str] = None
    grade: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    headline: Optional[str]
    summary: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    current_position: Optional[str]
    current_company: Optional[str]
    industry: Optional[str]
    years_of_experience: Optional[int]
    education_level: Optional[str]
    university: Optional[str]
    graduation_year: Optional[int]
    major: Optional[str]
    grade: Optional[str]
    linkedin_url: Optional[str]
    linkedin_profile_id: Optional[str]
    skills: Optional[List[str]]
    interests: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Resume Schemas
class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
    s3_key: str
    file_size: int
    file_type: str
    processing_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ParsedResumeData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    education: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    summary: Optional[str] = None


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    s3_key: str
    file_size: int
    file_type: str
    is_primary: bool
    processing_status: str
    extracted_name: Optional[str]
    extracted_email: Optional[str]
    extracted_phone: Optional[str]
    extracted_skills: Optional[List[str]]
    extracted_education: Optional[List[Dict[str, Any]]]
    extracted_experience: Optional[List[Dict[str, Any]]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# LinkedIn Autofill Schemas
class LinkedInProfileRequest(BaseModel):
    linkedin_url: str = Field(..., description="LinkedIn profile URL")


class LinkedInProfileData(BaseModel):
    first_name: str
    last_name: str
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    current_position: Optional[str] = None
    current_company: Optional[str] = None
    industry: Optional[str] = None
    skills: Optional[List[str]] = None
    education: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    linkedin_profile_id: Optional[str] = None
    profile_picture_url: Optional[str] = None


class AutofillProfileRequest(BaseModel):
    linkedin_url: Optional[str] = None
    use_resume: bool = False
    resume_id: Optional[int] = None


class AutofillProfileResponse(BaseModel):
    success: bool
    profile_data: Optional[UserProfileCreate] = None
    linkedin_data: Optional[LinkedInProfileData] = None
    resume_data: Optional[ParsedResumeData] = None
    message: str


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
