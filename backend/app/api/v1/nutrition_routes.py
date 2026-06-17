"""Nutrition routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_trainer
from app.models.nutrition import DietPlan, Meal, NutritionTracking
from app.models.member import Member
from datetime import datetime

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.get("/diet-plans/{member_id}")
async def get_member_diet_plans(
    member_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get member's diet plans."""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    plans = db.query(DietPlan).filter(
        DietPlan.member_id == member_id,
        DietPlan.is_active == True
    ).all()
    
    return plans


@router.post("/diet-plans")
async def create_diet_plan(
    plan_data: dict,
    current_user = Depends(get_current_trainer),
    db: Session = Depends(get_db)
):
    """Create diet plan."""
    member = db.query(Member).filter(Member.id == plan_data.get("member_id")).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    new_plan = DietPlan(**plan_data)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    return new_plan


@router.get("/diet-plans/{diet_plan_id}/meals")
async def get_diet_plan_meals(
    diet_plan_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get meals in diet plan."""
    plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    meals = db.query(Meal).filter(Meal.diet_plan_id == diet_plan_id).all()
    return meals


@router.post("/diet-plans/{diet_plan_id}/meals")
async def add_meal_to_plan(
    diet_plan_id: int,
    meal_data: dict,
    current_user = Depends(get_current_trainer),
    db: Session = Depends(get_db)
):
    """Add meal to diet plan."""
    plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    new_meal = Meal(
        diet_plan_id=diet_plan_id,
        **meal_data
    )
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    
    return new_meal


@router.get("/tracking/{diet_plan_id}")
async def get_nutrition_tracking(
    diet_plan_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get nutrition tracking for diet plan."""
    plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    tracking = db.query(NutritionTracking).filter(
        NutritionTracking.diet_plan_id == diet_plan_id
    ).order_by(NutritionTracking.tracking_date.desc()).all()
    
    return tracking


@router.post("/tracking/{diet_plan_id}")
async def log_nutrition(
    diet_plan_id: int,
    tracking_data: dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Log nutrition intake."""
    plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    new_tracking = NutritionTracking(
        diet_plan_id=diet_plan_id,
        tracking_date=datetime.utcnow(),
        **tracking_data
    )
    db.add(new_tracking)
    db.commit()
    db.refresh(new_tracking)
    
    return new_tracking
