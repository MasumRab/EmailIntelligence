"""
Basic tests to verify test setup is working.
"""

import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """Test the basic health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_app_creation():
    """Test that the test app can be created."""
    from tests.conftest import create_app

    app = create_app()
    assert app.title == "Test App"
    assert app.version == "1.0.0"


@pytest.mark.asyncio
async def test_mock_database_manager(mock_db_manager):
    """Test that mock database manager works."""
    # Test that the mock methods exist
    assert hasattr(mock_db_manager, "get_all_categories")
    assert hasattr(mock_db_manager, "create_category")
    assert hasattr(mock_db_manager, "get_email_by_id")

    # Test calling a mock method
    mock_db_manager.get_all_categories.return_value = [{"id": 1, "name": "Test"}]
    result = await mock_db_manager.get_all_categories()
    assert result == [{"id": 1, "name": "Test"}]
