from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class SLARuleCreate(BaseModel):
    module_name: str
    priority: str
    allowed_hours: int = Field(..., gt=0)
    escalation_enabled: bool = False
    escalation_after_hours: Optional[int] = Field(default=None, gt=0)
    is_active: bool = True

    @field_validator("module_name", "priority")
    @classmethod
    def required_text(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Value is required")
        return value


class SLARuleUpdate(BaseModel):
    module_name: Optional[str] = None
    priority: Optional[str] = None
    allowed_hours: Optional[int] = Field(default=None, gt=0)
    escalation_enabled: Optional[bool] = None
    escalation_after_hours: Optional[int] = Field(default=None, gt=0)
    is_active: Optional[bool] = None

    @field_validator("module_name", "priority")
    @classmethod
    def optional_text(cls, value: Optional[str]):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Value is required")
        return value


class SLARuleOut(SLARuleCreate):
    id: int
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
