from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import get_db

from app.models.approval import Approval
from app.models.sla_rule import SLARule
from app.models.sla_tracking import SLATracking
from app.models.task import Task

router = APIRouter(
    prefix="/sla-tracking",
    tags=["SLA Tracking"]
)


@router.get("/active")
def active_tracking(
    db: Session = Depends(get_db)
):

    return db.query(SLATracking).filter(
        SLATracking.status == "ACTIVE"
    ).all()


@router.get("/breached")
def breached_tracking(
    db: Session = Depends(get_db)
):

    return db.query(SLATracking).filter(
        SLATracking.status == "BREACHED"
    ).all()


@router.get("/module/{module_name}")
def tracking_by_module(
    module_name: str,
    db: Session = Depends(get_db)
):
    return db.query(SLATracking).filter(
        SLATracking.module_name == module_name.upper()
    ).all()


@router.get("/record/{module_name}/{record_id}")
def tracking_by_record(
    module_name: str,
    record_id: int,
    db: Session = Depends(get_db)
):
    return db.query(SLATracking).filter(
        SLATracking.module_name == module_name.upper(),
        SLATracking.record_id == record_id
    ).all()


def _find_rule(db: Session, module_name: str, priority: str):
    return db.query(SLARule).filter(
        SLARule.module_name == module_name,
        SLARule.priority == priority,
        SLARule.is_active == True
    ).first()


def _start_tracking(db: Session, module_name: str, record_id: int, priority: str):
    existing = db.query(SLATracking).filter(
        SLATracking.module_name == module_name,
        SLATracking.record_id == record_id,
        SLATracking.status == "ACTIVE"
    ).first()
    if existing:
        return existing

    rule = _find_rule(db, module_name, priority)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Active SLA rule not found for {module_name} / {priority}",
        )

    start_time = datetime.utcnow()
    tracking = SLATracking(
        module_name=module_name,
        record_id=record_id,
        sla_rule_id=rule.id,
        start_time=start_time,
        due_time=start_time + timedelta(hours=rule.allowed_hours),
        status="ACTIVE",
    )
    db.add(tracking)
    return tracking


@router.post("/tasks/{task_id}")
def start_task_tracking(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    tracking = _start_tracking(db, "TASK", task.id, task.priority)
    task.sla_status = tracking.status
    task.sla_due_time = tracking.due_time
    task.is_sla_breached = False
    db.commit()
    db.refresh(tracking)
    return tracking


@router.post("/approvals/{approval_id}")
def start_approval_tracking(
    approval_id: int,
    db: Session = Depends(get_db)
):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")

    tracking = _start_tracking(db, "APPROVAL", approval.id, "medium")
    approval.sla_status = tracking.status
    approval.sla_due_time = tracking.due_time
    db.commit()
    db.refresh(tracking)
    return tracking


@router.put("/{id}/complete")
def complete_tracking(
    id: int,
    db: Session = Depends(get_db)
):

    tracking = db.query(SLATracking).filter(
        SLATracking.id == id
    ).first()

    if not tracking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SLA tracking record not found")

    if tracking.status == "COMPLETED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SLA already completed")

    tracking.status = "COMPLETED"

    tracking.completed_time = datetime.utcnow()

    db.commit()

    return tracking
