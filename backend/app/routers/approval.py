from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.schemas.approval import (
    ApprovalCreate,
    ApprovalAction,
    ApprovalHistoryOut,
    ApprovalOut,
    ApprovalStatusEnum,
    ApprovalActionEnum,
    ApprovalListResponse,
)

from app.services.approval_service import (
    create_approval_service,
    take_action_service,
    get_approvals_service,
    get_history_service,
    get_single_approval_service,
    approve_approval_service,
    reject_approval_service,
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"],
)


@router.post("/", response_model=ApprovalOut, status_code=status.HTTP_201_CREATED)
def create_approval(
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Create a new approval request"""
    return create_approval_service(payload, user, db)


@router.get("/", response_model=ApprovalListResponse)
def get_approvals(
    status: ApprovalStatusEnum = Query(None),
    role: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """List approvals with filtering and pagination
    
    - **status**: Filter by PENDING, APPROVED, REJECTED, ESCALATED, ON_HOLD
    - **role**: Filter by ADMIN, MANAGER, EMPLOYEE
    - **skip**: Pagination offset
    - **limit**: Items per page (max 100)
    """
    return get_approvals_service(user, db, status=status, role=role, skip=skip, limit=limit)


@router.get("/me/pending", response_model=List[ApprovalOut])
def get_pending_approvals_for_me(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Get all pending approvals assigned to current user"""
    return get_approvals_service(user, db, status=ApprovalStatusEnum.PENDING, assigned_to_me=True)


@router.get("/{approval_id}", response_model=ApprovalOut)
def get_approval(
    approval_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Get single approval by ID"""
    return get_single_approval_service(approval_id, user, db)


@router.post("/{approval_id}/approve", response_model=ApprovalOut)
def approve_approval(
    approval_id: int,
    comment: str = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Approve an approval request"""
    return approve_approval_service(approval_id, comment, user, db)


@router.post("/{approval_id}/reject", response_model=ApprovalOut)
def reject_approval(
    approval_id: int,
    reason: str = Query(..., description="Rejection reason is required"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Reject an approval request"""
    return reject_approval_service(approval_id, reason, user, db)


@router.patch("/{approval_id}/action", response_model=ApprovalOut)
def take_action(
    approval_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Take action on approval (approve/reject/escalate/hold)"""
    return take_action_service(approval_id, payload, user, db)


@router.get("/{approval_id}/history", response_model=List[ApprovalHistoryOut])
def get_history(
    approval_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Get approval history/audit trail"""
    return get_history_service(approval_id, user, db)