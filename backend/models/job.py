"""Job posting model."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Job(Base):
    """Job posting created by companies."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company_profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, default="")
    required_skills = Column(JSON, default=list)  # ["Python", "SQL", ...]
    min_cgpa = Column(Float, default=0.0)
    experience_required = Column(Float, default=0.0)  # years
    job_type = Column(String(50), default="Full-time")  # Full-time, Internship, Part-time
    location = Column(String(255), default="")
    salary_min = Column(Integer, default=0)
    salary_max = Column(Integer, default=0)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(20), default="active")  # active, closed, draft
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    company = relationship("CompanyProfile", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
