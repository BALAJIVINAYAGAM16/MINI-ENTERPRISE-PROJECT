# models/approval_escalation.py

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    String
)

from sqlalchemy.sql import func
from app.db.database import Base


class ApprovalEscalation(Base):
    __tablename__ = "approval_escalations"

    id = Column(Integer, primary_key=True)

    approval_id = Column(Integer, ForeignKey("approvals.id"))

    escalated_from = Column(Integer, ForeignKey("users.id"))
    escalated_to = Column(Integer, ForeignKey("users.id"))

    reason = Column(Text)

    escalation_level = Column(Integer, default=1)

    status = Column(String(50), default="PENDING")

    escalated_at = Column(DateTime, server_default=func.now())

    resolved_at = Column(DateTime)