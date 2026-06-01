# models/sla_rule.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from app.db.database import Base


class SLARule(Base):
    __tablename__ = "sla_rules"

    id = Column(Integer, primary_key=True, index=True)

    module_name = Column(String(100), nullable=False)
    priority = Column(String(50), nullable=False)

    allowed_hours = Column(Integer, nullable=False)

    escalation_enabled = Column(Boolean, default=False)
    escalation_after_hours = Column(Integer)

    is_active = Column(Boolean, default=True)

    created_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )