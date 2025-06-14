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
# from .gmail_service import GmailAIService # Removed incorrect import
from .ai_engine import AdvancedAIEngine, AIAnalysisResult
# from .smart_filters import SmartFilterManager, EmailFilter # Removed, as SmartFilterManager is commented out in main.py
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
    # "GmailAIService", # Removed from __all__
    "AdvancedAIEngine",
    "AIAnalysisResult",
    # "SmartFilterManager", # Removed from __all__
    # "EmailFilter", # Removed from __all__
    "PerformanceMonitor"
]