"""Applications router — apply to jobs, manage application status."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, StudentProfile, CompanyProfile
from models.job import Job
from models.application import Application
from schemas.application import ApplicationCreate, ApplicationStatusUpdate
from services.auth_service import get_current_user
from services.notification_service import create_notification
from ai.ranking_engine import rank_candidate

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.post("")
def apply_to_job(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Apply to a job as a student."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can apply")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    job = db.query(Job).filter(Job.id == data.job_id, Job.status == "active").first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not active")

    # Check if already applied
    existing = db.query(Application).filter(
        Application.student_id == profile.id,
        Application.job_id == data.job_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")

    # Compute AI score
    result = rank_candidate(
        student_skills=profile.skills or [],
        student_cgpa=profile.cgpa,
        student_experience=profile.experience_years,
        student_department=profile.department,
        job_required_skills=job.required_skills or [],
        job_min_cgpa=job.min_cgpa,
        job_experience_required=job.experience_required,
        job_requirements=job.requirements or "",
    )

    application = Application(
        student_id=profile.id,
        job_id=data.job_id,
        cover_letter=data.cover_letter or "",
        ai_score=result["total_score"],
        ai_breakdown=result["breakdown"],
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    # Notify student
    create_notification(
        db, current_user.id,
        f"You applied to '{job.title}'. AI Match Score: {result['total_score']}%",
        "success", f"/student/applications"
    )

    # Notify company
    company = db.query(CompanyProfile).filter(CompanyProfile.id == job.company_id).first()
    if company:
        create_notification(
            db, company.user_id,
            f"New application for '{job.title}' from {current_user.full_name}",
            "info", f"/company/jobs/{job.id}/candidates"
        )

    return {
        "message": "Application submitted",
        "application_id": application.id,
        "ai_score": result["total_score"],
        "ai_breakdown": result["breakdown"],
    }


@router.get("")
def list_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List applications for the current student."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can view their applications")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        return []

    applications = (
        db.query(Application)
        .filter(Application.student_id == profile.id)
        .order_by(Application.applied_at.desc())
        .all()
    )

    result = []
    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        company = db.query(CompanyProfile).filter(CompanyProfile.id == job.company_id).first() if job else None
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else "",
            "company_name": company.company_name if company else "",
            "status": app.status,
            "ai_score": app.ai_score,
            "ai_breakdown": app.ai_breakdown or {},
            "cover_letter": app.cover_letter,
            "applied_at": str(app.applied_at) if app.applied_at else None,
            "job_type": job.job_type if job else "",
            "location": job.location if job else "",
        })

    return result


@router.patch("/{application_id}/status")
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update application status (company shortlists/rejects/selects)."""
    if current_user.role not in ("company", "admin"):
        raise HTTPException(status_code=403, detail="Only companies can update application status")

    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Verify company owns the job
    if current_user.role == "company":
        job = db.query(Job).filter(Job.id == application.job_id).first()
        company = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
        if not job or job.company_id != company.id:
            raise HTTPException(status_code=403, detail="Not authorized for this application")

    old_status = application.status
    application.status = data.status
    db.commit()

    # Notify student
    student = db.query(StudentProfile).filter(StudentProfile.id == application.student_id).first()
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if student and job:
        status_messages = {
            "shortlisted": f"🎉 You've been shortlisted for '{job.title}'!",
            "rejected": f"Your application for '{job.title}' was not selected.",
            "selected": f"🏆 Congratulations! You've been selected for '{job.title}'!",
        }
        msg = status_messages.get(data.status, f"Application status updated to {data.status}")
        notif_type = "success" if data.status in ("shortlisted", "selected") else "warning"
        create_notification(db, student.user_id, msg, notif_type, "/student/applications")

    return {"message": f"Status updated from '{old_status}' to '{data.status}'"}
