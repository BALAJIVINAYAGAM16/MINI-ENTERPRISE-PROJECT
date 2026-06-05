from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship
import enum

class ApprovalActionType(str, enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    ON_HOLD = "ON_HOLD"
    DELEGATED = "DELEGATED"

class ApprovalHistory(Base):
    __tablename__ = "approval_history"

    id = Column(Integer, primary_key=True)
    approval_id = Column(Integer, ForeignKey("approvals.id"), nullable=False)
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(Enum(ApprovalActionType), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    approval = relationship("Approval", back_populates="history")
    user = relationship("User", foreign_keys=[action_by])