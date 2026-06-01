from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_role
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserSummary
import logging

logger = logging.getLogger("mini_enterprise")

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserSummary])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_role(["admin"])),
):
    try:
        return db.query(User).order_by(User.name.asc()).all()
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list users")

@router.get("/assignable", response_model=list[UserSummary])
def list_assignable_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_role(["admin", "manager"])),
):
    try:
        return db.query(User).filter(User.is_active.is_(True)).order_by(User.name.asc()).all()
    except Exception as e:
        logger.error(f"Error listing assignable users: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list assignable users")

@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    return user
