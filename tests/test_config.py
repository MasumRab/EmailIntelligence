"""
Test configuration module to avoid importing the full application which requires gradio.
"""
import sys
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.core.database import get_db
from src.core.factory import get_data_source


def create_test_app():
    """
    Creates a minimal FastAPI app for testing without the Gradio UI.
    """
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from src.core.error_handler import add_error_handlers
    import backend.python_backend.email_routes
    import backend.python_backend.category_routes
    import backend.python_backend.dashboard_routes
    import backend.python_backend.gmail_routes
    import backend.python_backend.filter_routes
    import backend.python_backend.training_routes
    import backend.python_backend.workflow_routes
    import backend.python_backend.model_routes
    import backend.python_backend.performance_routes
    import backend.python_backend.action_routes
    import backend.python_backend.ai_routes
    
    app = FastAPI(
        title="Email Intelligence Platform Test",
        description="A test version without UI dependencies",
        version="3.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add standardized error handlers
    add_error_handlers(app)

    # Include necessary routes for testing
    from backend.python_backend import (
        email_routes,
        category_routes,
        dashboard_routes,
        gmail_routes,
        filter_routes,
        training_routes,
        workflow_routes,
        model_routes,
        performance_routes,
        action_routes,
        ai_routes
    )

    app.include_router(email_routes.router)
    app.include_router(category_routes.router)
    app.include_router(dashboard_routes.router)
    app.include_router(gmail_routes.router)
    app.include_router(filter_routes.router)
    app.include_router(training_routes.router)
    app.include_router(workflow_routes.router)
    app.include_router(model_routes.router)
    app.include_router(performance_routes.router)
    app.include_router(action_routes.router)
    app.include_router(ai_routes.router)
    
    return app


def create_mock_db_manager():
    """
    Provides a mock DatabaseManager instance.
    This mock is reset for each test function, ensuring test isolation.
    """
    mock = AsyncMock()
    # Pre-configure all database methods as AsyncMocks
    mock.get_all_categories = AsyncMock()
    mock.create_category = AsyncMock()
    mock.get_email_by_id = AsyncMock()
    mock.get_all_emails = AsyncMock()
    mock.search_emails = AsyncMock()
    mock.get_emails_by_category = AsyncMock()
    mock.create_email = AsyncMock()
    mock.update_email = AsyncMock()
    mock.get_dashboard_stats = AsyncMock()
    mock.get_recent_emails = AsyncMock()
    mock.shutdown = AsyncMock()
    return mock


def create_test_client(mock_db_manager):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
    app = create_test_app()
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_data_source] = lambda: mock_db_manager

    return TestClient(app)