"""User and authentication models."""

from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel
from app.core.constants import UserRole


class User(BaseModel):
    """User model."""
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    profile_picture = Column(String(500), nullable=True)
    
    # Relationships
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trainer = relationship("Trainer", back_populates="user", uselist=False, cascade="all, delete-orphan")
    staff = relationship("Staff", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class UserSession(BaseModel):
    """User session model for tracking active sessions."""
    __tablename__ = "user_sessions"

    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(500), unique=True, nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession(user_id={self.user_id}, token={self.token[:20]}...)>"


class AuditLog(BaseModel):
    """Audit log model for tracking user activities."""
    __tablename__ = "audit_logs"

    user_id = Column(Integer, nullable=True, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    old_values = Column(String(2000), nullable=True)
    new_values = Column(String(2000), nullable=True)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(50), default="success")
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(user_id={self.user_id}, action={self.action}, entity={self.entity_type})>"
