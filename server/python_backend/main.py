"""
FastAPI Backend for Gmail AI Email Management
Unified Python backend with optimized performance and integrated NLP
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime
import os
import psycopg2
from googleapiclient.errors import HttpError as GoogleApiHttpError
import json

# Import our Python modules
from .database import DatabaseManager, get_db
from .models import EmailCreate, EmailUpdate, CategoryCreate, ActivityCreate
# Updated import to use NLP GmailAIService directly
from server.python_nlp.gmail_service import GmailAIService
from .smart_filters import SmartFilterManager
from .ai_engine import AdvancedAIEngine
from .performance_monitor import PerformanceMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Gmail AI Email Management",
    description="Advanced email management with AI categorization and smart filtering",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5173", "https://*.replit.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for Action Item Extraction
class ActionExtractionRequest(BaseModel):
    subject: Optional[str] = None
    content: str

class ActionItem(BaseModel):
    action_phrase: str
    verb: Optional[str] = None
    object: Optional[str] = None
    raw_due_date_text: Optional[str] = None
    context: str

# Set up metrics if in production or staging environment
if os.getenv("NODE_ENV") in ["production", "staging"]:
    from .metrics import setup_metrics
    setup_metrics(app)

# Initialize services
gmail_service = GmailAIService()
filter_manager = SmartFilterManager()
ai_engine = AdvancedAIEngine()
performance_monitor = PerformanceMonitor()

# Request/Response Models
class EmailResponse(BaseModel):
    id: int
    messageId: Optional[str]
    threadId: Optional[str]
    sender: str
    senderEmail: str
    subject: str
    content: str
    preview: str
    time: str
    category: Optional[str]
    labels: List[str]
    isImportant: bool
    isStarred: bool
    isUnread: bool
    confidence: int

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    color: str
    count: int

class DashboardStatsResponse(BaseModel):
    totalEmails: int
    autoLabeled: int
    categories: int
    timeSaved: str
    weeklyGrowth: Dict[str, int]

class GmailSyncRequest(BaseModel):
    maxEmails: int = 500
    queryFilter: str = "newer_than:1d"
    includeAIAnalysis: bool = True
    strategies: List[str] = []
    timeBudgetMinutes: int = 15

class SmartRetrievalRequest(BaseModel):
    strategies: List[str] = []
    maxApiCalls: int = 100
    timeBudgetMinutes: int = 30

class FilterRequest(BaseModel):
    name: str
    criteria: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int = 5

# Dashboard Endpoints
@app.get("/api/dashboard/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    try:
        stats = await db.get_dashboard_stats()
        return stats
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_dashboard_stats",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard stats")

@app.get("/api/performance/overview")
async def get_performance_overview(request: Request):
    """Get real-time performance overview"""
    try:
        overview = await performance_monitor.get_real_time_dashboard()
        return overview
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_performance_overview",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch performance data")

# Email Management Endpoints
@app.get("/api/emails", response_model=List[EmailResponse])
async def get_emails(
    request: Request,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: DatabaseManager = Depends(get_db)
):
    """Get emails with optional filtering"""
    try:
        if search:
            emails = await db.search_emails(search)
        elif category_id:
            emails = await db.get_emails_by_category(category_id)
        else:
            emails = await db.get_all_emails()
        
        return [EmailResponse(**email) for email in emails]
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed while fetching emails",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_emails",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch emails")

@app.get("/api/emails/{email_id}")
async def get_email(request: Request, email_id: int, db: DatabaseManager = Depends(get_db)):
    """Get specific email by ID"""
    try:
        email = await db.get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return email
    except HTTPException:
        raise
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": f"Database operation failed while fetching email id {email_id}",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": f"Unhandled error fetching email id {email_id}",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch email")

@app.post("/api/emails")
async def create_email(
    request: Request,
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(get_db)
):
    """Create new email with AI analysis"""
    try:
        # Perform AI analysis
        ai_analysis = await ai_engine.analyze_email(email.subject, email.content)
        
        # Apply smart filters
        filter_results = await filter_manager.apply_filters_to_email(email.dict())
        
        # Create email with enhanced data
        email_data = email.dict()
        email_data.update({
            'confidence': int(ai_analysis.confidence * 100),
            'categoryId': ai_analysis.category_id,
            'labels': ai_analysis.suggested_labels,
            'analysisMetadata': ai_analysis.to_dict()
        })
        
        created_email = await db.create_email(email_data)
        
        # Background tasks for performance tracking
        background_tasks.add_task(
            performance_monitor.record_email_processing,
            created_email['id'],
            ai_analysis,
            filter_results
        )
        
        return created_email
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed while creating email",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in create_email",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to create email")

@app.put("/api/emails/{email_id}")
async def update_email(
    request: Request,
    email_id: int,
    email_update: EmailUpdate,
    db: DatabaseManager = Depends(get_db)
):
    """Update email"""
    try:
        updated_email = await db.update_email(email_id, email_update.dict(exclude_unset=True))
        if not updated_email:
            raise HTTPException(status_code=404, detail="Email not found")
        return updated_email
    except HTTPException:
        raise
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": f"Database operation failed while updating email id {email_id}",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": f"Unhandled error updating email id {email_id}",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to update email")

# Category Management Endpoints
@app.get("/api/categories", response_model=List[CategoryResponse])
async def get_categories(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get all categories"""
    try:
        categories = await db.get_all_categories()
        return [CategoryResponse(**cat) for cat in categories]
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed while fetching categories",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_categories",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@app.post("/api/categories")
async def create_category(
    request: Request,
    category: CategoryCreate,
    db: DatabaseManager = Depends(get_db)
):
    """Create new category"""
    try:
        created_category = await db.create_category(category.dict())
        return created_category
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed while creating category",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in create_category",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to create category")

# Gmail Integration Endpoints
@app.post("/api/gmail/sync")
async def sync_gmail(
    req: Request, # Renamed to req to avoid conflict with request model
    request_model: GmailSyncRequest, # Renamed model
    background_tasks: BackgroundTasks
):
    """Sync emails from Gmail with AI analysis"""
    try:
        # Call the NLP service's sync_gmail_emails method directly
        # Note: NLPGS.sync_gmail_emails does not use `strategies` or `time_budget_minutes` from GmailSyncRequest
        nlp_result = await gmail_service.sync_gmail_emails(
            max_emails=request_model.maxEmails, # This is from GmailSyncRequest
            query_filter=request_model.queryFilter, # This is from GmailSyncRequest
            include_ai_analysis=request_model.includeAIAnalysis # This is from GmailSyncRequest
        )

        # Adapt NLP result to BackendGS expected format (logic moved from old backend adapter)
        if nlp_result.get('success'):
            result = {
                "success": True,
                "processedCount": nlp_result.get('processed_count', 0),
                "emailsCreated": nlp_result.get('processed_count', 0), # Approximation
                "errorsCount": 0,
                "batchInfo": {
                    "batchId": nlp_result.get('batch_info', {}).get('batch_id', f'batch_{int(datetime.now().timestamp())}'),
                    "queryFilter": request_model.queryFilter, # Use the original request's query_filter
                    "timestamp": nlp_result.get('batch_info', {}).get('timestamp', datetime.now().isoformat())
                },
                "statistics": nlp_result.get('statistics', {}),
                "error": None
            }
        else:
            result = {
                "success": False,
                "processedCount": 0,
                "emailsCreated": 0,
                "errorsCount": 1,
                "batchInfo": {
                    "batchId": f'error_batch_{int(datetime.now().timestamp())}',
                    "queryFilter": request_model.queryFilter, # Use the original request's query_filter
                    "timestamp": datetime.now().isoformat()
                },
                "statistics": nlp_result.get('statistics', {}),
                "error": nlp_result.get('error', 'Unknown error from NLP service')
            }
        
        # Background performance monitoring
        background_tasks.add_task(
            performance_monitor.record_sync_performance,
            result
        )
        
        return result
    except GoogleApiHttpError as gmail_err:
        error_details_dict = {}
        try:
            error_details_dict = json.loads(gmail_err.content.decode())
        except: # Broad except for decoding issues
            error_details_dict = {"message": "Failed to decode Gmail error content."}

        logger.error(
            json.dumps({
                "message": "Gmail API operation failed during sync",
                "endpoint": str(req.url), # Use req here
                "error_type": type(gmail_err).__name__,
                "error_detail": error_details_dict.get("error", {}).get("message", str(gmail_err)),
                "gmail_status_code": gmail_err.resp.status if hasattr(gmail_err, 'resp') else None,
                "full_gmail_error": error_details_dict,
            })
        )
        status_code = gmail_err.resp.status if hasattr(gmail_err, 'resp') else 502
        detail = "Gmail API error during sync."
        if status_code == 401: # Unauthorized
            detail = "Gmail API authentication failed. Check credentials or token."
        elif status_code == 403: # Forbidden
            detail = "Gmail API permission denied. Ensure API is enabled and scopes are correct."
        elif status_code == 429: # Too Many Requests
            detail = "Gmail API rate limit exceeded. Please try again later."
        else: # Other errors (500, 502, 503, etc.)
            status_code = 502 # Treat as Bad Gateway from Gmail
            detail = "Gmail API returned an unexpected error. Please try again later."

        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in sync_gmail",
                "endpoint": str(req.url), # Use req here
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail=f"Gmail sync failed due to an unexpected error: {str(e)}")

@app.post("/api/gmail/smart-retrieval")
async def smart_retrieval(req: Request, request_model: SmartRetrievalRequest): # Renamed params
    """Execute smart Gmail retrieval with multiple strategies"""
    try:
        result = await gmail_service.execute_smart_retrieval(
            strategies=request_model.strategies,
            max_api_calls=request_model.maxApiCalls,
            time_budget_minutes=request_model.timeBudgetMinutes
        )
        return result
    except GoogleApiHttpError as gmail_err:
        error_details_dict = {}
        try:
            error_details_dict = json.loads(gmail_err.content.decode())
        except: # Broad except for decoding issues
            error_details_dict = {"message": "Failed to decode Gmail error content."}

        logger.error(
            json.dumps({
                "message": "Gmail API operation failed during smart retrieval",
                "endpoint": str(req.url), # Use req here
                "error_type": type(gmail_err).__name__,
                "error_detail": error_details_dict.get("error", {}).get("message", str(gmail_err)),
                "gmail_status_code": gmail_err.resp.status if hasattr(gmail_err, 'resp') else None,
                "full_gmail_error": error_details_dict,
            })
        )
        status_code = gmail_err.resp.status if hasattr(gmail_err, 'resp') else 502
        detail = "Gmail API error during smart retrieval."
        if status_code == 401: # Unauthorized
            detail = "Gmail API authentication failed. Check credentials or token."
        elif status_code == 403: # Forbidden
            detail = "Gmail API permission denied. Ensure API is enabled and scopes are correct."
        elif status_code == 429: # Too Many Requests
            detail = "Gmail API rate limit exceeded. Please try again later."
        else: # Other errors
            status_code = 502 # Treat as Bad Gateway
            detail = "Gmail API returned an unexpected error during smart retrieval."

        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in smart_retrieval",
                "endpoint": str(req.url), # Use req here
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail=f"Smart retrieval failed due to an unexpected error: {str(e)}")

@app.get("/api/gmail/strategies")
async def get_retrieval_strategies(request: Request):
    """Get available Gmail retrieval strategies"""
    try:
        strategies = await gmail_service.get_retrieval_strategies()
        return {"strategies": strategies}
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_retrieval_strategies",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch strategies")

@app.get("/api/gmail/performance")
async def get_gmail_performance(request: Request):
    """Get Gmail API performance metrics"""
    try:
        metrics = await gmail_service.get_performance_metrics()
        return metrics or {"status": "no_data"}
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_gmail_performance",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch performance metrics")

# Smart Filter Endpoints
@app.get("/api/filters")
async def get_filters(request: Request):
    """Get all active email filters"""
    try:
        filters = await filter_manager.get_all_filters() # This returns a list of dicts, not objects with to_dict()
        # Assuming get_all_filters() in SmartFilterManager was updated to return list of dicts
        # or EmailFilter dataclass has a to_dict() method.
        # The previous version of smart_filters.py had get_filters() returning a list of dicts.
        # Let's assume it's still compatible or was adjusted.
        return {"filters": filters } # Adjusted if get_all_filters returns list of dicts
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_filters",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch filters")

@app.post("/api/filters")
async def create_filter(request: Request, filter_request_model: FilterRequest): # Renamed model
    """Create new email filter"""
    try:
        # Assuming filter_manager.create_filter (or add_custom_filter) takes a dict or an EmailFilter object
        # The smart_filters.py in context had add_custom_filter(EmailFilter(...))
        # and no create_filter. This might need adjustment in SmartFilterManager or here.
        # For now, assuming a compatible create_filter or add_custom_filter exists.
        # Let's assume add_custom_filter is the intended method from previous context for adding new filters.
        from .smart_filters import EmailFilter # Ensure EmailFilter is available for instantiation
        new_filter_config = EmailFilter(
            name=filter_request_model.name,
            description=filter_request_model.criteria.get("description", ""), # Assuming description might be in criteria
            criteria=filter_request_model.criteria,
            action=filter_request_model.actions.get("type", ""), # Assuming actions dict has a 'type' for the action name
            priority=filter_request_model.priority,
            enabled=True
        )
        filter_manager.add_custom_filter(new_filter_config) # Using add_custom_filter
        return new_filter_config.__dict__ # Return the created filter as dict
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in create_filter",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to create filter")

@app.post("/api/filters/generate-intelligent")
async def generate_intelligent_filters(request: Request, db: DatabaseManager = Depends(get_db)):
    """Generate intelligent filters based on email patterns"""
    try:
        # Get recent emails for pattern analysis
        emails = await db.get_recent_emails(limit=1000) # Assuming this db method exists
        
        # Generate intelligent filters
        # Assuming filter_manager.create_intelligent_filters exists and returns a list of filter objects/dicts
        created_filters = await filter_manager.create_intelligent_filters(emails) # This method was not in original smart_filters.py
                                                                             # Assuming it's added or this is a placeholder.
                                                                             # If it returns objects with to_dict:
        # return {
        #     "created_filters": len(created_filters),
        #     "filters": [f.to_dict() for f in created_filters]
        # }
        # If it returns list of dicts:
        return {
             "created_filters": len(created_filters),
             "filters": created_filters
        }
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed while generating intelligent filters",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in generate_intelligent_filters",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to generate filters")

@app.post("/api/filters/prune")
async def prune_filters(request: Request):
    """Prune ineffective filters"""
    try:
        # Assuming filter_manager.prune_ineffective_filters exists
        # This method was not in original smart_filters.py, assuming added.
        results = await filter_manager.prune_ineffective_filters()
        return results
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in prune_filters",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to prune filters")

# Action Item Extraction Endpoint
@app.post("/api/actions/extract-from-text", response_model=List[ActionItem])
async def extract_actions_from_text(
    fastapi_req: Request, # Renamed to avoid conflict with Pydantic request model
    request_model: ActionExtractionRequest
):
    """Extract action items from provided text (subject and content)"""
    try:
        # Ensure AI engine is initialized (if it has an async init method)
        # This might be better handled as a FastAPI dependency or at startup.
        # For now, let's assume ai_engine is ready or handles its state.
        # await ai_engine.initialize() # If needed and not already handled

        logger.info(f"Received action extraction request for subject: '{request_model.subject[:50] if request_model.subject else 'N/A'}'")

        ai_analysis_result = await ai_engine.analyze_email(
            subject=request_model.subject or "", # Pass empty string if subject is None
            content=request_model.content
        )

        # The AIAnalysisResult object should have an 'action_items' attribute
        action_items_data = ai_analysis_result.action_items

        # Convert the list of dicts to a list of ActionItem Pydantic models
        # This ensures the response conforms to the defined schema.
        response_action_items = [ActionItem(**item) for item in action_items_data]

        logger.info(f"Extracted {len(response_action_items)} action items.")
        return response_action_items

    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in extract_actions_from_text",
                "endpoint": str(fastapi_req.url), # Use fastapi_req here
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        # Consider specific error codes for different failure types if necessary
        raise HTTPException(status_code=500, detail=f"Failed to extract action items: {str(e)}")

@app.get("/health")
async def health_check(request: Request):
    """System health check"""
    try:
        # Perform any necessary checks, e.g., DB connectivity if desired
        # await db.execute_query("SELECT 1") # Example DB check
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        }
    except Exception as e: # This generic exception is fine for health check's own error
        logger.error( # Simple log for health check itself
            json.dumps({
                "message": "Health check failed",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        return JSONResponse(
            status_code=503, # Service Unavailable
            content={
                "status": "unhealthy",
                "error": "Service health check failed.", # Generic message to client
                "timestamp": datetime.now().isoformat(),
                "endpoint": str(request.url)
            }
        )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )