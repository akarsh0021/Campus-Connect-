"""Application model linking students to jobs."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Application(Base):
    """Student application to a job posting."""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(String(20), default="applied")  # applied, shortlisted, rejected, selected
    ai_score = Column(Float, default=0.0)  # 0-100
    ai_breakdown = Column(JSON, default=dict)  # {"skills": 35, "cgpa": 22, ...}
    cover_letter = Column(String(1000), default="")
    applied_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    student = relationship("StudentProfile", back_populates="applications")
    job = relationship("Job", back_populates="applications")
