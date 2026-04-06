from backend.python_nlp.gmail_service import GmailAIService
from backend.python_nlp.smart_filters import EmailFilter, SmartFilterManager
from .ai_engine import AdvancedAIEngine, AIAnalysisResult
from .database import DatabaseManager
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

import warnings

warnings.warn(
    "backend.python_backend is deprecated. Use src.main:create_app() for the new modular architecture.",
    DeprecationWarning,
    stacklevel=2,
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
