"""
API Routes for AI Engine.

This module provides FastAPI routes for AI-driven email analysis,
including sentiment analysis, topic classification, and categorization.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException

from .auth import get_current_active_user
from .ai_engine import get_active_ai_engine
from .models import AIAnalysisRequest, AIAnalysisResponse, AICategorizeRequest, AICategorizeResponse

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ai", tags=["AI Engine"])


@router.post("/analyze", response_model=AIAnalysisResponse)
async def analyze_email(
    request: AIAnalysisRequest,
    current_user: str = Depends(get_current_active_user)
):
    """
    Analyzes email content and returns AI-driven insights.
    Requires authentication.
    """
    try:
        ai_engine = get_active_ai_engine()
        if not ai_engine:
            raise HTTPException(status_code=503, detail="AI engine not available")
            
        analysis_result = await ai_engine.analyze_email(
            subject=request.subject,
            content=request.content,
            models=request.models if request.models else {}
        )
        
        return AIAnalysisResponse(**analysis_result.to_dict())
    except Exception as e:
        logger.error(f"Error during email analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze email")


@router.post("/categorize", response_model=AICategorizeResponse)
async def categorize_email(
    request: AICategorizeRequest,
    current_user: str = Depends(get_current_active_user)
):
    """
    Categorizes an email using AI analysis.
    Requires authentication.
    """
    try:
        ai_engine = get_active_ai_engine()
        if not ai_engine:
            raise HTTPException(status_code=503, detail="AI engine not available")
            
        categorization_result = await ai_engine.categorize_email(
            subject=request.subject,
            content=request.content
        )
        
        return AICategorizeResponse(**categorization_result)
    except Exception as e:
        logger.error(f"Error during email categorization: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to categorize email")


@router.post("/validate")
async def validate_ai_models(
    current_user: str = Depends(get_current_active_user)
):
    """
    Validates the status and performance of AI models.
    Requires authentication.
    """
    try:
        ai_engine = get_active_ai_engine()
        if not ai_engine:
            raise HTTPException(status_code=503, detail="AI engine not available")
            
        validation_result = await ai_engine.validate_models()
        return validation_result
    except Exception as e:
        logger.error(f"Error during AI model validation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to validate AI models")