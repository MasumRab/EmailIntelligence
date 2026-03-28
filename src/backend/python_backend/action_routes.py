"""
Action routes for backward compatibility.
The action functionality has been integrated into email_routes.
"""
import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/actions/health")
async def health_check():
    """Health check endpoint for action routes."""
    return {"status": "ok", "message": "Action routes are deprecated. Use email routes instead."}


@router.post("/api/actions/extract")
async def extract_actions_placeholder():
    """
    Placeholder endpoint for action extraction.
    The action extraction functionality has been moved to email_routes.
    """
    raise HTTPException(
        status_code=410,
        detail="This endpoint is deprecated. Use email analysis endpoints instead."
    )