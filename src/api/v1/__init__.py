"""
API v1 router for Email Intelligence Platform
Combines all v1 routes into a single router
"""

from fastapi import APIRouter

from .email_routes import router as email_router
from .category_routes import router as category_router

# Create main v1 router
router = APIRouter(prefix="/api/v1")

# Include all v1 routes
router.include_router(email_router)
router.include_router(category_router)

__all__ = ["router"]