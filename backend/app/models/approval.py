from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    ON_HOLD = "ON_HOLD"

class ApprovalType(str, enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

class ApprovalLevel(str, enum.Enum):
    LEVEL_1_MANAGER = "LEVEL_1_MANAGER"
    LEVEL_2_ADMIN = "LEVEL_2_ADMIN"

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)

    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Approval type and workflow
    approval_type = Column(Enum(ApprovalType), default=ApprovalType.EMPLOYEE, nullable=False, index=True)
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False, index=True)
    current_level = Column(Enum(ApprovalLevel), default=ApprovalLevel.LEVEL_1_MANAGER, nullable=False, index=True)
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    required_approver_role = Column(String, nullable=True)  # "MANAGER" or "ADMIN"
    
    # Approval metadata
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    
    # SLA tracking
    sla_status = Column(String, nullable=True, index=True)
    sla_due_time = Column(DateTime, nullable=True, index=True)
    is_escalated = Column(Boolean, default=False, nullable=False, index=True)
    current_escalation_to = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    escalated_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Relationships
    requester = relationship("User", foreign_keys=[requested_by])
    assigned_approver = relationship("User", foreign_keys=[assigned_to])
    approver_user = relationship("User", foreign_keys=[approved_by])
    rejector_user = relationship("User", foreign_keys=[rejected_by])
    escalation_user = relationship("User", foreign_keys=[current_escalation_to])
    tenant = relationship("Tenant", back_populates="approvals")
    workspace = relationship("Workspace")
    channel = relationship("Channel")
    history = relationship("ApprovalHistory", back_populates="approval", cascade="all, delete-orphan")
