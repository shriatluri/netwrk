from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    resumes = relationship("Resume", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Basic Information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    headline = Column(String)
    summary = Column(Text)

    # Contact Information
    phone = Column(String)
    location = Column(String)

    # Professional Information
    current_position = Column(String)
    current_company = Column(String)
    industry = Column(String)
    years_of_experience = Column(Integer)

    # Education
    education_level = Column(String)  # e.g., "Bachelor's", "Master's", "PhD"
    university = Column(String)
    graduation_year = Column(Integer)
    major = Column(String)
    grade = Column(String)  # GPA or grade

    # LinkedIn
    linkedin_url = Column(String)
    linkedin_profile_id = Column(String)
    linkedin_profile_data = Column(JSON)  # Store raw LinkedIn data

    # Skills & Interests
    skills = Column(JSON)  # Array of skills
    interests = Column(JSON)  # Array of interests

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # File Information
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    file_size = Column(Integer)
    file_type = Column(String)  # PDF, DOCX, etc.

    # Parsed Content
    raw_text = Column(Text)
    parsed_data = Column(JSON)  # Structured data extracted from resume

    # Extracted Information
    extracted_name = Column(String)
    extracted_email = Column(String)
    extracted_phone = Column(String)
    extracted_skills = Column(JSON)
    extracted_education = Column(JSON)
    extracted_experience = Column(JSON)

    # Status
    is_primary = Column(Boolean, default=True)
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resumes")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String, nullable=False, index=True)
    linkedin_company_id = Column(String, unique=True, index=True)
    industry = Column(String)
    company_size = Column(String)
    headquarters = Column(String)

    # Details
    description = Column(Text)
    website = Column(String)
    specialties = Column(JSON)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employees = relationship("CompanyEmployee", back_populates="company")


class CompanyEmployee(Base):
    __tablename__ = "company_employees"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))

    # Employee Information
    linkedin_profile_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    headline = Column(String)
    position = Column(String)
    department = Column(String)

    # Profile Details
    profile_url = Column(String)
    profile_data = Column(JSON)
    skills = Column(JSON)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="employees")
    recommendations = relationship("ConnectionRecommendation", back_populates="employee")


class ConnectionRecommendation(Base):
    __tablename__ = "connection_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(Integer, ForeignKey("company_employees.id"))

    # Scoring
    total_score = Column(Float, nullable=False)
    industry_score = Column(Float)
    skill_score = Column(Float)
    experience_score = Column(Float)
    geographic_score = Column(Float)
    mutual_connections_score = Column(Float)

    # Status
    status = Column(String, default="pending")  # pending, accepted, rejected, sent

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("CompanyEmployee", back_populates="recommendations")
