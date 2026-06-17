"""Payment schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.core.constants import PaymentStatus, PaymentMethod


class PaymentBase(BaseModel):
    """Base payment schema."""
    amount: float = Field(..., gt=0)
    payment_method: PaymentMethod
    payment_type: str


class PaymentCreate(PaymentBase):
    """Payment creation schema."""
    member_id: int
    branch_id: int
    description: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Payment response schema."""
    id: int
    member_id: int
    branch_id: int
    status: PaymentStatus
    payment_date: datetime
    reference_id: Optional[str]
    receipt_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    """Invoice response schema."""
    id: int
    invoice_number: str
    invoice_date: datetime
    subtotal: float
    tax: float
    total: float
    due_date: Optional[datetime]

    class Config:
        from_attributes = True
