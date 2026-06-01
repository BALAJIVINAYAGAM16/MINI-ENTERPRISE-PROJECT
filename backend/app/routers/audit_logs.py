from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get("")
def list_logs(
    db: Session = Depends(get_db)
):

    return db.query(AuditLog).all()


@router.get("/{id}")
def get_log(
    id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        AuditLog
    ).filter(
        AuditLog.id == id
    ).first()


@router.get("/module/{module_name}")
def logs_by_module(
    module_name: str,
    db: Session = Depends(get_db)
):

    return db.query(
        AuditLog
    ).filter(
        AuditLog.module_name == module_name
    ).all()


@router.get("/user/{user_id}")
def logs_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        AuditLog
    ).filter(
        AuditLog.user_id == user_id
    ).all()