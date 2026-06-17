"""Attendance model."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel
from app.core.constants import AttendanceStatus


class Attendance(BaseModel):
    """Attendance record model."""
    __tablename__ = "attendance"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=True)
    status = Column(SQLEnum(AttendanceStatus), default=AttendanceStatus.PRESENT, nullable=False)
    duration_minutes = Column(Integer, nullable=True)  # calculated after check-out
    calories_burned = Column(Float, nullable=True)
    equipment_used = Column(String(500), nullable=True)  # comma-separated
    notes = Column(Text, nullable=True)
    recorded_by = Column(Integer, nullable=True)  # Staff ID
    source = Column(String(50), default="manual")  # manual, qr_code, rfid
    
    # Relationships
    member = relationship("Member", back_populates="attendance_records")
    branch = relationship("Branch")

    def __repr__(self):
        return f"<Attendance(member_id={self.member_id}, check_in={self.check_in_time})>"


class QRCode(BaseModel):
    """QR Code for members."""
    __tablename__ = "qr_codes"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True, unique=True)
    qr_code_data = Column(String(500), unique=True, nullable=False)
    generated_date = Column(DateTime, default=datetime.utcnow)
    expires_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    member = relationship("Member")

    def __repr__(self):
        return f"<QRCode(member_id={self.member_id})>"


class RFIDCard(BaseModel):
    """RFID Card mapping."""
    __tablename__ = "rfid_cards"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True, unique=True)
    rfid_number = Column(String(100), unique=True, nullable=False)
    issued_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    member = relationship("Member")

    def __repr__(self):
        return f"<RFIDCard(member_id={self.member_id}, rfid={self.rfid_number})>"
