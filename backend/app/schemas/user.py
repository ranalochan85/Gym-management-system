"""User schemas."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.core.constants import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.MEMBER


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    role: UserRole
    is_active: bool
    is_email_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class PasswordChange(BaseModel):
    """Password change schema."""
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str


class PasswordReset(BaseModel):
    """Password reset schema."""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
