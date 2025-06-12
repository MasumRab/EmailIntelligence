"""
FastAPI Backend for Gmail AI Email Management
Unified Python backend with optimized performance and integrated NLP
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime
import os

# Import our Python modules
from .database import DatabaseManager, get_db
from .models import EmailCreate, EmailUpdate, CategoryCreate, ActivityCreate
from .gmail_service import GmailAIService
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
    allow_origins=["http://localhost:5000", "https://*.replit.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def get_dashboard_stats(db: DatabaseManager = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    try:
        stats = await db.get_dashboard_stats()
        return stats
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard stats")

@app.get("/api/performance/overview")
async def get_performance_overview():
    """Get real-time performance overview"""
    try:
        overview = await performance_monitor.get_real_time_dashboard()
        return overview
    except Exception as e:
        logger.error(f"Error fetching performance overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch performance data")

# Email Management Endpoints
@app.get("/api/emails", response_model=List[EmailResponse])
async def get_emails(
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
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch emails")

@app.get("/api/emails/{email_id}")
async def get_email(email_id: int, db: DatabaseManager = Depends(get_db)):
    """Get specific email by ID"""
    try:
        email = await db.get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return email
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching email {email_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch email")

@app.post("/api/emails")
async def create_email(
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
    except Exception as e:
        logger.error(f"Error creating email: {e}")
        raise HTTPException(status_code=500, detail="Failed to create email")

@app.put("/api/emails/{email_id}")
async def update_email(
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
    except Exception as e:
        logger.error(f"Error updating email {email_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update email")

# Category Management Endpoints
@app.get("/api/categories", response_model=List[CategoryResponse])
async def get_categories(db: DatabaseManager = Depends(get_db)):
    """Get all categories"""
    try:
        categories = await db.get_all_categories()
        return [CategoryResponse(**cat) for cat in categories]
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@app.post("/api/categories")
async def create_category(
    category: CategoryCreate,
    db: DatabaseManager = Depends(get_db)
):
    """Create new category"""
    try:
        created_category = await db.create_category(category.dict())
        return created_category
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create category")

# Gmail Integration Endpoints
@app.post("/api/gmail/sync")
async def sync_gmail(
    request: GmailSyncRequest,
    background_tasks: BackgroundTasks
):
    """Sync emails from Gmail with AI analysis"""
    try:
        result = await gmail_service.sync_gmail_emails(
            max_emails=request.maxEmails,
            query_filter=request.queryFilter,
            include_ai_analysis=request.includeAIAnalysis,
            strategies=request.strategies,
            time_budget_minutes=request.timeBudgetMinutes
        )
        
        # Background performance monitoring
        background_tasks.add_task(
            performance_monitor.record_sync_performance,
            result
        )
        
        return result
    except Exception as e:
        logger.error(f"Gmail sync failed: {e}")
        raise HTTPException(status_code=500, detail=f"Gmail sync failed: {str(e)}")

@app.post("/api/gmail/smart-retrieval")
async def smart_retrieval(request: SmartRetrievalRequest):
    """Execute smart Gmail retrieval with multiple strategies"""
    try:
        result = await gmail_service.execute_smart_retrieval(
            strategies=request.strategies,
            max_api_calls=request.maxApiCalls,
            time_budget_minutes=request.timeBudgetMinutes
        )
        return result
    except Exception as e:
        logger.error(f"Smart retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Smart retrieval failed: {str(e)}")

@app.get("/api/gmail/strategies")
async def get_retrieval_strategies():
    """Get available Gmail retrieval strategies"""
    try:
        strategies = await gmail_service.get_retrieval_strategies()
        return {"strategies": strategies}
    except Exception as e:
        logger.error(f"Error fetching strategies: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch strategies")

@app.get("/api/gmail/performance")
async def get_gmail_performance():
    """Get Gmail API performance metrics"""
    try:
        metrics = await gmail_service.get_performance_metrics()
        return metrics or {"status": "no_data"}
    except Exception as e:
        logger.error(f"Error fetching Gmail performance: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch performance metrics")

# Smart Filter Endpoints
@app.get("/api/filters")
async def get_filters():
    """Get all active email filters"""
    try:
        filters = await filter_manager.get_all_filters()
        return {"filters": [filter_obj.to_dict() for filter_obj in filters]}
    except Exception as e:
        logger.error(f"Error fetching filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch filters")

@app.post("/api/filters")
async def create_filter(filter_request: FilterRequest):
    """Create new email filter"""
    try:
        filter_obj = await filter_manager.create_filter(
            name=filter_request.name,
            criteria=filter_request.criteria,
            actions=filter_request.actions,
            priority=filter_request.priority
        )
        return filter_obj.to_dict()
    except Exception as e:
        logger.error(f"Error creating filter: {e}")
        raise HTTPException(status_code=500, detail="Failed to create filter")

@app.post("/api/filters/generate-intelligent")
async def generate_intelligent_filters(db: DatabaseManager = Depends(get_db)):
    """Generate intelligent filters based on email patterns"""
    try:
        # Get recent emails for pattern analysis
        emails = await db.get_recent_emails(limit=1000)
        
        # Generate intelligent filters
        filters = await filter_manager.create_intelligent_filters(emails)
        
        return {
            "created_filters": len(filters),
            "filters": [f.to_dict() for f in filters]
        }
    except Exception as e:
        logger.error(f"Error generating intelligent filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate filters")

@app.post("/api/filters/prune")
async def prune_filters():
    """Prune ineffective filters"""
    try:
        results = await filter_manager.prune_ineffective_filters()
        return results
    except Exception as e:
        logger.error(f"Error pruning filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to prune filters")

@app.get("/health")
async def health_check():
    """System health check"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
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