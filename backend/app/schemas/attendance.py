"""Attendance schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.core.constants import AttendanceStatus


class AttendanceBase(BaseModel):
    """Base attendance schema."""
    member_id: int
    branch_id: int


class AttendanceCheckIn(AttendanceBase):
    """Attendance check-in schema."""
    qr_code: Optional[str] = None
    rfid_card: Optional[str] = None


class AttendanceCheckOut(BaseModel):
    """Attendance check-out schema."""
    member_id: int
    calories_burned: Optional[float] = None
    equipment_used: Optional[str] = None
    notes: Optional[str] = None


class AttendanceResponse(AttendanceBase):
    """Attendance response schema."""
    id: int
    check_in_time: datetime
    check_out_time: Optional[datetime]
    status: AttendanceStatus
    duration_minutes: Optional[int]
    calories_burned: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
