"""Workout and fitness models."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel
from app.core.constants import DifficultyLevel, WorkoutType, MuscleGroup


class Exercise(BaseModel):
    """Exercise library model."""
    __tablename__ = "exercises"

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    difficulty_level = Column(SQLEnum(DifficultyLevel), nullable=False)
    workout_type = Column(SQLEnum(WorkoutType), nullable=False)
    muscle_groups = Column(String(500), nullable=False)  # comma-separated
    equipment_required = Column(String(255), nullable=True)
    sets = Column(Integer, default=3)
    reps = Column(String(50), nullable=True)  # e.g., "10-12"
    duration_seconds = Column(Integer, nullable=True)
    rest_seconds = Column(Integer, default=60)
    calorie_burn = Column(Float, nullable=True)  # per rep/minute
    video_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    instructions = Column(Text, nullable=True)
    variations = Column(Text, nullable=True)  # comma-separated variations
    
    # Relationships
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, difficulty={self.difficulty_level})>"


class WorkoutPlan(BaseModel):
    """Personalized workout plan."""
    __tablename__ = "workout_plans"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    difficulty_level = Column(SQLEnum(DifficultyLevel), nullable=False)
    workout_type = Column(SQLEnum(WorkoutType), nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    sessions_per_week = Column(Integer, default=3)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    goal = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    member = relationship("Member", back_populates="workouts")
    trainer = relationship("Trainer")
    exercises = relationship("WorkoutExercise", back_populates="workout_plan", cascade="all, delete-orphan")
    sessions = relationship("WorkoutSession", back_populates="workout_plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkoutPlan(id={self.id}, member_id={self.member_id}, name={self.name})>"


class WorkoutExercise(BaseModel):
    """Exercise in a workout plan."""
    __tablename__ = "workout_exercises"

    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    sequence_order = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=True)  # Override exercise default
    reps = Column(String(50), nullable=True)  # Override exercise default
    rest_seconds = Column(Integer, nullable=True)  # Override exercise default
    notes = Column(Text, nullable=True)
    
    # Relationships
    workout_plan = relationship("WorkoutPlan", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")

    def __repr__(self):
        return f"<WorkoutExercise(workout_id={self.workout_plan_id}, exercise_id={self.exercise_id})>"


class WorkoutSession(BaseModel):
    """Individual workout session."""
    __tablename__ = "workout_sessions"

    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=False, index=True)
    session_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    calories_burned = Column(Float, nullable=True)
    intensity_level = Column(String(50), nullable=True)  # low, medium, high
    status = Column(String(50), default="pending")  # pending, completed, skipped, cancelled
    notes = Column(Text, nullable=True)
    trainer_notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 user satisfaction
    
    # Relationships
    workout_plan = relationship("WorkoutPlan", back_populates="sessions")
    exercise_logs = relationship("ExerciseLog", back_populates="workout_session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkoutSession(workout_plan_id={self.workout_plan_id}, date={self.session_date})>"


class ExerciseLog(BaseModel):
    """Log of exercise performance."""
    __tablename__ = "exercise_logs"

    workout_session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    sets_completed = Column(Integer, nullable=True)
    reps_completed = Column(String(50), nullable=True)
    weight_used = Column(Float, nullable=True)  # in kg
    duration_seconds = Column(Integer, nullable=True)
    calories_burned = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    workout_session = relationship("WorkoutSession", back_populates="exercise_logs")
    exercise = relationship("Exercise")

    def __repr__(self):
        return f"<ExerciseLog(workout_session_id={self.workout_session_id}, exercise_id={self.exercise_id})>"


class BodyProgress(BaseModel):
    """Body progress tracking."""
    __tablename__ = "body_progress"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    measurement_date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float, nullable=False)  # in kg
    height = Column(Float, nullable=True)  # in cm
    body_fat_percentage = Column(Float, nullable=True)
    muscle_mass = Column(Float, nullable=True)  # in kg
    bmi = Column(Float, nullable=True)
    chest = Column(Float, nullable=True)  # in cm
    waist = Column(Float, nullable=True)  # in cm
    hips = Column(Float, nullable=True)  # in cm
    thigh = Column(Float, nullable=True)  # in cm
    arm = Column(Float, nullable=True)  # in cm
    before_photo = Column(String(500), nullable=True)
    after_photo = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    member = relationship("Member", back_populates="progress")

    def __repr__(self):
        return f"<BodyProgress(member_id={self.member_id}, date={self.measurement_date}, weight={self.weight})>"
