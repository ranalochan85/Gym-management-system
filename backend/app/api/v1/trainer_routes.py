"""Trainer routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_manager, get_current_trainer
from app.schemas.trainer import TrainerCreate, TrainerUpdate, TrainerResponse, TrainerPerformanceResponse
from app.schemas.pagination import PaginatedResponse
from app.models.trainer import Trainer, TrainerPerformance
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/trainers", tags=["Trainers"])


@router.get("/", response_model=PaginatedResponse[TrainerResponse])
async def list_trainers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    branch_id: Optional[int] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all trainers."""
    query = db.query(Trainer)
    
    if branch_id:
        query = query.filter(Trainer.branch_id == branch_id)
    
    total = query.count()
    trainers = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": trainers
    }


@router.post("/", response_model=TrainerResponse)
async def create_trainer(
    trainer_data: TrainerCreate,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Create a new trainer."""
    # Check if user exists
    user = db.query(User).filter(User.id == trainer_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if trainer already exists
    existing = db.query(Trainer).filter(Trainer.user_id == trainer_data.user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trainer already exists"
        )
    
    new_trainer = Trainer(**trainer_data.dict())
    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)
    
    return new_trainer


@router.get("/{trainer_id}", response_model=TrainerResponse)
async def get_trainer(
    trainer_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get trainer details."""
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found"
        )
    
    return trainer


@router.put("/{trainer_id}", response_model=TrainerResponse)
async def update_trainer(
    trainer_id: int,
    trainer_data: TrainerUpdate,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Update trainer."""
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found"
        )
    
    update_data = trainer_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(trainer, key, value)
    
    db.commit()
    db.refresh(trainer)
    
    return trainer


@router.get("/{trainer_id}/performance", response_model=TrainerPerformanceResponse)
async def get_trainer_performance(
    trainer_id: int,
    month: Optional[datetime] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get trainer performance metrics."""
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found"
        )
    
    if not month:
        month = datetime.utcnow()
    
    performance = db.query(TrainerPerformance).filter(
        TrainerPerformance.trainer_id == trainer_id,
        TrainerPerformance.month == month
    ).first()
    
    if not performance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance data not found"
        )
    
    return performance
