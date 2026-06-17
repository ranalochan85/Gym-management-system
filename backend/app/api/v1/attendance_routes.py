"""Attendance routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.schemas.attendance import AttendanceCheckIn, AttendanceCheckOut, AttendanceResponse
from app.schemas.pagination import PaginatedResponse
from app.models.attendance import Attendance
from app.models.member import Member
from app.core.constants import AttendanceStatus

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/checkin", response_model=AttendanceResponse)
async def check_in(
    attendance_data: AttendanceCheckIn,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Check in member."""
    # Verify member exists
    member = db.query(Member).filter(Member.id == attendance_data.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Check for duplicate check-in today
    today = datetime.utcnow().date()
    today_checkin = db.query(Attendance).filter(
        Attendance.member_id == attendance_data.member_id,
        Attendance.check_in_time >= datetime.combine(today, datetime.min.time()),
        Attendance.check_out_time == None
    ).first()
    
    if today_checkin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already checked in today"
        )
    
    # Create check-in record
    attendance = Attendance(
        member_id=attendance_data.member_id,
        branch_id=attendance_data.branch_id,
        check_in_time=datetime.utcnow(),
        status=AttendanceStatus.PRESENT,
        source="qr_code" if attendance_data.qr_code else "rfid" if attendance_data.rfid_card else "manual"
    )
    
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    return attendance


@router.post("/checkout", response_model=AttendanceResponse)
async def check_out(
    attendance_data: AttendanceCheckOut,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Check out member."""
    # Find active check-in
    attendance = db.query(Attendance).filter(
        Attendance.member_id == attendance_data.member_id,
        Attendance.check_out_time == None
    ).first()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active check-in found"
        )
    
    # Calculate duration
    checkout_time = datetime.utcnow()
    duration = (checkout_time - attendance.check_in_time).total_seconds() / 60
    
    # Update attendance
    attendance.check_out_time = checkout_time
    attendance.duration_minutes = int(duration)
    attendance.calories_burned = attendance_data.calories_burned
    attendance.equipment_used = attendance_data.equipment_used
    attendance.notes = attendance_data.notes
    
    db.commit()
    db.refresh(attendance)
    
    return attendance


@router.get("/", response_model=PaginatedResponse[AttendanceResponse])
async def list_attendance(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    member_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List attendance records."""
    query = db.query(Attendance)
    
    if member_id:
        query = query.filter(Attendance.member_id == member_id)
    if branch_id:
        query = query.filter(Attendance.branch_id == branch_id)
    if date_from:
        query = query.filter(Attendance.check_in_time >= date_from)
    if date_to:
        query = query.filter(Attendance.check_in_time <= date_to)
    
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": records
    }


@router.get("/daily-summary")
async def get_daily_summary(
    branch_id: int,
    date: Optional[datetime] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get daily attendance summary."""
    if not date:
        date = datetime.utcnow().date()
    else:
        date = date.date()
    
    query = db.query(Attendance).filter(
        Attendance.branch_id == branch_id,
        Attendance.check_in_time >= datetime.combine(date, datetime.min.time()),
        Attendance.check_in_time <= datetime.combine(date, datetime.max.time())
    )
    
    total_present = query.filter(Attendance.status == AttendanceStatus.PRESENT).count()
    total_absent = query.filter(Attendance.status == AttendanceStatus.ABSENT).count()
    total_late = query.filter(Attendance.status == AttendanceStatus.LATE).count()
    
    return {
        "date": date,
        "branch_id": branch_id,
        "total_present": total_present,
        "total_absent": total_absent,
        "total_late": total_late,
        "total_checkins": total_present + total_absent + total_late
    }
