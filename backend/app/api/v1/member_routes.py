"""Member routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_manager
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse, MembershipResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.models.member import Member, Membership
from app.models.user import User

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=PaginatedResponse[MemberResponse])
async def list_members(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    branch_id: Optional[int] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all members."""
    query = db.query(Member)
    
    if branch_id:
        query = query.filter(Member.branch_id == branch_id)
    
    if search:
        query = query.join(User).filter(
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    total = query.count()
    members = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": members
    }


@router.post("/", response_model=MemberResponse)
async def create_member(
    member_data: MemberCreate,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Create a new member."""
    # Check if user exists
    user = db.query(User).filter(User.id == member_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if member already exists
    existing = db.query(Member).filter(Member.user_id == member_data.user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already exists"
        )
    
    new_member = Member(**member_data.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return new_member


@router.get("/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get member details."""
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    return member


@router.put("/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: int,
    member_data: MemberUpdate,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Update member."""
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    update_data = member_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)
    
    db.commit()
    db.refresh(member)
    
    return member


@router.delete("/{member_id}")
async def delete_member(
    member_id: int,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Delete member."""
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    db.delete(member)
    db.commit()
    
    return {"message": "Member deleted successfully"}


@router.get("/{member_id}/memberships", response_model=List[MembershipResponse])
async def get_member_memberships(
    member_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get member's memberships."""
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    memberships = db.query(Membership).filter(Membership.member_id == member_id).all()
    return memberships
