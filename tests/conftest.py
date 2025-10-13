import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.main import create_app
from src.core.database import get_db


@pytest.fixture
def mock_db_manager():
    """
    Provides a mock DatabaseManager instance.
    This mock is reset for each test function, ensuring test isolation.
    """
    mock = AsyncMock()
    # Pre-configure all database methods as AsyncMocks
    mock.get_all_categories = AsyncMock(
        return_value=[
            {
                "id": 1,
                "name": "Test Category",
                "description": "A category for testing purposes.",
                "color": "#FF0000",
            }
        ]
    )
    mock.create_category = AsyncMock(
        return_value={
            "id": 1,
            "name": "Test Category",
            "description": "A category for testing purposes.",
            "color": "#FF0000",
        }
    )
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
    app = create_app()
    app.dependency_overrides[get_db] = lambda: mock_db_manager

    with TestClient(app) as test_client:
        yield test_client

    del app.dependency_overrides[get_db]
