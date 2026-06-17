"""Workout routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_trainer
from app.models.workout import (
    Exercise, WorkoutPlan, WorkoutSession, ExerciseLog, BodyProgress
)
from app.models.member import Member
from datetime import datetime

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/exercises")
async def list_exercises(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    difficulty: Optional[str] = None,
    workout_type: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all exercises."""
    query = db.query(Exercise)
    
    if difficulty:
        query = query.filter(Exercise.difficulty_level == difficulty)
    if workout_type:
        query = query.filter(Exercise.workout_type == workout_type)
    
    total = query.count()
    exercises = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": exercises
    }


@router.get("/plans/{member_id}")
async def get_member_workout_plans(
    member_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get member's workout plans."""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    plans = db.query(WorkoutPlan).filter(
        WorkoutPlan.member_id == member_id,
        WorkoutPlan.is_active == True
    ).all()
    
    return plans


@router.post("/plans")
async def create_workout_plan(
    plan_data: dict,
    current_user = Depends(get_current_trainer),
    db: Session = Depends(get_db)
):
    """Create workout plan."""
    member = db.query(Member).filter(Member.id == plan_data.get("member_id")).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    new_plan = WorkoutPlan(**plan_data)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    return new_plan


@router.get("/sessions/{member_id}")
async def get_member_workout_sessions(
    member_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get member's workout sessions."""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    sessions = db.query(WorkoutSession).join(
        WorkoutPlan
    ).filter(WorkoutPlan.member_id == member_id).all()
    
    return sessions


@router.post("/sessions/{workout_plan_id}")
async def log_workout_session(
    workout_plan_id: int,
    session_data: dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Log workout session."""
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == workout_plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
    
    new_session = WorkoutSession(
        workout_plan_id=workout_plan_id,
        **session_data
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return new_session


@router.get("/progress/{member_id}")
async def get_body_progress(
    member_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get member's body progress."""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    progress = db.query(BodyProgress).filter(
        BodyProgress.member_id == member_id
    ).order_by(BodyProgress.measurement_date.desc()).all()
    
    return progress


@router.post("/progress/{member_id}")
async def record_body_progress(
    member_id: int,
    progress_data: dict,
    current_user = Depends(get_current_trainer),
    db: Session = Depends(get_db)
):
    """Record body progress."""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    new_progress = BodyProgress(
        member_id=member_id,
        measurement_date=datetime.utcnow(),
        **progress_data
    )
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    
    return new_progress
