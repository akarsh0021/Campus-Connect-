"""Company router — profile management."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, CompanyProfile
from schemas.user import CompanyProfileUpdate
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/companies", tags=["Companies"])


@router.put("/profile")
def update_company_profile(
    data: CompanyProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update company profile."""
    if current_user.role != "company":
        raise HTTPException(status_code=403, detail="Only companies can update company profiles")

    profile = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return {"message": "Profile updated", "profile": {
        "id": profile.id,
        "company_name": profile.company_name,
        "industry": profile.industry,
        "website": profile.website,
        "description": profile.description,
        "location": profile.location,
        "employee_count": profile.employee_count,
    }}


@router.get("/profile")
def get_my_company_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current company's profile."""
    if current_user.role != "company":
        raise HTTPException(status_code=403, detail="Not a company user")

    profile = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "company_name": profile.company_name,
        "industry": profile.industry,
        "website": profile.website,
        "description": profile.description,
        "location": profile.location,
        "employee_count": profile.employee_count,
    }
