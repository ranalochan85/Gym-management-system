"""Payment routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_manager
from app.schemas.payment import PaymentCreate, PaymentResponse, InvoiceResponse
from app.schemas.pagination import PaginatedResponse
from app.models.payment import Payment, Invoice
from app.models.member import Member
from app.core.constants import PaymentStatus
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=PaginatedResponse[PaymentResponse])
async def list_payments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    member_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    status_filter: Optional[PaymentStatus] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List payments."""
    query = db.query(Payment)
    
    if member_id:
        query = query.filter(Payment.member_id == member_id)
    if branch_id:
        query = query.filter(Payment.branch_id == branch_id)
    if status_filter:
        query = query.filter(Payment.status == status_filter)
    
    total = query.count()
    payments = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": payments
    }


@router.post("/", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Create a payment."""
    # Verify member exists
    member = db.query(Member).filter(Member.id == payment_data.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    payment = Payment(
        member_id=payment_data.member_id,
        branch_id=payment_data.branch_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        payment_type=payment_data.payment_type,
        status=PaymentStatus.COMPLETED,
        payment_date=datetime.utcnow(),
        description=payment_data.description
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return payment


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get payment details."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment


@router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: int,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Refund a payment."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    if payment.status == PaymentStatus.REFUNDED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already refunded"
        )
    
    payment.status = PaymentStatus.REFUNDED
    db.commit()
    
    return {"message": "Payment refunded successfully"}


@router.get("/{payment_id}/invoice", response_model=InvoiceResponse)
async def get_invoice(
    payment_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get payment invoice."""
    invoice = db.query(Invoice).filter(Invoice.payment_id == payment_id).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    return invoice
