"""Branch routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.dependencies import get_current_manager
from app.models.branch import Branch, Gym, BranchTiming
from app.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/")
async def list_branches(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    gym_id: Optional[int] = None,
    city: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all branches."""
    query = db.query(Branch)
    
    if gym_id:
        query = query.filter(Branch.gym_id == gym_id)
    if city:
        query = query.filter(Branch.city.ilike(f"%{city}%"))
    
    total = query.count()
    branches = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": branches
    }


@router.get("/{branch_id}")
async def get_branch(
    branch_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get branch details."""
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )
    
    return branch


@router.get("/{branch_id}/timings")
async def get_branch_timings(
    branch_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get branch operating hours."""
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )
    
    timings = db.query(BranchTiming).filter(BranchTiming.branch_id == branch_id).all()
    return timings


@router.get("/{branch_id}/stats")
async def get_branch_stats(
    branch_id: int,
    current_user = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Get branch statistics."""
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )
    
    from app.models.member import Member, Membership
    from app.models.trainer import Trainer
    from app.models.staff import Staff
    
    total_members = db.query(Member).filter(Member.branch_id == branch_id).count()
    active_memberships = db.query(Membership).filter(
        Membership.branch_id == branch_id,
        Membership.status == "active"
    ).count()
    trainers = db.query(Trainer).filter(Trainer.branch_id == branch_id).count()
    staff = db.query(Staff).filter(Staff.branch_id == branch_id).count()
    
    return {
        "branch_id": branch_id,
        "total_members": total_members,
        "active_memberships": active_memberships,
        "trainers": trainers,
        "staff": staff,
        "capacity_utilization": (active_memberships / branch.capacity * 100) if branch.capacity > 0 else 0
    }
