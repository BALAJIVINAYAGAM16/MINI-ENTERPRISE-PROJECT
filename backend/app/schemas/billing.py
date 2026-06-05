from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CheckoutRequest(BaseModel):
    customer_id: str
    price_id: str


class CheckoutResponse(BaseModel):
    checkout_url: str


class PlanDetailsResponse(BaseModel):
    credits: int
    price: int
    price_id: Optional[str] = None
    description: str
    features: list[str]


class SubscriptionDetailsResponse(BaseModel):
    id: int
    plan: str
    credits: int
    stripe_customer_id: Optional[str] = None
    is_active: bool
    billing_cycle_start: Optional[datetime] = None
    billing_cycle_end: Optional[datetime] = None
    created_at: datetime
    plan_details: Optional[PlanDetailsResponse] = None

    class Config:
        from_attributes = True
