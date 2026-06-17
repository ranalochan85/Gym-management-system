"""Branch model."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class Branch(BaseModel):
    """Branch model."""
    __tablename__ = "branches"

    gym_id = Column(Integer, ForeignKey("gyms.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zipcode = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    manager_id = Column(Integer, nullable=True)  # Staff ID
    established_date = Column(DateTime, default=datetime.utcnow)
    branch_image = Column(String(500), nullable=True)
    total_area = Column(Float, nullable=True)  # in sq ft
    number_of_equipment = Column(Integer, default=0)
    capacity = Column(Integer, default=100)
    
    # Relationships
    gym = relationship("Gym", back_populates="branches")
    timings = relationship("BranchTiming", back_populates="branch", cascade="all, delete-orphan")
    members = relationship("Member", back_populates="branch", cascade="all, delete-orphan")
    trainers = relationship("Trainer", back_populates="branch", cascade="all, delete-orphan")
    staff_members = relationship("Staff", back_populates="branch", cascade="all, delete-orphan")
    memberships = relationship("Membership", back_populates="branch", cascade="all, delete-orphan")
    equipment = relationship("Equipment", back_populates="branch", cascade="all, delete-orphan")
    classes = relationship("GroupClass", back_populates="branch", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Branch(id={self.id}, name={self.name}, city={self.city})>"


class BranchTiming(BaseModel):
    """Branch operating hours."""
    __tablename__ = "branch_timings"

    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    opening_time = Column(String(10), nullable=False)  # HH:MM
    closing_time = Column(String(10), nullable=False)  # HH:MM
    is_open = Column(Boolean, default=True)
    
    # Relationships
    branch = relationship("Branch", back_populates="timings")

    def __repr__(self):
        return f"<BranchTiming(branch_id={self.branch_id}, day={self.day_of_week})>"


class Gym(BaseModel):
    """Gym main entity."""
    __tablename__ = "gyms"

    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    logo = Column(String(500), nullable=True)
    established_date = Column(DateTime, default=datetime.utcnow)
    total_branches = Column(Integer, default=1)
    
    # Relationships
    branches = relationship("Branch", back_populates="gym", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Gym(id={self.id}, name={self.name}, branches={self.total_branches})>"
