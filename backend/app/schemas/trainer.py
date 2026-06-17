"""Trainer schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class TrainerBase(BaseModel):
    """Base trainer schema."""
    specializations: Optional[str] = None
    years_experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    bio: Optional[str] = None


class TrainerCreate(TrainerBase):
    """Trainer creation schema."""
    user_id: int
    branch_id: int


class TrainerUpdate(TrainerBase):
    """Trainer update schema."""
    availability_status: Optional[str] = None


class TrainerResponse(TrainerBase):
    """Trainer response schema."""
    id: int
    user_id: int
    branch_id: int
    hire_date: datetime
    availability_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrainerPerformanceResponse(BaseModel):
    """Trainer performance response."""
    total_sessions: int
    completed_sessions: int
    member_satisfaction_rating: Optional[float]
    average_member_progress: Optional[float]
    revenue_generated: float
