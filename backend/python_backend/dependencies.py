"""
Dependency injectors for the FastAPI application.
"""
import logging
from typing import TYPE_CHECKING, Optional

from fastapi import Depends

# To avoid circular imports with type hints
if TYPE_CHECKING:
    from .ai_engine import AdvancedAIEngine
    from .model_manager import ModelManager
    from .workflow_engine import WorkflowEngine
    from .plugin_manager import PluginManager
    from ..python_nlp.gmail_service import GmailAIService
    from ..python_nlp.smart_filters import SmartFilterManager
    from .database import DatabaseManager
    from ..python_nlp.protocols import AIEngineProtocol, DatabaseProtocol

from ..python_nlp.gmail_service import GmailAIService
from ..python_nlp.smart_filters import SmartFilterManager
from .ai_engine import AdvancedAIEngine
from .model_manager import ModelManager
from .workflow_engine import WorkflowEngine
from .plugin_manager import PluginManager
from .database import DatabaseManager, get_db
from .model_manager import ModelManager
from .plugin_manager import PluginManager
from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)

# Module-level variables to store instances
_model_manager_instance: Optional[ModelManager] = None
_ai_engine_instance: Optional[AdvancedAIEngine] = None
_filter_manager_instance: Optional[SmartFilterManager] = None
_workflow_engine_instance: Optional[WorkflowEngine] = None
_plugin_manager_instance: Optional[PluginManager] = None
_gmail_service_instance: Optional[GmailAIService] = None


async def initialize_services():
    """Initialize all singleton services. This should be called on application startup."""
    global _model_manager_instance, _ai_engine_instance, _filter_manager_instance, _workflow_engine_instance, _plugin_manager_instance, _gmail_service_instance
    
    db = await get_db()

    # Initialize core managers first
    if _model_manager_instance is None:
        _model_manager_instance = ModelManager()
        _model_manager_instance.discover_models()

    if _ai_engine_instance is None:
        _ai_engine_instance = AdvancedAIEngine(model_manager=_model_manager_instance)
        _ai_engine_instance.initialize()
    
    if _filter_manager_instance is None:
        _filter_manager_instance = SmartFilterManager()

    if _workflow_engine_instance is None:
        _workflow_engine_instance = WorkflowEngine()
        await _workflow_engine_instance.discover_workflows(
            ai_engine=_ai_engine_instance,
            filter_manager=_filter_manager_instance,
            db=db
        )

    # Initialize Plugin Manager, which may need other managers
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
        _plugin_manager_instance.discover_and_load_plugins(
            model_manager=_model_manager_instance,
            workflow_engine=_workflow_engine_instance,
            ai_engine=_ai_engine_instance,
            filter_manager=_filter_manager_instance,
            db=db
        )
    
    # Initialize services that depend on the core managers
    if _gmail_service_instance is None:
        _gmail_service_instance = GmailAIService(
            db_manager=db, advanced_ai_engine=_ai_engine_instance
        )


def get_model_manager() -> "ModelManager":
    """Dependency injector for ModelManager."""
    global _model_manager_instance
    if _model_manager_instance is None:
        _model_manager_instance = ModelManager()
        _model_manager_instance.discover_models()
    return _model_manager_instance


def get_ai_engine() -> "AdvancedAIEngine":
    """Dependency injector for AdvancedAIEngine."""
    global _ai_engine_instance
    if _ai_engine_instance is None:
        model_manager = get_model_manager()
        _ai_engine_instance = AdvancedAIEngine(model_manager=model_manager)
        _ai_engine_instance.initialize()
    return _ai_engine_instance


def get_workflow_engine() -> "WorkflowEngine":
    """Dependency injector for WorkflowEngine."""
    global _workflow_engine_instance
    if _workflow_engine_instance is None:
        # This path should ideally not be taken in production if startup events work correctly.
        logger.warning("WorkflowEngine is being initialized on-the-fly. This should only happen in specific testing scenarios.")
        _workflow_engine_instance = WorkflowEngine()
        # Cannot reliably call async discover_workflows here.
        # The primary initialization MUST happen at startup.
    return _workflow_engine_instance


def get_plugin_manager() -> "PluginManager":
    """Dependency injector for PluginManager."""
    global _plugin_manager_instance
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
        _plugin_manager_instance.discover_and_load_plugins()
    return _plugin_manager_instance


def get_filter_manager() -> "SmartFilterManager":
    """Dependency injector for SmartFilterManager."""
    global _filter_manager_instance
    if _filter_manager_instance is None:
        _filter_manager_instance = SmartFilterManager()
    return _filter_manager_instance


def get_gmail_service(
    db: DatabaseManager = Depends(get_db),
) -> "GmailAIService":
    """Dependency injector for GmailAIService."""
    global _gmail_service_instance
    if _gmail_service_instance is None:
        ai_engine = get_ai_engine()
        _gmail_service_instance = GmailAIService(db_manager=db, advanced_ai_engine=ai_engine)
    return _gmail_service_instance
