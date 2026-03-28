"""Job-related Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = ""
    required_skills: Optional[List[str]] = []
    min_cgpa: Optional[float] = 0.0
    experience_required: Optional[float] = 0.0
    job_type: Optional[str] = "Full-time"
    location: Optional[str] = ""
    salary_min: Optional[int] = 0
    salary_max: Optional[int] = 0
    deadline: Optional[str] = None
    status: Optional[str] = "active"


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    required_skills: Optional[List[str]] = None
    min_cgpa: Optional[float] = None
    experience_required: Optional[float] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    deadline: Optional[str] = None
    status: Optional[str] = None


class JobOut(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    requirements: str
    required_skills: list
    min_cgpa: float
    experience_required: float
    job_type: str
    location: str
    salary_min: int
    salary_max: int
    deadline: Optional[datetime] = None
    status: str
    created_at: Optional[datetime] = None
    company_name: Optional[str] = None
    application_count: Optional[int] = 0

    class Config:
        from_attributes = True
