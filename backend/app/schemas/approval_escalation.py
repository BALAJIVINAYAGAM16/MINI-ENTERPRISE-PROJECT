from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ApprovalEscalationCreate(BaseModel):
    approval_id: int
    escalated_to: int
    reason: str = Field(..., min_length=1)

    @field_validator("reason")
    @classmethod
    def reason_required(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Reason is required")
        return value


class ApprovalEscalationOut(BaseModel):
    id: int

    approval_id: int

    escalated_from: int
    escalated_to: int

    reason: str

    escalation_level: int

    status: str

    escalated_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True
