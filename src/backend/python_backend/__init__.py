"""
Python Backend for Gmail AI Email Management
Optimized FastAPI backend with comprehensive NLP integration

Legacy Component - Maintained for Backward Compatibility.
Kept to preserve compatibility and to allow open PRs to migrate into the main architecture.
Planned migration: track related PRs; do not remove without explicit cross-team approval.
"""

import warnings

warnings.warn(
    "backend.python_backend is Legacy. Use src.main:create_app() for the new modular architecture.",
    DeprecationWarning,
    stacklevel=2,
)

# NOTE: Import paths updated to src-prefixed imports to work with new project structure

from .ai_engine import AdvancedAIEngine, AIAnalysisResult
from .database import DatabaseManager, get_db  # noqa: F401
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
]
