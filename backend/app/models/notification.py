"""Notification models."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel
from app.core.constants import NotificationType


class Notification(BaseModel):
    """Notification record model."""
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    related_entity_type = Column(String(100), nullable=True)  # member, payment, workout, etc.
    related_entity_id = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    action_url = Column(String(500), nullable=True)
    
    # Relationships
    user = relationship("User")
    delivery_logs = relationship("NotificationLog", back_populates="notification", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type})>"


class NotificationLog(BaseModel):
    """Notification delivery log."""
    __tablename__ = "notification_logs"

    notification_id = Column(Integer, ForeignKey("notifications.id"), nullable=False, index=True)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    recipient = Column(String(255), nullable=False)  # email or phone
    status = Column(String(50), default="pending")  # pending, sent, failed, bounced
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Relationships
    notification = relationship("Notification", back_populates="delivery_logs")

    def __repr__(self):
        return f"<NotificationLog(notification_id={self.notification_id}, status={self.status})>"


class NotificationTemplate(BaseModel):
    """Email/SMS template model."""
    __tablename__ = "notification_templates"

    name = Column(String(255), unique=True, nullable=False)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    subject = Column(String(255), nullable=True)  # For email
    body = Column(Text, nullable=False)
    variables = Column(String(500), nullable=True)  # comma-separated, e.g., {name}, {email}
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<NotificationTemplate(id={self.id}, name={self.name})>"
