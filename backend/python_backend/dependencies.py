"""
Dependency injectors for the FastAPI application.
"""
from typing import Optional, TYPE_CHECKING
from fastapi import Depends

# To avoid circular imports with type hints
if TYPE_CHECKING:
    from .ai_engine import AdvancedAIEngine
    from ..python_nlp.gmail_service import GmailAIService
    from ..python_nlp.smart_filters import SmartFilterManager
    from .database import DatabaseManager

from .ai_engine import AdvancedAIEngine
from ..python_nlp.gmail_service import GmailAIService
from ..python_nlp.smart_filters import SmartFilterManager
from .database import get_db, DatabaseManager


# Singleton instances
_ai_engine_instance: Optional[AdvancedAIEngine] = None
_filter_manager_instance: Optional[SmartFilterManager] = None
_gmail_service_instance: Optional[GmailAIService] = None


def get_ai_engine() -> "AdvancedAIEngine":
    """Dependency injector for AdvancedAIEngine. Returns a singleton instance."""
    global _ai_engine_instance
    if _ai_engine_instance is None:
        _ai_engine_instance = AdvancedAIEngine()
        _ai_engine_instance.initialize()
    return _ai_engine_instance


def get_filter_manager() -> "SmartFilterManager":
    """Dependency injector for SmartFilterManager. Returns a singleton instance."""
    global _filter_manager_instance
    if _filter_manager_instance is None:
        _filter_manager_instance = SmartFilterManager()
    return _filter_manager_instance


def get_gmail_service(
    db: DatabaseManager = Depends(get_db),
    ai_engine: AdvancedAIEngine = Depends(get_ai_engine),
) -> "GmailAIService":
    """
    Dependency injector for GmailAIService. Returns a singleton instance.
    This service depends on other services which are also injected.
    """
    global _gmail_service_instance
    if _gmail_service_instance is None:
        _gmail_service_instance = GmailAIService(
            db_manager=db, advanced_ai_engine=ai_engine
        )
    return _gmail_service_instance