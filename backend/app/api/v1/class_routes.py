"""Classes routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_trainer
from app.models.class_model import GroupClass, ClassEnrollment, ClassAttendance, ClassSchedule
from app.models.member import Member
from datetime import datetime

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.get("/")
async def list_classes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    branch_id: Optional[int] = None,
    class_type: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all group classes."""
    query = db.query(GroupClass)
    
    if branch_id:
        query = query.filter(GroupClass.branch_id == branch_id)
    if class_type:
        query = query.filter(GroupClass.class_type == class_type)
    
    query = query.filter(GroupClass.is_active == True)
    
    total = query.count()
    classes = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": classes
    }


@router.get("/{class_id}")
async def get_class(
    class_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get class details."""
    group_class = db.query(GroupClass).filter(GroupClass.id == class_id).first()
    
    if not group_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    return group_class


@router.get("/{class_id}/schedules")
async def get_class_schedules(
    class_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get class schedule."""
    group_class = db.query(GroupClass).filter(GroupClass.id == class_id).first()
    
    if not group_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    schedules = db.query(ClassSchedule).filter(ClassSchedule.group_class_id == class_id).all()
    return schedules


@router.post("/{class_id}/enroll")
async def enroll_in_class(
    class_id: int,
    member_id: int,
    enrollment_type: str = "regular",
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enroll member in class."""
    group_class = db.query(GroupClass).filter(GroupClass.id == class_id).first()
    if not group_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Check if already enrolled
    existing = db.query(ClassEnrollment).filter(
        ClassEnrollment.group_class_id == class_id,
        ClassEnrollment.member_id == member_id,
        ClassEnrollment.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already enrolled in this class"
        )
    
    enrollment = ClassEnrollment(
        group_class_id=class_id,
        member_id=member_id,
        enrollment_type=enrollment_type,
        enrolled_date=datetime.utcnow()
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return {"message": "Member enrolled successfully", "enrollment_id": enrollment.id}


@router.get("/{class_id}/attendance")
async def get_class_attendance(
    class_id: int,
    session_date: Optional[datetime] = None,
    current_user = Depends(get_current_trainer),
    db: Session = Depends(get_db)
):
    """Get class attendance records."""
    group_class = db.query(GroupClass).filter(GroupClass.id == class_id).first()
    if not group_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    query = db.query(ClassAttendance).filter(ClassAttendance.group_class_id == class_id)
    
    if session_date:
        query = query.filter(ClassAttendance.session_date.cast(String) == session_date.strftime("%Y-%m-%d"))
    
    attendance = query.all()
    return attendance
