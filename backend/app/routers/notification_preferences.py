from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User

from app.models.notification_preference import (
    NotificationPreference
)

from app.schemas.notification_preference import (
    NotificationPreferenceUpdate
)

router = APIRouter(
    prefix="/notification-preferences",
    tags=["Notification Preferences"]
)


@router.get("/me")
def get_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    preference = db.query(
        NotificationPreference
    ).filter(
        NotificationPreference.user_id == current_user.id
    ).first()

    if not preference:
        preference = NotificationPreference(user_id=current_user.id)
        db.add(preference)
        db.commit()
        db.refresh(preference)

    return preference


@router.put("/me")
def update_preferences(
    payload: NotificationPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    preference = db.query(
        NotificationPreference
    ).filter(
        NotificationPreference.user_id == current_user.id
    ).first()

    if not preference:
        preference = NotificationPreference(user_id=current_user.id)
        db.add(preference)

    for key, value in payload.model_dump().items():
        setattr(preference, key, value)

    db.commit()
    db.refresh(preference)

    return preference


@router.post("/default/{user_id}")
def create_default_preferences(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    preference = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == user_id
    ).first()
    if preference:
        return preference

    preference = NotificationPreference(user_id=user_id)
    db.add(preference)
    db.commit()
    db.refresh(preference)
    return preference
