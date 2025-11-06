"""
Main application factory for the Email Intelligence Platform's FastAPI backend.
This file brings together all the components of the application, including
database setup, middleware, and API routers.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.database import DatabaseManager, DatabaseConfig
from .core.settings import AppSettings
from .api import (
    emails, categories, dashboard, search,
    gmail_service, action_service, filter_service,
    workflow_service, performance_service
)
from .core.exceptions import (
    DatabaseErrorHandler,
    GmailServiceErrorHandler,
    GeneralErrorHandler
)
from .middleware import PerformanceMonitoringMiddleware, RequestLoggingMiddleware
from . import module_loader

logger = logging.getLogger(__name__)

# --- Dependency Injection Setup ---
# This section defines how dependencies like the database manager are created
# and managed throughout the application's lifecycle.

db_manager: DatabaseManager = None

async def get_db() -> DatabaseManager:
    """
    Dependency injection function to get the database manager instance.
    This ensures that the same instance is used across the application for a
    given request, without relying on a global singleton.
    """
    global db_manager
    if db_manager is None:
        # This is a fallback, but in a well-managed app, db_manager should
        # be initialized at startup.
        logger.warning("DatabaseManager was not initialized at startup. Initializing now.")
        settings = AppSettings()
        db_config = DatabaseConfig(data_dir=settings.data_dir)
        # The 'global' keyword is used to modify the db_manager in the global scope of this module
        db_manager = await DatabaseManager(config=db_config)._ensure_initialized()
    return db_manager

# --- Application Lifecycle (Lifespan) ---
# The lifespan context manager handles startup and shutdown events.

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    - On startup: Initializes the settings and the database manager.
    - On shutdown: Gracefully closes the database manager.
    """
    global db_manager
    logger.info("Application startup...")

    # Load application settings from environment variables and .env files
    settings = AppSettings()

    # Initialize the database using the settings
    db_config = DatabaseConfig(data_dir=settings.data_dir)
    db_manager = DatabaseManager(config=db_config)
    await db_manager._ensure_initialized()

    # Make the database manager and settings available to the rest of the app
    app.state.db = db_manager
    app.state.settings = settings

    yield  # The application is now running

    logger.info("Application shutdown...")
    if db_manager:
        await db_manager.shutdown()

# --- Application Factory ---

def create_app() -> FastAPI:
    """
    Creates and configures the main FastAPI application instance.
    This function acts as the central factory for the application.
    """
    # Initialize the FastAPI app with the lifespan manager
    app = FastAPI(
        title="Email Intelligence Platform API",
        description="API for managing and analyzing email data with AI-powered insights.",
        version="1.0.0",
        lifespan=lifespan
    )

    # --- Middleware ---
    # Middleware functions are processed for every request.
    app.add_middleware(PerformanceMonitoringMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # --- Exception Handlers ---
    # Custom handlers for specific exception types to ensure consistent error responses.
    app.add_exception_handler(Exception, GeneralErrorHandler.handle)
    app.add_exception_handler(IOError, DatabaseErrorHandler.handle)
    app.add_exception_handler(ConnectionError, GmailServiceErrorHandler.handle)

    # --- API Routers ---
    # Include all the API endpoints from the 'api' module.
    app.include_router(emails.router, prefix="/api/v1", tags=["Emails"])
    app.include_router(categories.router, prefix="/api/v1", tags=["Categories"])
    app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
    app.include_router(search.router, prefix="/api/v1", tags=["Search"])
    app.include_router(gmail_service.router, prefix="/api/v1", tags=["Gmail Service"])
    app.include_router(action_service.router, prefix="/api/v1", tags=["Action Service"])
    app.include_router(filter_service.router, prefix="/api/v1", tags=["Filter Service"])
    app.include_router(workflow_service.router, prefix="/api/v1", tags=["Workflow Service"])
    app.include_router(performance_service.router, prefix="/api/v1", tags=["Performance"])

    # --- Modular Component Loading ---
    # Dynamically load and register modules from the 'modules' directory.
    module_loader.load_and_register_modules(app)

    # --- Root Endpoint ---
    @app.get("/", tags=["Root"])
    async def read_root():
        """
        A simple root endpoint to confirm the API is running.
        """
        return {"message": "Welcome to the Email Intelligence Platform API!"}

    return app
