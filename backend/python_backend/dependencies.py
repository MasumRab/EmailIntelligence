"""
Dependency injection system for the Email Intelligence Platform
Manages service dependencies and provides them to route handlers
"""
from typing import Generator, AsyncGenerator
from fastapi import Depends
from backend.python_backend.services.email_service import EmailService
from backend.python_backend.services.category_service import CategoryService
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


# For backward compatibility with existing code
async def get_database():
    """Provides database instance (for existing code that uses direct database access)"""
    db = await get_db()
    return db


# Additional dependencies for other services can be added here