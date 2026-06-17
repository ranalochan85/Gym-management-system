"""Nutrition and diet models."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class DietPlan(BaseModel):
    """Diet plan model."""
    __tablename__ = "diet_plans"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    diet_type = Column(String(100), nullable=True)  # e.g., keto, vegan, balanced
    calories_per_day = Column(Float, nullable=False)
    protein_grams = Column(Float, nullable=False)
    carbs_grams = Column(Float, nullable=False)
    fats_grams = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    goal = Column(String(255), nullable=True)  # e.g., weight loss, muscle gain
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    member = relationship("Member", back_populates="diet_plans")
    trainer = relationship("Trainer")
    meals = relationship("Meal", back_populates="diet_plan", cascade="all, delete-orphan")
    tracking = relationship("NutritionTracking", back_populates="diet_plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DietPlan(id={self.id}, member_id={self.member_id}, name={self.name})>"


class Meal(BaseModel):
    """Meal in a diet plan."""
    __tablename__ = "meals"

    diet_plan_id = Column(Integer, ForeignKey("diet_plans.id"), nullable=False, index=True)
    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    calories = Column(Float, nullable=False)
    protein_grams = Column(Float, nullable=False)
    carbs_grams = Column(Float, nullable=False)
    fats_grams = Column(Float, nullable=False)
    fiber_grams = Column(Float, nullable=True)
    ingredients = Column(Text, nullable=True)  # comma-separated
    preparation_instructions = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    
    # Relationships
    diet_plan = relationship("DietPlan", back_populates="meals")

    def __repr__(self):
        return f"<Meal(id={self.id}, diet_plan_id={self.diet_plan_id}, meal_type={self.meal_type})>"


class NutritionTracking(BaseModel):
    """Nutrition tracking record."""
    __tablename__ = "nutrition_tracking"

    diet_plan_id = Column(Integer, ForeignKey("diet_plans.id"), nullable=False, index=True)
    tracking_date = Column(DateTime, default=datetime.utcnow)
    calories_consumed = Column(Float, nullable=True)
    protein_consumed = Column(Float, nullable=True)
    carbs_consumed = Column(Float, nullable=True)
    fats_consumed = Column(Float, nullable=True)
    water_intake_liters = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    diet_plan = relationship("DietPlan", back_populates="tracking")

    def __repr__(self):
        return f"<NutritionTracking(diet_plan_id={self.diet_plan_id}, date={self.tracking_date})>"
