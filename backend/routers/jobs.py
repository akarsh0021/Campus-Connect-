"""Jobs router — CRUD for job postings, AI candidate ranking."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from database import get_db
from models.user import User, CompanyProfile, StudentProfile
from models.job import Job
from models.application import Application
from schemas.job import JobCreate, JobUpdate, JobOut
from services.auth_service import get_current_user
from ai.ranking_engine import rank_candidates_for_job
from ai.job_recommender import recommend_jobs

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("")
def list_jobs(
    status: str = Query("active", description="Filter by status"),
    search: str = Query("", description="Search in title/description"),
    db: Session = Depends(get_db),
):
    """List all jobs with optional filters."""
    query = db.query(Job).filter(Job.status == status)

    if search:
        query = query.filter(
            (Job.title.ilike(f"%{search}%")) | (Job.description.ilike(f"%{search}%"))
        )

    jobs = query.order_by(Job.created_at.desc()).all()

    result = []
    for job in jobs:
        company = db.query(CompanyProfile).filter(CompanyProfile.id == job.company_id).first()
        app_count = db.query(func.count(Application.id)).filter(Application.job_id == job.id).scalar()
        result.append({
            "id": job.id,
            "company_id": job.company_id,
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements,
            "required_skills": job.required_skills or [],
            "min_cgpa": job.min_cgpa,
            "experience_required": job.experience_required,
            "job_type": job.job_type,
            "location": job.location,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "deadline": str(job.deadline) if job.deadline else None,
            "status": job.status,
            "created_at": str(job.created_at) if job.created_at else None,
            "company_name": company.company_name if company else "Unknown",
            "application_count": app_count,
        })

    return result


@router.get("/my")
def list_my_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List jobs posted by the current company."""
    if current_user.role != "company":
        raise HTTPException(status_code=403, detail="Only companies can view their jobs")

    company = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")

    jobs = db.query(Job).filter(Job.company_id == company.id).order_by(Job.created_at.desc()).all()

    result = []
    for job in jobs:
        app_count = db.query(func.count(Application.id)).filter(Application.job_id == job.id).scalar()
        result.append({
            "id": job.id,
            "company_id": job.company_id,
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements,
            "required_skills": job.required_skills or [],
            "min_cgpa": job.min_cgpa,
            "experience_required": job.experience_required,
            "job_type": job.job_type,
            "location": job.location,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "deadline": str(job.deadline) if job.deadline else None,
            "status": job.status,
            "created_at": str(job.created_at) if job.created_at else None,
            "company_name": company.company_name,
            "application_count": app_count,
        })

    return result


@router.post("")
def create_job(
    data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new job posting."""
    if current_user.role != "company":
        raise HTTPException(status_code=403, detail="Only companies can post jobs")

    company = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")

    job = Job(
        company_id=company.id,
        title=data.title,
        description=data.description,
        requirements=data.requirements or "",
        required_skills=data.required_skills or [],
        min_cgpa=data.min_cgpa or 0.0,
        experience_required=data.experience_required or 0.0,
        job_type=data.job_type or "Full-time",
        location=data.location or "",
        salary_min=data.salary_min or 0,
        salary_max=data.salary_max or 0,
        deadline=datetime.fromisoformat(data.deadline) if data.deadline else None,
        status=data.status or "active",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return {"message": "Job posted successfully", "job_id": job.id}


@router.put("/{job_id}")
def update_job(
    job_id: int,
    data: JobUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a job posting."""
    if current_user.role != "company":
        raise HTTPException(status_code=403, detail="Only companies can update jobs")

    company = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == company.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    update_data = data.model_dump(exclude_unset=True)
    if "deadline" in update_data and update_data["deadline"]:
        update_data["deadline"] = datetime.fromisoformat(update_data["deadline"])

    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    return {"message": "Job updated"}


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a job posting."""
    company = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == company.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}


@router.get("/recommendations/student")
def get_job_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get AI-recommended jobs for the current student."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can get recommendations")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # Get active jobs
    active_jobs = db.query(Job).filter(Job.status == "active").all()

    # Get IDs of jobs already applied to
    applied_ids = set()
    apps = db.query(Application).filter(Application.student_id == profile.id).all()
    for a in apps:
        applied_ids.add(a.job_id)

    # Build job dicts (exclude already applied)
    job_dicts = []
    for job in active_jobs:
        if job.id in applied_ids:
            continue
        company = db.query(CompanyProfile).filter(CompanyProfile.id == job.company_id).first()
        job_dicts.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills or [],
            "min_cgpa": job.min_cgpa,
            "experience_required": job.experience_required,
            "job_type": job.job_type,
            "location": job.location,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "company_name": company.company_name if company else "Unknown",
            "company_id": job.company_id,
        })

    student_dict = {
        "skills": profile.skills or [],
        "cgpa": profile.cgpa,
        "experience_years": profile.experience_years,
        "department": profile.department,
    }

    recommended = recommend_jobs(student_dict, job_dicts, top_n=10)
    return recommended


@router.get("/{job_id}/candidates")
def get_ranked_candidates(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get AI-ranked candidates for a job. Companies see all applicants ranked."""
    if current_user.role not in ("company", "admin"):
        raise HTTPException(status_code=403, detail="Only companies and admins can view candidates")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get all applications for this job
    applications = db.query(Application).filter(Application.job_id == job_id).all()

    candidates = []
    for app in applications:
        student = db.query(StudentProfile).filter(StudentProfile.id == app.student_id).first()
        if student:
            user = db.query(User).filter(User.id == student.user_id).first()
            candidates.append({
                "application_id": app.id,
                "student_id": student.id,
                "user_id": student.user_id,
                "name": user.full_name if user else "",
                "email": user.email if user else "",
                "skills": student.skills or [],
                "cgpa": student.cgpa,
                "experience_years": student.experience_years,
                "department": student.department,
                "graduation_year": student.graduation_year,
                "status": app.status,
                "applied_at": str(app.applied_at) if app.applied_at else None,
            })

    # Run AI ranking
    job_dict = {
        "required_skills": job.required_skills or [],
        "min_cgpa": job.min_cgpa,
        "experience_required": job.experience_required,
        "requirements": job.requirements or "",
    }

    ranked = rank_candidates_for_job(candidates, job_dict)

    # Update AI scores in applications
    for candidate in ranked:
        app = db.query(Application).filter(Application.id == candidate["application_id"]).first()
        if app:
            app.ai_score = candidate["ai_score"]
            app.ai_breakdown = candidate["ai_breakdown"]
    db.commit()

    return {
        "job": {
            "id": job.id,
            "title": job.title,
            "required_skills": job.required_skills,
        },
        "candidates": ranked,
        "total": len(ranked),
    }
