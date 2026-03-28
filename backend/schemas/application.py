"""Application-related Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = ""


class ApplicationStatusUpdate(BaseModel):
    status: str  # shortlisted, rejected, selected


class ApplicationOut(BaseModel):
    id: int
    student_id: int
    job_id: int
    status: str
    ai_score: float
    ai_breakdown: dict
    cover_letter: str
    applied_at: Optional[datetime] = None
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    student_cgpa: Optional[float] = None
    student_skills: Optional[list] = None
    student_department: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True
