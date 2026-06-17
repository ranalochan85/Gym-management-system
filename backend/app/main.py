"""Main application file."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
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
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Cleanup on shutdown
    print("👋 Application shutdown")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Comprehensive Gym Management System",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME
    }


# Include routers
app.include_router(auth_routes.router)
app.include_router(member_routes.router)
app.include_router(trainer_routes.router)
app.include_router(attendance_routes.router)
app.include_router(payment_routes.router)
app.include_router(workout_routes.router)
app.include_router(nutrition_routes.router)
app.include_router(branch_routes.router)
app.include_router(class_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
