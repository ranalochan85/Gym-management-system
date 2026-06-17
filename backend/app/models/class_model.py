"""Group classes and scheduling models."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class GroupClass(BaseModel):
    """Group class definition model."""
    __tablename__ = "group_classes"

    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    class_type = Column(String(100), nullable=False)  # yoga, pilates, zumba, hiit, etc.
    capacity = Column(Integer, default=20)
    duration_minutes = Column(Integer, nullable=False)
    difficulty_level = Column(String(50), nullable=False)  # beginner, intermediate, advanced
    price_per_session = Column(Integer, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    branch = relationship("Branch", back_populates="classes")
    trainer = relationship("Trainer", back_populates="classes")
    schedules = relationship("ClassSchedule", back_populates="group_class", cascade="all, delete-orphan")
    enrollments = relationship("ClassEnrollment", back_populates="group_class", cascade="all, delete-orphan")
    attendance = relationship("ClassAttendance", back_populates="group_class", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<GroupClass(id={self.id}, name={self.name}, branch_id={self.branch_id})>"


class ClassSchedule(BaseModel):
    """Class schedule/session."""
    __tablename__ = "class_schedules"

    group_class_id = Column(Integer, ForeignKey("group_classes.id"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String(10), nullable=False)  # HH:MM
    end_time = Column(String(10), nullable=False)  # HH:MM
    location = Column(String(255), nullable=True)  # Room/Zone in gym
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    group_class = relationship("GroupClass", back_populates="schedules")

    def __repr__(self):
        return f"<ClassSchedule(class_id={self.group_class_id}, day={self.day_of_week})>"


class ClassEnrollment(BaseModel):
    """Member enrollment in class."""
    __tablename__ = "class_enrollments"

    group_class_id = Column(Integer, ForeignKey("group_classes.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    enrolled_date = Column(DateTime, default=datetime.utcnow)
    enrollment_type = Column(String(50), default="regular")  # regular, trial, drop-in
    sessions_purchased = Column(Integer, nullable=True)
    sessions_used = Column(Integer, default=0)
    expiry_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    group_class = relationship("GroupClass", back_populates="enrollments")
    member = relationship("Member", back_populates="class_enrollments")

    def __repr__(self):
        return f"<ClassEnrollment(class_id={self.group_class_id}, member_id={self.member_id})>"


class ClassAttendance(BaseModel):
    """Class attendance record."""
    __tablename__ = "class_attendance"

    group_class_id = Column(Integer, ForeignKey("group_classes.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    session_date = Column(DateTime, nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=True)
    attendance_status = Column(String(50), default="present")  # present, absent, late, cancelled
    notes = Column(Text, nullable=True)
    
    # Relationships
    group_class = relationship("GroupClass", back_populates="attendance")
    member = relationship("Member")

    def __repr__(self):
        return f"<ClassAttendance(class_id={self.group_class_id}, member_id={self.member_id}, date={self.session_date})>"
