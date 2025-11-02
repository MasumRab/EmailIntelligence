import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.core.factory import get_email_repository
from src.core.data.repository import DatabaseEmailRepository
from src.core.data_source import DataSource
from src.core.database import DatabaseManager
from unittest.mock import MagicMock, AsyncMock
import os

# Mock authentication dependency
async def mock_get_current_user():
    return "test_user"

# Create a minimal FastAPI app for testing
app = FastAPI()
from modules.dashboard.routes import router as dashboard_router
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
from src.core.auth import get_current_active_user
app.dependency_overrides[get_current_active_user] = mock_get_current_user

@pytest.fixture
def db_manager():
    """Fixture to create an in-memory SQLite database for testing."""
    db = DatabaseManager(data_dir=":memory:")
    yield db

def test_get_dashboard_stats_with_db(db_manager):
    """Test the dashboard API with the DatabaseDataSource."""
    app.dependency_overrides[get_email_repository] = lambda: DatabaseEmailRepository(db_manager)
    client = TestClient(app)

    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_emails"] == 0

@pytest.fixture
def notmuch_data_source():
    """Fixture to create a mock NotmuchDataSource."""
    nm = MagicMock()
    nm.get_dashboard_aggregates = AsyncMock(return_value={
        'total_emails': 10,
        'auto_labeled': 5,
        'categories_count': 2,
        'unread_count': 3,
        'weekly_growth': {'emails': 1, 'percentage': 0.1}
    })
    nm.get_category_breakdown = AsyncMock(return_value={
        "Work": 5,
        "Personal": 5,
    })
    return nm

def test_get_dashboard_stats_with_notmuch(notmuch_data_source):
    """Test the dashboard API with the NotmuchDataSource."""
    app.dependency_overrides[get_email_repository] = lambda: DatabaseEmailRepository(notmuch_data_source)
    client = TestClient(app)

    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_emails"] == 10
