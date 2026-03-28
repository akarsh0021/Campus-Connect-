"""Authentication router — register, login, profile."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, StudentProfile, CompanyProfile
from schemas.user import UserRegister, UserLogin, TokenResponse, UserOut
from services.auth_service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user (student or company)."""
    # Check if email exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    if data.role not in ("student", "company"):
        raise HTTPException(status_code=400, detail="Role must be 'student' or 'company'")

    # Create user
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        full_name=data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create role-specific profile
    if data.role == "student":
        profile = StudentProfile(user_id=user.id)
        db.add(profile)
    elif data.role == "company":
        profile = CompanyProfile(user_id=user.id, company_name=data.full_name)
        db.add(profile)

    db.commit()

    # Generate token
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        },
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT token."""
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        },
    )


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user profile with role-specific data."""
    result = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": str(current_user.created_at) if current_user.created_at else None,
    }

    if current_user.role == "student":
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if profile:
            result["profile"] = {
                "id": profile.id,
                "department": profile.department,
                "cgpa": profile.cgpa,
                "graduation_year": profile.graduation_year,
                "skills": profile.skills or [],
                "experience_years": profile.experience_years,
                "resume_path": profile.resume_path,
                "parsed_skills": profile.parsed_skills or [],
                "bio": profile.bio,
                "phone": profile.phone,
                "linkedin": profile.linkedin,
                "github": profile.github,
            }
    elif current_user.role == "company":
        profile = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
        if profile:
            result["profile"] = {
                "id": profile.id,
                "company_name": profile.company_name,
                "industry": profile.industry,
                "website": profile.website,
                "description": profile.description,
                "location": profile.location,
                "employee_count": profile.employee_count,
            }

    return result
