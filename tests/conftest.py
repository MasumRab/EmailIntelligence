import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from unittest.mock import AsyncMock

import pytest

# Create a minimal test app without gradio dependencies
def create_test_app():
    """Create a minimal FastAPI app for testing without gradio."""
    from fastapi import FastAPI
    app = FastAPI(title="Test App", version="1.0.0")

    # Add basic CORS
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add a simple health endpoint
    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app

try:
    from src.core.database import get_db
except SyntaxError:
    get_db = None

try:
    from src.core.factory import get_data_source
    HAS_NOTMUCH = True
except (ImportError, SyntaxError):
    HAS_NOTMUCH = False
    get_data_source = None

# Use the test app instead of the main app
from tests.conftest import create_test_app as create_app


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    pass

@pytest.fixture
def mock_db_manager():
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
    return mock


@pytest.fixture
def client(mock_db_manager: AsyncMock):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
    from fastapi.testclient import TestClient
    app = create_app()
    if get_db:
        app.dependency_overrides[get_db] = lambda: mock_db_manager
    if HAS_NOTMUCH and get_data_source:
        app.dependency_overrides[get_data_source] = lambda: mock_db_manager

    with TestClient(app) as test_client:
        yield test_client

    if get_db:
        del app.dependency_overrides[get_db]
    if HAS_NOTMUCH and get_data_source:
        del app.dependency_overrides[get_data_source]
