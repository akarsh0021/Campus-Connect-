"""Student router — profile management, resume upload."""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, StudentProfile
from schemas.user import StudentProfileUpdate
from services.auth_service import get_current_user
from ai.resume_parser import parse_resume
from config import UPLOAD_DIR

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.put("/profile")
def update_profile(
    data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update student profile."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can update student profiles")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    # Also update full_name if provided
    if data.bio is not None:
        pass  # bio is on profile

    db.commit()
    db.refresh(profile)

    return {"message": "Profile updated", "profile": {
        "id": profile.id,
        "department": profile.department,
        "cgpa": profile.cgpa,
        "graduation_year": profile.graduation_year,
        "skills": profile.skills or [],
        "experience_years": profile.experience_years,
        "bio": profile.bio,
        "phone": profile.phone,
        "linkedin": profile.linkedin,
        "github": profile.github,
        "resume_path": profile.resume_path,
        "parsed_skills": profile.parsed_skills or [],
    }}


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload and parse a resume (PDF or DOCX)."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can upload resumes")

    # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".docx", ".doc"):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are accepted")

    # Save file
    filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Parse resume with AI
    parsed = parse_resume(file_path)

    # Update student profile
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile:
        profile.resume_path = filename
        profile.resume_text = parsed["text"]
        profile.parsed_skills = parsed["skills"]
        # Auto-fill CGPA and experience if detected and not already set
        if parsed["cgpa"] > 0 and profile.cgpa == 0:
            profile.cgpa = parsed["cgpa"]
        if parsed["experience_years"] > 0 and profile.experience_years == 0:
            profile.experience_years = parsed["experience_years"]
        # Merge parsed skills with manually added skills (strip any legacy tags)
        from ai.resume_parser import strip_tag
        existing = {strip_tag(s) for s in (profile.skills or [])}
        existing.update(strip_tag(s) for s in parsed["skills"])
        profile.skills = sorted(s for s in existing if s)
        db.commit()

    return {
        "message": "Resume uploaded and parsed successfully",
        "filename": filename,
        "parsed": parsed,
    }


@router.get("/profile/{user_id}")
def get_student_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a student's profile (for company/admin viewing)."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    user = db.query(User).filter(User.id == user_id).first()

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "full_name": user.full_name if user else "",
        "email": user.email if user else "",
        "department": profile.department,
        "cgpa": profile.cgpa,
        "graduation_year": profile.graduation_year,
        "skills": profile.skills or [],
        "experience_years": profile.experience_years,
        "bio": profile.bio,
        "phone": profile.phone,
        "linkedin": profile.linkedin,
        "github": profile.github,
        "parsed_skills": profile.parsed_skills or [],
    }
