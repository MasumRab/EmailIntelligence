import json
import logging
from typing import List

from fastapi import APIRouter, HTTPException, Request

from .ai_engine import AdvancedAIEngine
from .models import (ActionExtractionRequest,  # Changed from .main to .models
                     ActionItem)
from .performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)
router = APIRouter()
ai_engine = AdvancedAIEngine()  # Initialize AI engine
performance_monitor = PerformanceMonitor()  # Initialize performance monitor


@router.post("/api/actions/extract-from-text", response_model=List[ActionItem])
@performance_monitor.track
async def extract_actions_from_text(
    # Renamed to avoid conflict with Pydantic request model
    fastapi_req: Request,
    request_model: ActionExtractionRequest,
):
    """Extract action items from provided text (subject and content)"""
    try:
        # Ensure AI engine is initialized (if it has an async init method)
        # This might be better handled as a FastAPI dependency or at startup.
        # For now, let's assume ai_engine is ready or handles its state.
        # await ai_engine.initialize() # If needed and not already handled

        subject_log = request_model.subject[:50] if request_model.subject else "N/A"
        logger.info(f"Action extraction req for subject: '{subject_log}'")

        # Pass db=None as category matching is not essential for pure action extraction
        ai_analysis_result = await ai_engine.analyze_email(
            subject=request_model.subject or "",
            content=request_model.content,
            db=None,  # Category matching not essential for pure action extraction
        )

        # The AIAnalysisResult object should have an 'action_items' attribute
        action_items_data = ai_analysis_result.action_items

        # Convert the list of dicts to a list of ActionItem Pydantic models
        # This ensures the response conforms to the defined schema.
        act_items = [ActionItem(**item) for item in action_items_data]

        logger.info(f"Extracted {len(act_items)} actions.")
        return act_items

    except Exception as e:
        logger.error(
            json.dumps(
                {
                    "message": "Unhandled error in extract_actions_from_text",
                    "endpoint": str(fastapi_req.url),  # Use fastapi_req here
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
            )
        )
        # Consider specific error codes for different failure types if necessary
        detail_message = f"Failed to extract action items: {str(e)}"
        raise HTTPException(status_code=500, detail=detail_message)
