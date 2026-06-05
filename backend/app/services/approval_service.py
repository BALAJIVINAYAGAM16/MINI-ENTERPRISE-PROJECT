from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import Optional

from app.models.approval import Approval, ApprovalStatus, ApprovalLevel, ApprovalType
from app.models.approval_history import ApprovalHistory, ApprovalActionType
from app.models.user import User
from app.services.audit_service import log_action


def create_approval_service(data, user, db: Session):
    """Create a new approval request"""
    
    # Check if user's tenant is set
    if not hasattr(user, 'tenant_id') or not user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must belong to a tenant"
        )
    
    # Determine approval type based on user role
    approval_type = data.approval_type if data.approval_type else ApprovalType.EMPLOYEE
    
    # Set required approver role
    required_role = data.required_approver_role
    if not required_role:
        if approval_type == ApprovalType.EMPLOYEE:
            required_role = "MANAGER"
        elif approval_type == ApprovalType.MANAGER:
            required_role = "ADMIN"
        else:
            required_role = "ADMIN"
    
    approval = Approval(
        tenant_id=user.tenant_id,
        title=data.title,
        description=data.description,
        requested_by=user.id,
        approval_type=approval_type,
        status=ApprovalStatus.PENDING,
        current_level=ApprovalLevel.LEVEL_1_MANAGER,
        required_approver_role=required_role,
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    log_action(
        db,
        user.id,
        "create_approval",
        "approval",
        approval.id,
    )

    return approval


def get_single_approval_service(approval_id: int, user, db: Session):
    """Get single approval by ID with authorization"""
    
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found"
        )
    
    # Authorization check
    is_requester = approval.requested_by == user.id
    is_assigned_approver = approval.assigned_to == user.id
    is_admin_or_manager = user.role in ["ADMIN", "MANAGER"]
    
    if not (is_requester or is_assigned_approver or is_admin_or_manager):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this approval"
        )
    
    return approval


def take_action_service(approval_id: int, data, user, db: Session):
    """Take action on approval (approve/reject/escalate/hold)"""
    
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found"
        )
    
    # Validate action
    if data.action not in [ApprovalActionType.APPROVED, ApprovalActionType.REJECTED, 
                           ApprovalActionType.ESCALATED, ApprovalActionType.ON_HOLD]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action. Must be one of: APPROVED, REJECTED, ESCALATED, ON_HOLD"
        )
    
    # Check if approval is already finalized
    if approval.status in [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Approval already finalized"
        )
    
    # Authorization check - user must be assigned approver or have admin role
    if approval.assigned_to != user.id and user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only assigned approver or admin can take action"
        )
    
    # Rejection requires comment
    if data.action == ApprovalActionType.REJECTED and not data.comment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment required for rejection"
        )
    
    # Process action
    if data.action == ApprovalActionType.APPROVED:
        if approval.current_level == ApprovalLevel.LEVEL_1_MANAGER:
            # Move to next level (ADMIN)
            approval.current_level = ApprovalLevel.LEVEL_2_ADMIN
            approval.status = ApprovalStatus.PENDING
            # TODO: Assign to admin automatically or set for manual assignment
        else:
            # Final approval
            approval.status = ApprovalStatus.APPROVED
            approval.approved_by = user.id
            approval.approved_at = datetime.utcnow()
    
    elif data.action == ApprovalActionType.REJECTED:
        approval.status = ApprovalStatus.REJECTED
        approval.rejected_by = user.id
        approval.rejected_at = datetime.utcnow()
        approval.rejection_reason = data.comment
    
    elif data.action == ApprovalActionType.ESCALATED:
        approval.status = ApprovalStatus.ESCALATED
        approval.is_escalated = True
        approval.escalated_at = datetime.utcnow()
    
    elif data.action == ApprovalActionType.ON_HOLD:
        approval.status = ApprovalStatus.ON_HOLD
    
    # Record action in history
    history = ApprovalHistory(
        approval_id=approval.id,
        action_by=user.id,
        action=data.action,
        comment=data.comment,
    )
    
    db.add(history)
    db.commit()
    db.refresh(approval)
    
    log_action(
        db,
        user.id,
        f"approval_{data.action.value.lower()}",
        "approval",
        approval.id,
    )
    
    return approval


def approve_approval_service(approval_id: int, comment: Optional[str], user, db: Session):
    """Approve an approval request"""
    
    action_data = type('obj', (object,), {
        'action': ApprovalActionType.APPROVED,
        'comment': comment
    })()
    
    return take_action_service(approval_id, action_data, user, db)


def reject_approval_service(approval_id: int, reason: str, user, db: Session):
    """Reject an approval request"""
    
    action_data = type('obj', (object,), {
        'action': ApprovalActionType.REJECTED,
        'comment': reason
    })()
    
    return take_action_service(approval_id, action_data, user, db)


def get_approvals_service(user, db: Session, status: Optional[str] = None, role: Optional[str] = None, 
                          skip: int = 0, limit: int = 10, assigned_to_me: bool = False):
    """Get approvals with filtering and pagination
    
    Args:
        user: Current user
        db: Database session
        status: Filter by approval status
        role: Filter by approval type (EMPLOYEE, MANAGER, ADMIN)
        skip: Pagination offset
        limit: Items per page
        assigned_to_me: Only get approvals assigned to current user
    """
    
    query = db.query(Approval).filter(Approval.tenant_id == user.tenant_id)
    
    # Role-based filtering
    if user.role == "EMPLOYEE":
        # Employees see their own requests and assigned approvals
        query = query.filter(
            or_(
                Approval.requested_by == user.id,
                Approval.assigned_to == user.id
            )
        )
    elif user.role == "MANAGER":
        # Managers see assigned approvals and can see all in their tenant
        query = query.filter(
            or_(
                Approval.assigned_to == user.id,
                Approval.current_level == ApprovalLevel.LEVEL_1_MANAGER
            )
        )
    # ADMIN sees everything for the tenant
    
    # Additional filters
    if assigned_to_me:
        query = query.filter(Approval.assigned_to == user.id)
    
    if status:
        try:
            status_enum = ApprovalStatus[status.value] if hasattr(status, 'value') else ApprovalStatus[status]
            query = query.filter(Approval.status == status_enum)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status}"
            )
    
    if role:
        try:
            role_enum = ApprovalType[role]
            query = query.filter(Approval.approval_type == role_enum)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role: {role}"
            )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    items = query.order_by(Approval.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


def get_history_service(approval_id: int, user, db: Session):
    """Get approval history/audit trail"""
    
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found"
        )
    
    # Authorization check
    if (approval.requested_by != user.id and 
        approval.assigned_to != user.id and 
        user.role != "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view approval history"
        )
    
    return (
        db.query(ApprovalHistory)
        .filter(ApprovalHistory.approval_id == approval_id)
        .order_by(ApprovalHistory.created_at.desc())
        .all()
    )