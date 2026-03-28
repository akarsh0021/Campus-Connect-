"""Notification service — create and manage notifications."""
from sqlalchemy.orm import Session
from models.notification import Notification


def create_notification(db: Session, user_id: int, message: str,
                        notif_type: str = "info", link: str = ""):
    """Create a notification for a user."""
    notif = Notification(
        user_id=user_id,
        message=message,
        type=notif_type,
        link=link,
    )
    db.add(notif)
    db.commit()
    return notif


def get_user_notifications(db: Session, user_id: int, limit: int = 20):
    """Get recent notifications for a user."""
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .all()
    )


def mark_as_read(db: Session, notification_id: int, user_id: int):
    """Mark a notification as read."""
    notif = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if notif:
        notif.is_read = 1
        db.commit()
    return notif


def mark_all_as_read(db: Session, user_id: int):
    """Mark all notifications as read for a user."""
    db.query(Notification).filter(
        Notification.user_id == user_id, Notification.is_read == 0
    ).update({"is_read": 1})
    db.commit()
