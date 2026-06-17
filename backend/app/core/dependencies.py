"""FastAPI dependencies."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.constants import UserRole
from app.models.user import User


async def get_current_admin(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)) -> User:
    """Verify current user is admin."""
    user = db.query(User).filter(User.id == current_user.get("sub")).first()
    if not user or user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this resource"
        )
    return user


async def get_current_manager(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)) -> User:
    """Verify current user is manager."""
    user = db.query(User).filter(User.id == current_user.get("sub")).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can access this resource"
        )
    return user


async def get_current_trainer(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)) -> User:
    """Verify current user is trainer."""
    user = db.query(User).filter(User.id == current_user.get("sub")).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.TRAINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only trainers and admins can access this resource"
        )
    return user


async def get_current_staff(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)) -> User:
    """Verify current user is staff."""
    user = db.query(User).filter(User.id == current_user.get("sub")).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required"
        )
    return user
