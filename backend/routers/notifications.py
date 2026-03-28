"""Notifications router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from services.auth_service import get_current_user
from services.notification_service import (
    get_user_notifications, mark_as_read, mark_all_as_read
)

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("")
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user's notifications."""
    notifs = get_user_notifications(db, current_user.id)
    return [{
        "id": n.id,
        "message": n.message,
        "type": n.type,
        "is_read": n.is_read,
        "link": n.link,
        "created_at": str(n.created_at) if n.created_at else None,
    } for n in notifs]


@router.patch("/{notif_id}/read")
def mark_notification_read(
    notif_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a notification as read."""
    mark_as_read(db, notif_id, current_user.id)
    return {"message": "Marked as read"}


@router.patch("/read-all")
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark all notifications as read."""
    mark_all_as_read(db, current_user.id)
    return {"message": "All marked as read"}
