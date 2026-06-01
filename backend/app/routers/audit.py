# routers/audit_router.py

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.audit_log import AuditLog
from app.services.audit_service import get_audit_logs

router = APIRouter(prefix="/audit-logs", tags=["Audit"])


@router.get("")
def get_logs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_audit_logs(db, user)


@router.get("/date-range")
def get_logs_by_date_range(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(AuditLog).filter(
        AuditLog.created_at >= start_date,
        AuditLog.created_at <= end_date,
    )
    if getattr(user, "role", None) != "admin" and getattr(user, "role", None) != "auditor":
        query = query.filter(AuditLog.user_id == user.id)
    return query.order_by(AuditLog.created_at.desc()).all()


@router.get("/module/{module_name}")
def get_logs_by_module(
    module_name: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(AuditLog).filter(AuditLog.module_name == module_name)
    if getattr(user, "role", None) != "admin" and getattr(user, "role", None) != "auditor":
        query = query.filter(AuditLog.user_id == user.id)
    return query.order_by(AuditLog.created_at.desc()).all()


@router.get("/user/{user_id}")
def get_logs_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if getattr(user, "role", None) not in {"admin", "auditor"} and user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return db.query(AuditLog).filter(
        AuditLog.user_id == user_id
    ).order_by(AuditLog.created_at.desc()).all()


@router.get("/{id}")
def get_log(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(AuditLog).filter(AuditLog.id == id)
    if getattr(user, "role", None) not in {"admin", "auditor"}:
        query = query.filter(AuditLog.user_id == user.id)
    log = query.first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit log not found")
    return log
