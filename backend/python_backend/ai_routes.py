
import logging
from fastapi import APIRouter, Depends, HTTPException
from .dependencies import get_ai_engine, get_db
from .database import DatabaseManager
from .models import AIAnalysisRequest, AIAnalysisResponse, AICategorizeRequest, AICategorizeResponse, EmailResponse, AIValidateRequest, AIValidateResponse
from src.core.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/api/ai/analyze", response_model=AIAnalysisResponse)
async def analyze_email(
    request: AIAnalysisRequest,
    current_user: str = Depends(get_current_active_user),
    ai_engine: AdvancedAIEngine = Depends(get_ai_engine),
    db: DatabaseManager = Depends(get_db),
):
    """
    Analyzes email content and returns AI-driven insights.
    
    Requires authentication.
    """
    try:
        default_models = {
            "sentiment": "sentiment-default",
            "topic": "topic-default"
        }
        analysis_result = await ai_engine.analyze_email(
            subject=request.subject,
            content=request.content,
            models_to_use=default_models,
            db=db
        )
        return analysis_result.to_dict()
    except Exception as e:
        logger.error(f"Error in AI analysis endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to analyze email with AI.")

@router.post("/api/ai/categorize", response_model=AICategorizeResponse)
async def categorize_email(
    request: AICategorizeRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
    ai_engine: AdvancedAIEngine = Depends(get_ai_engine),
):
    """
    Categorizes an email, either automatically using AI or manually.
    
    Requires authentication.
    """
    email = await db.get_email_by_id(request.emailId)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    if request.autoAnalyze:
        try:
            default_models = {
                "sentiment": "sentiment-default",
                "topic": "topic-default"
            }
            analysis_result = await ai_engine.analyze_email(
                subject=email["subject"],
                content=email["content"],
                models_to_use=default_models,
                db=db
            )

            if analysis_result and analysis_result.category_id:
                updated_email_dict = await db.update_email(
                    request.emailId,
                    {
                        "categoryId": analysis_result.category_id,
                        "confidence": int(analysis_result.confidence * 100),
                        "labels": analysis_result.suggested_labels,
                    },
                )
                category = await db.get_category_by_id(analysis_result.category_id)
                return AICategorizeResponse(
                    success=True,
                    email=EmailResponse(**updated_email_dict),
                    analysis=AIAnalysisResponse(**analysis_result.to_dict()),
                    categoryAssigned=category["name"],
                )
            else:
                return AICategorizeResponse(
                    success=False,
                    message="AI analysis did not result in a category.",
                    analysis=AIAnalysisResponse(**analysis_result.to_dict()) if analysis_result else None,
                )
        except Exception as e:
            logger.error(f"Error in AI categorization: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to categorize email with AI.")
    else:
        if request.categoryId is None:
            raise HTTPException(status_code=400, detail="categoryId is required for manual categorization")
        
        update_data = {"categoryId": request.categoryId}
        if request.confidence is not None:
            update_data["confidence"] = request.confidence

        updated_email_dict = await db.update_email(request.emailId, update_data)
        category = await db.get_category_by_id(request.categoryId)
        return AICategorizeResponse(
            success=True, 
            email=EmailResponse(**updated_email_dict),
            categoryAssigned=category["name"],
        )

@router.post("/api/ai/validate", response_model=AIValidateResponse)
async def validate_analysis(
    request: AIValidateRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Validates AI analysis based on user feedback.
    
    Requires authentication.
    """
    logger.info(f"Received validation feedback for email {request.emailId}: {request.userFeedback}")

    if request.userFeedback == 'incorrect' and request.correctCategory:
        email = await db.get_email_by_id(request.emailId)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")

        # In a real application, you might want to find the category by name
        # For now, we assume the frontend sends a valid category ID or name
        # This is a simplified logic
        try:
            # Assuming correctCategory is a name, we need to find its ID
            # This is a simplified approach; a real implementation would need a more robust way to get all categories
            all_categories = await db.get_all_categories()
            category_id = None
            for cat in all_categories:
                if cat['name'].lower() == request.correctCategory.lower():
                    category_id = cat['id']
                    break
            
            if category_id:
                await db.update_email(request.emailId, {"categoryId": category_id, "confidence": 100})
                logger.info(f"Email {request.emailId} category updated to {request.correctCategory} (ID: {category_id}) based on user feedback.")
            else:
                logger.warning(f"Could not find category named '{request.correctCategory}' to update email {request.emailId}.")

        except Exception as e:
            logger.error(f"Error updating email category based on validation feedback: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to update email category.")

    # In a real application, this feedback would be stored and used for model retraining
    return AIValidateResponse(success=True, message="Feedback recorded successfully")
