import json
import logging
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from googleapiclient.errors import HttpError as GoogleApiHttpError

# Corrected import path for GmailAIService
from ..python_nlp.gmail_service import GmailAIService
from .dependencies import get_gmail_service
from .exceptions import GmailServiceError
from .models import (
    GmailSyncRequest,
    SmartRetrievalRequest,
)  # Changed from .main to .models
from .performance_monitor import log_performance

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/gmail/sync")
@log_performance(operation="sync_gmail")
async def sync_gmail(
    req: Request,
    request_model: GmailSyncRequest,
    background_tasks: BackgroundTasks,
    gmail_service: GmailAIService = Depends(get_gmail_service),
):
    """
    Triggers a synchronization process to fetch emails from Gmail.

    This endpoint initiates a background task to fetch emails based on the
    provided criteria, perform AI analysis, and store them in the database.

    Args:
        req: The incoming request object.
        request_model: The request body containing sync parameters like max emails
                       and query filters.
        background_tasks: FastAPI's background task runner.

    Returns:
        A confirmation response indicating the sync process has started.

    Raises:
        HTTPException: If there is a Google API error or another unexpected failure.
    """
    try:
        nlp_result = await gmail_service.sync_gmail_emails(
            max_emails=request_model.maxEmails,
            query_filter=request_model.queryFilter,
            include_ai_analysis=request_model.includeAIAnalysis,
        )

        if nlp_result.get("success"):
            result = {
                "success": True,
                "processedCount": nlp_result.get("processed_count", 0),
                "emailsCreated": nlp_result.get("processed_count", 0),
                "errorsCount": 0,
                "batchInfo": {
                    "batchId": nlp_result.get("batch_info", {}).get(
                        "batch_id", f"batch_{int(datetime.now().timestamp())}"
                    ),
                    "queryFilter": request_model.queryFilter,
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
        except Exception:
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

        raise GmailServiceError(detail=detail, status_code=status_code)
    except Exception as e:
        log_data = {
            "message": "Unhandled error in sync_gmail",
            "endpoint": str(req.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))  # Added logger call
        raise GmailServiceError(
            detail=f"Gmail sync failed due to an unexpected error: {str(e)}",
        )


@router.post("/api/gmail/smart-retrieval")
@log_performance(operation="smart_retrieval")
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
        except Exception:
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

        raise GmailServiceError(detail=detail, status_code=status_code)
    except Exception as e:
        log_data = {
            "message": "Unhandled error in smart_retrieval",
            "endpoint": str(req.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))  # Added logger call
        raise GmailServiceError(
            detail=f"Smart retrieval failed due to an unexpected error: {str(e)}",
        )


@router.get("/api/gmail/strategies")
@log_performance(operation="get_retrieval_strategies")
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
        logger.error(json.dumps(log_data))  # Added logger call
        raise GmailServiceError(detail="Failed to fetch strategies")


@router.get("/api/gmail/performance")
@log_performance(operation="get_gmail_performance")
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
        logger.error(json.dumps(log_data))  # Added logger call
        raise GmailServiceError(detail="Failed to fetch performance metrics")
