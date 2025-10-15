"""
Dependency injection system for the Email Intelligence Platform
Manages service dependencies and provides them to route handlers
"""
from typing import Generator, AsyncGenerator
from fastapi import Depends
from backend.python_backend.services.email_service import EmailService
from backend.python_backend.services.category_service import CategoryService
from backend.python_backend.ai_engine import AdvancedAIEngine
from backend.python_nlp.smart_filters import SmartFilterManager
from backend.python_backend.workflow_engine import WorkflowEngine
from backend.python_nlp.gmail_service import GmailAIService
from backend.python_backend.model_manager import ModelManager
from backend.python_backend.database import get_db


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


# Additional dependencies for other services can be added here


# Global instances for backward compatibility
_workflow_engine_instance = None


async def initialize_services():
    """Initialize services for backward compatibility"""
    pass