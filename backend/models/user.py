"""User, StudentProfile, and CompanyProfile models."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class User(Base):
    """Base user model with role-based access."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # student, company, admin
    full_name = Column(String(255), nullable=False)
    avatar_url = Column(String(500), default="")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    company_profile = relationship("CompanyProfile", back_populates="user", uselist=False)
    notifications = relationship("Notification", back_populates="user")


class StudentProfile(Base):
    """Extended profile for student users."""
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department = Column(String(100), default="")
    cgpa = Column(Float, default=0.0)
    graduation_year = Column(Integer, default=2026)
    skills = Column(JSON, default=list)  # ["Python", "React", ...]
    experience_years = Column(Float, default=0.0)
    resume_path = Column(String(500), default="")
    resume_text = Column(Text, default="")  # Extracted text from resume
    parsed_skills = Column(JSON, default=list)  # AI-extracted skills
    bio = Column(Text, default="")
    phone = Column(String(20), default="")
    linkedin = Column(String(255), default="")
    github = Column(String(255), default="")

    # Relationships
    user = relationship("User", back_populates="student_profile")
    applications = relationship("Application", back_populates="student")


class CompanyProfile(Base):
    """Extended profile for company users."""
    __tablename__ = "company_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    company_name = Column(String(255), default="")
    industry = Column(String(100), default="")
    website = Column(String(255), default="")
    description = Column(Text, default="")
    location = Column(String(255), default="")
    employee_count = Column(String(50), default="")
    logo_url = Column(String(500), default="")

    # Relationships
    user = relationship("User", back_populates="company_profile")
    jobs = relationship("Job", back_populates="company")
