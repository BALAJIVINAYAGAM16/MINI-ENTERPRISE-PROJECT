from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums for approval system
class ApprovalStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    ON_HOLD = "ON_HOLD"

class ApprovalTypeEnum(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

class ApprovalLevelEnum(str, Enum):
    LEVEL_1_MANAGER = "LEVEL_1_MANAGER"
    LEVEL_2_ADMIN = "LEVEL_2_ADMIN"

class ApprovalActionEnum(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    ON_HOLD = "ON_HOLD"
    DELEGATED = "DELEGATED"

# Create Approval Request
class ApprovalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    approval_type: ApprovalTypeEnum = ApprovalTypeEnum.EMPLOYEE
    required_approver_role: Optional[str] = None  # "MANAGER" or "ADMIN"

# Take Action on Approval
class ApprovalAction(BaseModel):
    action: ApprovalActionEnum
    comment: Optional[str] = None

# Approval Response - Complete
class ApprovalOut(BaseModel):
    id: int
    tenant_id: int
    title: str
    description: Optional[str] = None
    approval_type: ApprovalTypeEnum
    status: ApprovalStatusEnum
    current_level: ApprovalLevelEnum
    
    # Requester info
    requested_by: int
    requester_name: Optional[str] = None
    requester_email: Optional[str] = None
    
    # Assignment info
    assigned_to: Optional[int] = None
    required_approver_role: Optional[str] = None
    
    # Approval metadata
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    approved_by_name: Optional[str] = None
    
    rejected_by: Optional[int] = None
    rejection_reason: Optional[str] = None
    rejected_at: Optional[datetime] = None
    rejected_by_name: Optional[str] = None
    
    # SLA tracking
    sla_status: Optional[str] = None
    sla_due_time: Optional[datetime] = None
    is_escalated: bool = False
    current_escalation_to: Optional[int] = None
    escalated_at: Optional[datetime] = None
    
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Approval History Response
class ApprovalHistoryOut(BaseModel):
    id: int
    approval_id: int
    action_by: int
    action_by_name: Optional[str] = None
    action: ApprovalActionEnum
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# List view with pagination
class ApprovalListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ApprovalOut]
