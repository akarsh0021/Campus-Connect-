"""User-related Pydantic schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str  # student, company


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# --- User Schemas ---
class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Student Profile Schemas ---
class StudentProfileUpdate(BaseModel):
    department: Optional[str] = None
    cgpa: Optional[float] = None
    graduation_year: Optional[int] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[float] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class StudentProfileOut(BaseModel):
    id: int
    user_id: int
    department: str
    cgpa: float
    graduation_year: int
    skills: list
    experience_years: float
    resume_path: str
    parsed_skills: list
    bio: str
    phone: str
    linkedin: str
    github: str
    user: Optional[UserOut] = None

    class Config:
        from_attributes = True


# --- Company Profile Schemas ---
class CompanyProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    employee_count: Optional[str] = None


class CompanyProfileOut(BaseModel):
    id: int
    user_id: int
    company_name: str
    industry: str
    website: str
    description: str
    location: str
    employee_count: str
    user: Optional[UserOut] = None

    class Config:
        from_attributes = True
