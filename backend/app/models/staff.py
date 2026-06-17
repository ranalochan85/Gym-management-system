"""Staff model."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class Staff(BaseModel):
    """Staff member model."""
    __tablename__ = "staff"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    designation = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    salary = Column(Float, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    hire_date = Column(DateTime, default=datetime.utcnow)
    contract_end_date = Column(DateTime, nullable=True)
    emergency_contact = Column(String(100), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zipcode = Column(String(20), nullable=True)
    profile_image = Column(String(500), nullable=True)
    bank_account = Column(String(50), nullable=True)
    bank_name = Column(String(100), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="staff")
    branch = relationship("Branch", back_populates="staff_members")
    schedules = relationship("StaffSchedule", back_populates="staff", cascade="all, delete-orphan")
    performance = relationship("StaffPerformance", back_populates="staff", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Staff(id={self.id}, user_id={self.user_id}, designation={self.designation})>"


class StaffSchedule(BaseModel):
    """Staff work schedule."""
    __tablename__ = "staff_schedules"

    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String(10), nullable=False)  # HH:MM
    end_time = Column(String(10), nullable=False)  # HH:MM
    is_available = Column(Boolean, default=True)
    
    # Relationships
    staff = relationship("Staff", back_populates="schedules")

    def __repr__(self):
        return f"<StaffSchedule(staff_id={self.staff_id}, day={self.day_of_week})>"


class StaffPerformance(BaseModel):
    """Staff performance metrics."""
    __tablename__ = "staff_performance"

    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False, index=True)
    month = Column(DateTime, nullable=False)
    attendance_percentage = Column(Float, nullable=True)
    performance_rating = Column(Float, nullable=True)  # 1-5
    tasks_completed = Column(Integer, default=0)
    customer_feedback = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    staff = relationship("Staff", back_populates="performance")

    def __repr__(self):
        return f"<StaffPerformance(staff_id={self.staff_id}, month={self.month})>"
