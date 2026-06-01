# models/audit_log.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    ForeignKey
)

from sqlalchemy.sql import func
from app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    action = Column(String, index=True)
    entity = Column(String, index=True)
    entity_id = Column(Integer, index=True)
    timestamp = Column(DateTime, server_default=func.now(), index=True)

    module_name = Column(String(100))

    action_type = Column(String(100))

    record_id = Column(Integer)

    old_data = Column(JSON)
    new_data = Column(JSON)

    ip_address = Column(String(255))
    user_agent = Column(String(500))

    created_at = Column(DateTime, server_default=func.now())
