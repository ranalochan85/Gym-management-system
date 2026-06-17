"""Member schemas."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
from app.core.constants import MembershipStatus, MembershipType


class MemberBase(BaseModel):
    """Base member schema."""
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None


class MemberCreate(MemberBase):
    """Member creation schema."""
    user_id: int
    branch_id: int


class MemberUpdate(MemberBase):
    """Member update schema."""
    pass


class MemberResponse(MemberBase):
    """Member response schema."""
    id: int
    user_id: int
    branch_id: int
    member_since: datetime
    qr_code: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MembershipBase(BaseModel):
    """Base membership schema."""
    membership_type: MembershipType
    amount: float = Field(..., gt=0)


class MembershipCreate(MembershipBase):
    """Membership creation schema."""
    member_id: int
    end_date: datetime


class MembershipUpdate(BaseModel):
    """Membership update schema."""
    status: Optional[MembershipStatus] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None


class MembershipResponse(MembershipBase):
    """Membership response schema."""
    id: int
    member_id: int
    status: MembershipStatus
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
