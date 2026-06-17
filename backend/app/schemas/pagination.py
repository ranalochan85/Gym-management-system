"""Pagination schemas."""

from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List, Any

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    search: str = Field(None, min_length=1)
    sort_by: str = None
    sort_order: str = "asc"


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[T]

    class Config:
        from_attributes = True
