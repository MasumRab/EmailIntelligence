import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from modules.categories.routes import router as categories_router
from src.core.data.factory import get_data_source
from src.core.auth import get_current_active_user

@pytest.fixture
def categories_client(mock_db_manager: AsyncMock):
    app = FastAPI()
    app.include_router(categories_router, prefix="/api/categories")
    app.dependency_overrides[get_data_source] = lambda: mock_db_manager
    app.dependency_overrides[get_current_active_user] = lambda: "testuser"
    with TestClient(app) as client:
        yield client

@pytest.mark.asyncio
async def test_create_and_get_categories(categories_client: TestClient, mock_db_manager: AsyncMock):
    """
    Tests creating a new category and then retrieving it to ensure the
    categories module is loaded and its API endpoints are working.
    """
    # 1. Create a new category
    new_category_data = {
        "name": "Test Category",
        "description": "A category for testing purposes.",
        "color": "#FF0000",
    }
    mock_db_manager.create_category.return_value = {"id": 1, **new_category_data}
    response = categories_client.post("/api/categories", json=new_category_data)
    assert response.status_code == 200
    created_category = response.json()
    assert created_category["name"] == new_category_data["name"]

    # 2. Get all categories and verify the new one is present
    mock_db_manager.get_all_categories.return_value = [created_category]
    response = categories_client.get("/api/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert any(cat["name"] == new_category_data["name"] for cat in categories)
