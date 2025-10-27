"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Dependency injection system for the Email Intelligence Platform
Manages service dependencies and provides them to route handlers
"""

from typing import Generator, AsyncGenerator
import logging
from typing import TYPE_CHECKING, Optional
from fastapi import Depends
from backend.python_backend.services.email_service import EmailService
from backend.python_backend.services.category_service import CategoryService
from backend.python_backend.database import get_db, DatabaseManager
from backend.python_backend.model_manager import ModelManager
from backend.python_backend.ai_engine import AdvancedAIEngine
from backend.python_backend.smart_filters import SmartFilterManager
from backend.python_backend.workflow_engine import WorkflowEngine
from backend.python_backend.plugin_manager import PluginManager
from backend.python_nlp.gmail_service import GmailAIService

if TYPE_CHECKING:
    from backend.python_backend.model_manager import ModelManager
    from backend.python_backend.ai_engine import AdvancedAIEngine
    from backend.python_backend.smart_filters import SmartFilterManager
    from backend.python_backend.workflow_engine import WorkflowEngine
    from backend.python_backend.plugin_manager import PluginManager
    from backend.python_nlp.gmail_service import GmailAIService

logger = logging.getLogger(__name__)

# Singleton instances of services
_model_manager_instance: Optional["ModelManager"] = None
_ai_engine_instance: Optional["AdvancedAIEngine"] = None
_filter_manager_instance: Optional["SmartFilterManager"] = None
_workflow_engine_instance: Optional["WorkflowEngine"] = None
_plugin_manager_instance: Optional["PluginManager"] = None
_gmail_service_instance: Optional["GmailAIService"] = None


# Dependency functions for services
async def get_email_service() -> AsyncGenerator[EmailService, None]:
    """Provides an EmailService instance"""
    service = EmailService()
    try:
        yield service
    finally:
        # Perform any cleanup if needed
        pass


async def get_category_service() -> AsyncGenerator[CategoryService, None]:
    """Provides a CategoryService instance"""
    service = CategoryService()
    try:
        yield service
    finally:
        # Perform any cleanup if needed
        pass


async def get_ai_engine() -> AsyncGenerator[AdvancedAIEngine, None]:
    """Provides an AdvancedAIEngine instance"""
    engine = AdvancedAIEngine()
    try:
        yield engine
    finally:
        # Perform any cleanup if needed
        pass


async def get_filter_manager() -> AsyncGenerator[SmartFilterManager, None]:
    """Provides a SmartFilterManager instance"""
    manager = SmartFilterManager()
    try:
        yield manager
    finally:
        # Perform any cleanup if needed
        pass


async def get_workflow_engine() -> AsyncGenerator[WorkflowEngine, None]:
    """Provides a WorkflowEngine instance"""
    engine = WorkflowEngine()
    try:
        yield engine
    finally:
        # Perform any cleanup if needed
        pass


async def get_gmail_service() -> AsyncGenerator[GmailAIService, None]:
    """Provides a GmailAIService instance"""
    service = GmailAIService()
    try:
        yield service
    finally:
        # Perform any cleanup if needed
        pass


async def get_model_manager() -> AsyncGenerator[ModelManager, None]:
    """Provides a ModelManager instance"""
    manager = ModelManager()
    try:
        yield manager
    finally:
        # Perform any cleanup if needed
        pass


# For backward compatibility with existing code
async def get_database():
    """Provides database instance (for existing code that uses direct database access)"""
    db = await get_db()
    return db


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
            ai_engine=_ai_engine_instance, filter_manager=_filter_manager_instance, db=db
        )

    # Initialize Plugin Manager, which may need other managers
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
        _plugin_manager_instance.discover_and_load_plugins(
            model_manager=_model_manager_instance,
            workflow_engine=_workflow_engine_instance,
            ai_engine=_ai_engine_instance,
            filter_manager=_filter_manager_instance,
            db=db,
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
        logger.warning(
            "WorkflowEngine is being initialized on-the-fly. This should only happen in specific testing scenarios."
        )
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

async def get_email_service() -> "EmailService":
    """Provides an EmailService instance"""
    return EmailService()

async def get_category_service() -> "CategoryService":
    """Provides a CategoryService instance"""
    return CategoryService()

async def get_database():
    """Provides database instance (for existing code that uses direct database access)"""
    db = await get_db()
    return db
