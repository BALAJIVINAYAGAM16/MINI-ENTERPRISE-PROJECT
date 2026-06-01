# models/notification_preference.py

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from app.db.database import Base


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    in_app_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)

    task_notifications = Column(Boolean, default=True)
    approval_notifications = Column(Boolean, default=True)

    escalation_notifications = Column(Boolean, default=True)
    document_notifications = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )