"""
Dependency injection system for the Email Intelligence Platform
Manages service dependencies and provides them to route handlers
"""
import logging
from typing import AsyncGenerator

from backend.python_backend.database import DatabaseManager, get_db
from backend.python_backend.services.category_service import CategoryService
from backend.python_backend.services.email_service import EmailService

logger = logging.getLogger(__name__)


# Dependency functions for services
async def get_email_service(
    db: DatabaseManager = Depends(get_db),
) -> AsyncGenerator[EmailService, None]:
    """Provides an EmailService instance"""
    service = EmailService(db)
    try:
        yield service
    finally:
        # Perform any cleanup if needed
        pass


async def get_category_service(
    db: DatabaseManager = Depends(get_db),
) -> AsyncGenerator[CategoryService, None]:
    """Provides a CategoryService instance"""
    service = CategoryService(db)
    try:
        yield service
    finally:
        # Perform any cleanup if needed
        pass


# For backward compatibility with existing code
async def get_database() -> DatabaseManager:
    """Provides database instance (for existing code that uses direct database access)"""
    db = await get_db()
    return db
