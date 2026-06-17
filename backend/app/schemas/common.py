"""Common/shared schemas."""

from pydantic import BaseModel
from typing import Any, Optional


class SuccessResponse(BaseModel):
    """Success response schema."""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None


class HealthCheck(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    database: str = "connected"
