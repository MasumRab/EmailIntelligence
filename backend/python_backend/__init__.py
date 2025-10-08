"""
Python Backend for Gmail AI Email Management
Optimized FastAPI backend with comprehensive NLP integration
"""

from backend.python_nlp.gmail_service import GmailAIService
from backend.python_nlp.smart_filters import EmailFilter, SmartFilterManager

from .ai_engine import AdvancedAIEngine, AIAnalysisResult
from .database import DatabaseManager
from .main import app
from .models import (
    ActivityCreate,
    ActivityResponse,
    AIAnalysisResponse,
    CategoryCreate,
    CategoryResponse,
    DashboardStats,
    EmailCreate,
    EmailResponse,
    EmailUpdate,
    FilterRequest,
    GmailSyncRequest,
    GmailSyncResponse,
    SmartRetrievalRequest,
)

__version__ = "2.0.0"

__all__ = [
    "app",
    "DatabaseManager",
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
]
