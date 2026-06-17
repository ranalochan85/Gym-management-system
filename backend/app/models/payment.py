"""Payment and financial models."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel
from app.core.constants import PaymentStatus, PaymentMethod, ExpenseCategory


class Payment(BaseModel):
    """Payment record model."""
    __tablename__ = "payments"

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_type = Column(String(100), nullable=False)  # membership, training, class, other
    reference_id = Column(String(255), nullable=True)  # Transaction ID from gateway
    description = Column(Text, nullable=True)
    paid_by = Column(String(100), nullable=True)  # Name of payer if different from member
    receipt_number = Column(String(100), unique=True, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    member = relationship("Member", back_populates="payments")
    branch = relationship("Branch")
    invoice = relationship("Invoice", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    receipt = relationship("Receipt", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    membership = relationship("Membership", back_populates="payment", uselist=False)

    def __repr__(self):
        return f"<Payment(id={self.id}, member_id={self.member_id}, amount={self.amount}, status={self.status})>"


class Invoice(BaseModel):
    """Invoice model."""
    __tablename__ = "invoices"

    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False, index=True, unique=True)
    invoice_number = Column(String(100), unique=True, nullable=False)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0)
    total = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    notes = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)  # PDF file path
    
    # Relationships
    payment = relationship("Payment", back_populates="invoice")

    def __repr__(self):
        return f"<Invoice(id={self.id}, invoice_number={self.invoice_number})>"


class Receipt(BaseModel):
    """Receipt model."""
    __tablename__ = "receipts"

    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False, index=True, unique=True)
    receipt_number = Column(String(100), unique=True, nullable=False)
    receipt_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    file_path = Column(String(500), nullable=True)  # PDF file path
    email_sent = Column(Boolean, default=False)
    email_sent_date = Column(DateTime, nullable=True)
    
    # Relationships
    payment = relationship("Payment", back_populates="receipt")

    def __repr__(self):
        return f"<Receipt(id={self.id}, receipt_number={self.receipt_number})>"


class Revenue(BaseModel):
    """Revenue tracking model."""
    __tablename__ = "revenue"

    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    revenue_date = Column(DateTime, nullable=False)
    membership_revenue = Column(Float, default=0)
    training_revenue = Column(Float, default=0)
    class_revenue = Column(Float, default=0)
    supplement_revenue = Column(Float, default=0)
    merchandise_revenue = Column(Float, default=0)
    other_revenue = Column(Float, default=0)
    total_revenue = Column(Float, default=0)
    notes = Column(Text, nullable=True)
    
    # Relationships
    branch = relationship("Branch")

    def __repr__(self):
        return f"<Revenue(branch_id={self.branch_id}, date={self.revenue_date}, total={self.total_revenue})>"


class Expense(BaseModel):
    """Expense tracking model."""
    __tablename__ = "expenses"

    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    category = Column(SQLEnum(ExpenseCategory), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(DateTime, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    reference_number = Column(String(100), nullable=True)  # Invoice/Bill number
    vendor = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    receipt_file = Column(String(500), nullable=True)
    
    # Relationships
    branch = relationship("Branch")

    def __repr__(self):
        return f"<Expense(branch_id={self.branch_id}, category={self.category}, amount={self.amount})>"
