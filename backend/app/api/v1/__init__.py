"""Application API routes initialization."""

from app.api.v1 import (
    auth_routes,
    member_routes,
    trainer_routes,
    attendance_routes,
    payment_routes,
    workout_routes,
    nutrition_routes,
    branch_routes,
    class_routes,
)

__all__ = [
    "auth_routes",
    "member_routes",
    "trainer_routes",
    "attendance_routes",
    "payment_routes",
    "workout_routes",
    "nutrition_routes",
    "branch_routes",
    "class_routes",
]
