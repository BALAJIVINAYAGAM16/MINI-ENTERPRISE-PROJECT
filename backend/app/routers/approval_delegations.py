from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User

from app.models.approval_delegation import (
    ApprovalDelegation
)

from app.schemas.approval_delegation import (
    ApprovalDelegationCreate
)

router = APIRouter(
    prefix="/approval-delegations",
    tags=["Approval Delegations"]
)


@router.post("")
def create_delegation(
    payload: ApprovalDelegationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conflict = db.query(ApprovalDelegation).filter(
        ApprovalDelegation.delegator_id == current_user.id,
        ApprovalDelegation.is_active == True,
        ApprovalDelegation.start_date <= payload.end_date,
        ApprovalDelegation.end_date >= payload.start_date
    ).first()
    if conflict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delegation date conflict")

    delegation = ApprovalDelegation(
        delegator_id=current_user.id,
        delegatee_id=payload.delegatee_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason
    )

    db.add(delegation)

    db.commit()

    db.refresh(delegation)

    return delegation


@router.get("/me")
def my_delegations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(
        ApprovalDelegation
    ).filter(
        ApprovalDelegation.delegator_id == current_user.id
    ).all()


@router.get("/active")
def active_delegations(
    db: Session = Depends(get_db)
):

    return db.query(
        ApprovalDelegation
    ).filter(
        ApprovalDelegation.is_active == True
    ).all()


@router.put("/{id}/cancel")
def cancel_delegation(
    id: int,
    db: Session = Depends(get_db)
):

    delegation = db.query(
        ApprovalDelegation
    ).filter(
        ApprovalDelegation.id == id
    ).first()

    if not delegation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delegation not found")

    delegation.is_active = False

    db.commit()

    return {
        "message": "Delegation Cancelled"
    }
