# models/approval_delegation.py

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    Text
)

from sqlalchemy.sql import func
from app.db.database import Base


class ApprovalDelegation(Base):
    __tablename__ = "approval_delegations"

    id = Column(Integer, primary_key=True)

    delegator_id = Column(Integer, ForeignKey("users.id"))
    delegatee_id = Column(Integer, ForeignKey("users.id"))

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    reason = Column(Text)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())