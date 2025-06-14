"""
Python Backend for Gmail AI Email Management
Optimized FastAPI backend with comprehensive NLP integration
"""

from .main import app
from .database import DatabaseManager, get_db
from .models import (
    EmailCreate, EmailUpdate, EmailResponse,
    CategoryCreate, CategoryResponse,
    ActivityCreate, ActivityResponse,
    GmailSyncRequest, GmailSyncResponse,
    SmartRetrievalRequest, FilterRequest,
    AIAnalysisResponse, DashboardStats
)
from server.python_nlp.gmail_service import GmailAIService
from .ai_engine import AdvancedAIEngine, AIAnalysisResult
from server.python_nlp.smart_filters import SmartFilterManager, EmailFilter
from .performance_monitor import PerformanceMonitor

__version__ = "2.0.0"

__all__ = [
    "app",
    "DatabaseManager",
    "get_db",
    "EmailCreate",
    "EmailUpdate", 
    "EmailResponse",
    "CategoryCreate",
    "CategoryResponse",
    "ActivityCreate",
    "ActivityResponse",
    "GmailSyncRequest",
    "GmailSyncResponse",
    "SmartRetrievalRequest",
    "FilterRequest",
    "AIAnalysisResponse",
    "DashboardStats",
    "GmailAIService",
    "AdvancedAIEngine",
    "AIAnalysisResult",
    "SmartFilterManager",
    "EmailFilter",
    "PerformanceMonitor"
]