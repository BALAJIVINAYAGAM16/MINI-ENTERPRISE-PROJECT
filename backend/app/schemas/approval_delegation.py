from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


class ApprovalDelegationCreate(BaseModel):
    delegatee_id: int
    start_date: datetime
    end_date: datetime
    reason: str = Field(..., min_length=1)

    @field_validator("reason")
    @classmethod
    def reason_required(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Reason is required")
        return value

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self


class ApprovalDelegationOut(BaseModel):
    id: int

    delegator_id: int
    delegatee_id: int

    start_date: datetime
    end_date: datetime

    reason: str

    is_active: bool

    class Config:
        from_attributes = True
