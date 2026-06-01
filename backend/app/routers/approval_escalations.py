from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db

from app.models.approval import Approval
from app.models.approval_escalation import ApprovalEscalation

from app.schemas.approval_escalation import (
    ApprovalEscalationCreate
)

router = APIRouter(
    prefix="/approval-escalations",
    tags=["Approval Escalations"]
)


@router.post("")
def create_escalation(
    payload: ApprovalEscalationCreate,
    db: Session = Depends(get_db)
):
    approval = db.query(Approval).filter(Approval.id == payload.approval_id).first()
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")

    escalation = ApprovalEscalation(
        approval_id=payload.approval_id,
        escalated_to=payload.escalated_to,
        escalated_from=approval.current_escalation_to or approval.requested_by,
        reason=payload.reason
    )

    db.add(escalation)
    approval.is_escalated = True
    approval.current_escalation_to = payload.escalated_to

    db.commit()

    db.refresh(escalation)

    return escalation


@router.get("")
def list_escalations(
    db: Session = Depends(get_db)
):

    return db.query(
        ApprovalEscalation
    ).all()


@router.get("/approval/{approval_id}")
def escalation_history(
    approval_id: int,
    db: Session = Depends(get_db)
):
    return db.query(
        ApprovalEscalation
    ).filter(
        ApprovalEscalation.approval_id == approval_id
    ).all()


@router.get("/pending")
def pending_escalations(
    db: Session = Depends(get_db)
):

    return db.query(
        ApprovalEscalation
    ).filter(
        ApprovalEscalation.status == "PENDING"
    ).all()


@router.put("/{id}/resolve")
def resolve_escalation(
    id: int,
    db: Session = Depends(get_db)
):

    escalation = db.query(
        ApprovalEscalation
    ).filter(
        ApprovalEscalation.id == id
    ).first()

    if not escalation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escalation not found")

    if escalation.status == "RESOLVED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Escalation already resolved")

    escalation.status = "RESOLVED"

    escalation.resolved_at = datetime.utcnow()

    approval = db.query(Approval).filter(Approval.id == escalation.approval_id).first()
    if approval:
        pending = db.query(ApprovalEscalation).filter(
            ApprovalEscalation.approval_id == approval.id,
            ApprovalEscalation.status == "PENDING",
            ApprovalEscalation.id != escalation.id
        ).first()
        if not pending:
            approval.is_escalated = False
            approval.current_escalation_to = None

    db.commit()

    return escalation


@router.put("/{id}/cancel")
def cancel_escalation(
    id: int,
    db: Session = Depends(get_db)
):
    escalation = db.query(
        ApprovalEscalation
    ).filter(
        ApprovalEscalation.id == id
    ).first()

    if not escalation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escalation not found")

    if escalation.status == "RESOLVED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Escalation already resolved")

    escalation.status = "CANCELLED"
    escalation.resolved_at = datetime.utcnow()

    approval = db.query(Approval).filter(Approval.id == escalation.approval_id).first()
    if approval:
        approval.is_escalated = False
        approval.current_escalation_to = None

    db.commit()

    return escalation
