# models/tenant.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    slug = Column(
        String(100),
        unique=True,
        nullable=False
    )

    contact_email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(50),
        nullable=True
    )

    address = Column(
        String(500),
        nullable=True
    )

    industry = Column(
        String(100),
        nullable=True
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationships

    onboarding = relationship(
        "TenantOnboarding",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan"
    )

    workspaces = relationship(
        "Workspace",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    channels = relationship(
        "Channel",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    collaboration_settings = relationship(
        "TenantCollaborationSettings",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan"
    )

    collaboration_usage = relationship(
        "TenantCollaborationUsage",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan"
    )

    approvals = relationship(
        "Approval",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )