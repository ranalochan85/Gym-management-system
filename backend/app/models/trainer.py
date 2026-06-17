"""Trainer model."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class Trainer(BaseModel):
    """Trainer model."""
    __tablename__ = "trainers"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    specializations = Column(String(500), nullable=True)  # comma-separated
    years_experience = Column(Integer, nullable=True)
    hourly_rate = Column(Float, nullable=True)
    bio = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    hire_date = Column(DateTime, default=datetime.utcnow)
    profile_image = Column(String(500), nullable=True)
    availability_status = Column(String(50), default="available")  # available, busy, on_leave
    
    # Relationships
    user = relationship("User", back_populates="trainer")
    branch = relationship("Branch", back_populates="trainers")
    certifications_rel = relationship("TrainerCertification", back_populates="trainer", cascade="all, delete-orphan")
    member_assignments = relationship("TrainerMemberAssignment", back_populates="trainer", cascade="all, delete-orphan")
    performance = relationship("TrainerPerformance", back_populates="trainer", cascade="all, delete-orphan")
    schedules = relationship("TrainerSchedule", back_populates="trainer", cascade="all, delete-orphan")
    classes = relationship("GroupClass", back_populates="trainer")

    def __repr__(self):
        return f"<Trainer(id={self.id}, user_id={self.user_id}, branch_id={self.branch_id})>"


class TrainerCertification(BaseModel):
    """Trainer certification model."""
    __tablename__ = "trainer_certifications"

    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False, index=True)
    certification_name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    certificate_number = Column(String(100), nullable=True)
    certificate_file = Column(String(500), nullable=True)
    
    # Relationships
    trainer = relationship("Trainer", back_populates="certifications_rel")

    def __repr__(self):
        return f"<TrainerCertification(trainer_id={self.trainer_id}, name={self.certification_name})>"


class TrainerMemberAssignment(BaseModel):
    """Trainer-Member assignment model."""
    __tablename__ = "trainer_member_assignments"

    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    assigned_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    sessions_per_week = Column(Integer, default=3)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    trainer = relationship("Trainer", back_populates="member_assignments")
    member = relationship("Member", back_populates="trainer_assignments")

    def __repr__(self):
        return f"<TrainerMemberAssignment(trainer_id={self.trainer_id}, member_id={self.member_id})>"


class TrainerPerformance(BaseModel):
    """Trainer performance metrics."""
    __tablename__ = "trainer_performance"

    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False, index=True)
    month = Column(DateTime, nullable=False)
    total_sessions = Column(Integer, default=0)
    completed_sessions = Column(Integer, default=0)
    member_satisfaction_rating = Column(Float, nullable=True)  # 1-5
    average_member_progress = Column(Float, nullable=True)  # percentage
    revenue_generated = Column(Float, default=0)
    notes = Column(Text, nullable=True)
    
    # Relationships
    trainer = relationship("Trainer", back_populates="performance")

    def __repr__(self):
        return f"<TrainerPerformance(trainer_id={self.trainer_id}, month={self.month})>"


class TrainerSchedule(BaseModel):
    """Trainer working schedule."""
    __tablename__ = "trainer_schedules"

    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String(10), nullable=False)  # HH:MM
    end_time = Column(String(10), nullable=False)  # HH:MM
    is_available = Column(Boolean, default=True)
    
    # Relationships
    trainer = relationship("Trainer", back_populates="schedules")

    def __repr__(self):
        return f"<TrainerSchedule(trainer_id={self.trainer_id}, day={self.day_of_week})>"
