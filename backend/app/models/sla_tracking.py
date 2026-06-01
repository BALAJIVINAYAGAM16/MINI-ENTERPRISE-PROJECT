# models/sla_tracking.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func
from app.db.database import Base


class SLATracking(Base):
    __tablename__ = "sla_tracking"

    id = Column(Integer, primary_key=True)

    module_name = Column(String(100), nullable=False)

    record_id = Column(Integer, nullable=False)

    sla_rule_id = Column(Integer, ForeignKey("sla_rules.id"))

    start_time = Column(DateTime, nullable=False)
    due_time = Column(DateTime, nullable=False)

    completed_time = Column(DateTime)

    status = Column(String(50), default="ACTIVE")

    breach_reason = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )