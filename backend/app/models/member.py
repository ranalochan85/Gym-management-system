"""Member model."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, Text, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel
from app.core.constants import MembershipStatus, MembershipType


class Member(BaseModel):
    """Member model."""
    __tablename__ = "members"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zipcode = Column(String(20), nullable=True)
    emergency_contact = Column(String(100), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    height = Column(Float, nullable=True)  # in cm
    weight = Column(Float, nullable=True)  # in kg
    blood_type = Column(String(10), nullable=True)
    medical_conditions = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    qr_code = Column(String(500), nullable=True)
    rfid_card = Column(String(100), nullable=True, unique=True)
    member_since = Column(DateTime, default=datetime.utcnow)
    profile_image = Column(String(500), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="member")
    branch = relationship("Branch", back_populates="members")
    memberships = relationship("Membership", back_populates="member", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="member", cascade="all, delete-orphan")
    trainer_assignments = relationship("TrainerMemberAssignment", back_populates="member", cascade="all, delete-orphan")
    workouts = relationship("WorkoutPlan", back_populates="member", cascade="all, delete-orphan")
    diet_plans = relationship("DietPlan", back_populates="member", cascade="all, delete-orphan")
    progress = relationship("BodyProgress", back_populates="member", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="member", cascade="all, delete-orphan")
    class_enrollments = relationship("ClassEnrollment", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Member(id={self.id}, user_id={self.user_id}, branch_id={self.branch_id})>"


class Membership(BaseModel):
    """Membership model."""
    __tablename__ = "memberships"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    membership_type = Column(SQLEnum(MembershipType), nullable=False)
    status = Column(SQLEnum(MembershipStatus), default=MembershipStatus.ACTIVE, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    notes = Column(Text, nullable=True)
    renewal_reminder_sent = Column(Boolean, default=False)
    
    # Relationships
    member = relationship("Member", back_populates="memberships")
    branch = relationship("Branch", back_populates="memberships")
    payment = relationship("Payment", back_populates="membership")
    history = relationship("MembershipHistory", back_populates="membership", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Membership(member_id={self.member_id}, type={self.membership_type}, status={self.status})>"


class MembershipHistory(BaseModel):
    """Membership history tracking."""
    __tablename__ = "membership_history"

    membership_id = Column(Integer, ForeignKey("memberships.id"), nullable=False, index=True)
    old_status = Column(SQLEnum(MembershipStatus), nullable=True)
    new_status = Column(SQLEnum(MembershipStatus), nullable=True)
    reason = Column(String(255), nullable=True)
    changed_by = Column(Integer, nullable=True)  # User ID who made the change
    
    # Relationships
    membership = relationship("Membership", back_populates="history")

    def __repr__(self):
        return f"<MembershipHistory(membership_id={self.membership_id}, old_status={self.old_status}, new_status={self.new_status})>"
