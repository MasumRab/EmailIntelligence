import json
import logging
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from googleapiclient.errors import HttpError as GoogleApiHttpError

# Corrected import path for GmailAIService
from server.python_nlp.gmail_service import GmailAIService

from .ai_engine import AdvancedAIEngine  # Import AdvancedAIEngine
from .database import DatabaseManager  # Import DatabaseManager
from .models import (GmailSyncRequest,  # Changed from .main to .models
                     SmartRetrievalRequest)
from .performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)
router = APIRouter()
# Instantiate services with necessary dependencies
# This assumes DatabaseManager() and AdvancedAIEngine() can be
# instantiated simply here. If complex setup, use FastAPI Depends or factory.
db_manager_for_gmail_service = DatabaseManager()
ai_engine_for_gmail_service = AdvancedAIEngine()
gmail_service = GmailAIService(
    db_manager=db_manager_for_gmail_service,
    advanced_ai_engine=ai_engine_for_gmail_service,
)
performance_monitor = PerformanceMonitor()


@router.post("/api/gmail/sync")
@performance_monitor.track
async def sync_gmail(
    req: Request,  # Renamed to req to avoid conflict with request model
    request_model: GmailSyncRequest,  # Renamed model
    background_tasks: BackgroundTasks,
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
                        "timestamp", datetime.now().isoformat()),
                },
                "statistics": nlp_result.get("statistics", {}),
                "error": None,
            }
        else:
            result = {
                "success": False, "processedCount": 0, "emailsCreated": 0,
                "errorsCount": 1,
                "batchInfo": {
                    "batchId": f"error_batch_{int(datetime.now().timestamp())}",
                    "queryFilter": request_model.queryFilter,
                    "timestamp": datetime.now().isoformat(),
                },
                "statistics": nlp_result.get("statistics", {}),
                "error": nlp_result.get("error", "Unknown NLP error"),
            }

        # Background performance monitoring
        background_tasks.add_task(performance_monitor.record_sync_performance, result)

        return result
    except GoogleApiHttpError as gmail_err:
        error_details_dict = {}
        try:
            error_details_dict = json.loads(gmail_err.content.decode())
        except Exception:  # Broad except for decoding issues
            error_details_dict = {"message": "Failed to decode Gmail error content."}

        log_data = {
            "message": "Gmail API operation failed during sync",
            "endpoint": str(req.url),
            "error_type": type(gmail_err).__name__,
            "error_detail": error_details_dict.get("error", {}).get(
                "message", str(gmail_err)
            ),
            "gmail_status_code": getattr(gmail_err.resp, 'status', None),
            "full_gmail_error": error_details_dict,
        }
        logger.error(json.dumps(log_data))

        status_code = getattr(gmail_err.resp, 'status', 502)
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
            )
        )
        raise HTTPException(
            status_code=500,
            detail=f"Gmail sync failed due to an unexpected error: {str(e)}",
        )


@router.post("/api/gmail/smart-retrieval")
@performance_monitor.track
async def smart_retrieval(
    req: Request, request_model: SmartRetrievalRequest
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

        log_data = {
            "message": "Gmail API operation failed during smart retrieval",
            "endpoint": str(req.url),
            "error_type": type(gmail_err).__name__,
            "error_detail": error_details_dict.get("error", {}).get(
                "message", str(gmail_err)
            ),
            "gmail_status_code": getattr(gmail_err.resp, 'status', None),
            "full_gmail_error": error_details_dict,
        }
        logger.error(json.dumps(log_data))

        status_code = getattr(gmail_err.resp, 'status', 502)
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
            )
        )
        raise HTTPException(
            status_code=500,
            detail=f"Smart retrieval failed due to an unexpected error: {str(e)}",
        )


@router.get("/api/gmail/strategies")
@performance_monitor.track
async def get_retrieval_strategies(request: Request):
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
            )
        )
        raise HTTPException(status_code=500, detail="Failed to fetch strategies")


@router.get("/api/gmail/performance")
@performance_monitor.track
async def get_gmail_performance(request: Request):
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
            )
        )
        raise HTTPException(
            status_code=500, detail="Failed to fetch performance metrics"
        )
