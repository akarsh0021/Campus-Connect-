"""Admin router — user management, analytics, placement oversight."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.user import User, StudentProfile, CompanyProfile
from models.job import Job
from models.application import Application
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/analytics")
def get_analytics(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get platform-wide analytics."""
    total_students = db.query(func.count(User.id)).filter(User.role == "student").scalar()
    total_companies = db.query(func.count(User.id)).filter(User.role == "company").scalar()
    total_jobs = db.query(func.count(Job.id)).scalar()
    total_applications = db.query(func.count(Application.id)).scalar()
    total_shortlisted = db.query(func.count(Application.id)).filter(Application.status == "shortlisted").scalar()
    total_selected = db.query(func.count(Application.id)).filter(Application.status == "selected").scalar()
    total_rejected = db.query(func.count(Application.id)).filter(Application.status == "rejected").scalar()

    # Department-wise student count
    dept_stats = (
        db.query(StudentProfile.department, func.count(StudentProfile.id))
        .group_by(StudentProfile.department)
        .all()
    )
    departments = {dept: count for dept, count in dept_stats if dept}

    # Application status distribution
    status_dist = (
        db.query(Application.status, func.count(Application.id))
        .group_by(Application.status)
        .all()
    )
    status_distribution = {status: count for status, count in status_dist}

    # Top skills (from student profiles)
    all_students = db.query(StudentProfile).all()
    skill_counts = {}
    for s in all_students:
        for skill in (s.skills or []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15]

    # Average AI score
    avg_score = db.query(func.avg(Application.ai_score)).scalar() or 0

    return {
        "overview": {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "total_shortlisted": total_shortlisted,
            "total_selected": total_selected,
            "total_rejected": total_rejected,
            "placement_rate": round((total_selected / max(total_students, 1)) * 100, 1),
            "avg_ai_score": round(avg_score, 1),
        },
        "departments": departments,
        "status_distribution": status_distribution,
        "top_skills": [{"skill": s, "count": c} for s, c in top_skills],
    }


@router.get("/users")
def list_users(
    role: str = Query("", description="Filter by role"),
    search: str = Query("", description="Search by name/email"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all users with optional filters."""
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )

    users = query.order_by(User.created_at.desc()).all()

    result = []
    for user in users:
        item = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": str(user.created_at) if user.created_at else None,
        }
        if user.role == "student":
            profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
            if profile:
                item["department"] = profile.department
                item["cgpa"] = profile.cgpa
                item["skills_count"] = len(profile.skills or [])
        elif user.role == "company":
            profile = db.query(CompanyProfile).filter(CompanyProfile.user_id == user.id).first()
            if profile:
                item["company_name"] = profile.company_name
                item["industry"] = profile.industry
        result.append(item)

    return result


@router.patch("/users/{user_id}/toggle")
def toggle_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Activate/deactivate a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot toggle admin users")

    user.is_active = 0 if user.is_active else 1
    db.commit()

    return {"message": f"User {'activated' if user.is_active else 'deactivated'}", "is_active": user.is_active}


@router.get("/placements")
def list_placements(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all placement (selected) records."""
    placements = (
        db.query(Application)
        .filter(Application.status == "selected")
        .order_by(Application.applied_at.desc())
        .all()
    )

    result = []
    for app in placements:
        student = db.query(StudentProfile).filter(StudentProfile.id == app.student_id).first()
        user = db.query(User).filter(User.id == student.user_id).first() if student else None
        job = db.query(Job).filter(Job.id == app.job_id).first()
        company = db.query(CompanyProfile).filter(CompanyProfile.id == job.company_id).first() if job else None

        result.append({
            "id": app.id,
            "student_name": user.full_name if user else "",
            "student_email": user.email if user else "",
            "department": student.department if student else "",
            "company_name": company.company_name if company else "",
            "job_title": job.title if job else "",
            "ai_score": app.ai_score,
            "applied_at": str(app.applied_at) if app.applied_at else None,
        })

    return result
