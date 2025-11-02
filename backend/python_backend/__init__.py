"""
Python Backend for Gmail AI Email Management
Optimized FastAPI backend with comprehensive NLP integration

Use the modular architecture in src/ and modules/ instead.
"""

import warnings

warnings.warn(
    "backend.python_backend is deprecated. Use src.main:create_app() for the new modular architecture.",
    DeprecationWarning,
    stacklevel=2,
)

from backend.python_nlp.gmail_service import GmailAIService
from backend.python_nlp.smart_filters import EmailFilter, SmartFilterManager

from .ai_engine import AdvancedAIEngine, AIAnalysisResult
from .database import DatabaseManager, get_db
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
