import json
import logging
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from googleapiclient.errors import HttpError as GoogleApiHttpError

# Corrected import path for GmailAIService
from ..python_nlp.gmail_service import GmailAIService

from .ai_engine import AdvancedAIEngine
from .database import DatabaseManager, get_db
from .dependencies import get_gmail_service
from .performance_monitor import performance_monitor
from .models import GmailSyncRequest, SmartRetrievalRequest  # Changed from .main to .models

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/gmail/sync")
@performance_monitor.track
async def sync_gmail(
    req: Request,  # Renamed to req to avoid conflict with request model
    request_model: GmailSyncRequest,  # Renamed model
    background_tasks: BackgroundTasks,
    gmail_service: GmailAIService = Depends(get_gmail_service),
):
    """Sync emails from Gmail with AI analysis"""
    try:
        # Call the NLP service's sync_gmail_emails method directly
        # Note: sync_gmail_emails does not use `strategies` or
        # `time_budget_minutes` from GmailSyncRequest.
        nlp_result = await gmail_service.sync_gmail_emails(
            max_emails=request_model.maxEmails,
            query_filter=request_model.queryFilter,
            include_ai_analysis=request_model.includeAIAnalysis,
        )

        # Adapt NLP result to BackendGS expected format
        if nlp_result.get("success"):
            result = {
                "success": True,
                "processedCount": nlp_result.get("processed_count", 0),
                "emailsCreated": nlp_result.get("processed_count", 0),  # Approximation
                "errorsCount": 0,
                "batchInfo": {
                    "batchId": nlp_result.get("batch_info", {}).get(
                        "batch_id", f"batch_{int(datetime.now().timestamp())}"
                    ),
                    "queryFilter": request_model.queryFilter,  # Use the original request's query_filter
                    "timestamp": nlp_result.get("batch_info", {}).get(
                        "timestamp", datetime.now().isoformat()
                    ),
                },
                "statistics": nlp_result.get("statistics", {}),
                "error": None,
            }
        else:
            result = {
                "success": False,
                "processedCount": 0,
                "emailsCreated": 0,
                "errorsCount": 1,
                "batchInfo": {
                    "batchId": f"error_batch_{int(datetime.now().timestamp())}",
                    "queryFilter": request_model.queryFilter,
                    "timestamp": datetime.now().isoformat(),
                },
                "statistics": nlp_result.get("statistics", {}),
                "error": nlp_result.get("error", "Unknown NLP error"),
            }

        return result
    except GoogleApiHttpError as gmail_err:
        error_details_dict = {}
        try:
            error_details_dict = json.loads(gmail_err.content.decode())
        except Exception:  # Broad except for decoding issues
            error_details_dict = {"message": "Failed to decode Gmail error content."}

        error_content = error_details_dict.get("error", {})
        error_detail_message = str(gmail_err)
        if isinstance(error_content, dict):
            error_detail_message = error_content.get("message", str(gmail_err))
        elif isinstance(error_content, str):
            error_detail_message = error_content

        log_data = {
            "message": "Gmail API operation failed during sync",
            "endpoint": str(req.url),
            "error_type": type(gmail_err).__name__,
            "error_detail": error_detail_message,
            "gmail_status_code": getattr(gmail_err.resp, "status", None),
            "full_gmail_error": error_details_dict,
        }
        logger.error(json.dumps(log_data))

        status_code = getattr(gmail_err.resp, "status", 502)
        detail = "Gmail API error during sync."
        if status_code == 401:
            detail = "Gmail API authentication failed. Check credentials."
        elif status_code == 403:
            detail = "Gmail API permission denied. Check API scopes."
        elif status_code == 429:
            detail = "Gmail API rate limit exceeded. Try again later."
        else:
            status_code = 502
            detail = "Gmail API returned an unexpected error. Try again."

        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        log_data = {
            "message": "Unhandled error in sync_gmail",
            "endpoint": str(req.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(
            status_code=500,
            detail=f"Gmail sync failed due to an unexpected error: {str(e)}",
        )


@router.post("/api/gmail/smart-retrieval")
@performance_monitor.track
async def smart_retrieval(
    req: Request,
    request_model: SmartRetrievalRequest,
    gmail_service: GmailAIService = Depends(get_gmail_service),
):  # Renamed params
    """Execute smart Gmail retrieval with multiple strategies"""
    try:
        result = await gmail_service.execute_smart_retrieval(
            strategies=request_model.strategies,
            max_api_calls=request_model.maxApiCalls,
            time_budget_minutes=request_model.timeBudgetMinutes,
        )
        return result
    except GoogleApiHttpError as gmail_err:
        error_details_dict = {}
        try:
            error_details_dict = json.loads(gmail_err.content.decode())
        except Exception:  # Broad except for decoding issues
            error_details_dict = {"message": "Failed to decode Gmail error content."}

        error_content = error_details_dict.get("error", {})
        error_detail_message = str(gmail_err)
        if isinstance(error_content, dict):
            error_detail_message = error_content.get("message", str(gmail_err))
        elif isinstance(error_content, str):
            error_detail_message = error_content

        log_data = {
            "message": "Gmail API operation failed during smart retrieval",
            "endpoint": str(req.url),
            "error_type": type(gmail_err).__name__,
            "error_detail": error_detail_message,
            "gmail_status_code": getattr(gmail_err.resp, "status", None),
            "full_gmail_error": error_details_dict,
        }
        logger.error(json.dumps(log_data))

        status_code = getattr(gmail_err.resp, "status", 502)
        detail = "Gmail API error during smart retrieval."
        if status_code == 401:
            detail = "Gmail API authentication failed. Check credentials."
        elif status_code == 403:
            detail = "Gmail API permission denied. Check API scopes."
        elif status_code == 429:
            detail = "Gmail API rate limit exceeded. Try again later."
        else:
            status_code = 502
            detail = "Gmail API returned an unexpected error for smart retrieval."

        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        log_data = {
            "message": "Unhandled error in smart_retrieval",
            "endpoint": str(req.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(
            status_code=500,
            detail=f"Smart retrieval failed due to an unexpected error: {str(e)}",
        )


@router.get("/api/gmail/strategies")
@performance_monitor.track
async def get_retrieval_strategies(
    request: Request, gmail_service: GmailAIService = Depends(get_gmail_service)
):
    """Get available Gmail retrieval strategies"""
    try:
        strategies = await gmail_service.get_retrieval_strategies()
        return {"strategies": strategies}
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_retrieval_strategies",
                    "endpoint": str(request.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(status_code=500, detail="Failed to fetch strategies")


@router.get("/api/gmail/performance")
@performance_monitor.track
async def get_gmail_performance(
    request: Request, gmail_service: GmailAIService = Depends(get_gmail_service)
):
    """Get Gmail API performance metrics"""
    try:
        metrics = await gmail_service.get_performance_metrics()
        return metrics or {"status": "no_data"}
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_gmail_performance",
                    "endpoint": str(request.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(
            status_code=500, detail="Failed to fetch performance metrics"
        )