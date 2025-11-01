import pytest
from unittest.mock import AsyncMock

from src.core.models import CategoryCreate


async def test_get_categories_success(client, mock_db_manager: AsyncMock):
    """Test successful retrieval of all categories."""
    mock_categories_data = [
        {"id": 1, "name": "Work", "description": "Work related", "color": "#ff0000", "count": 5},
        {
            "id": 2,
            "name": "Personal",
            "description": "Personal stuff",
            "color": "#00ff00",
            "count": 10,
        },
    ]
    mock_db_manager.get_all_categories.return_value = mock_categories_data

    response = client.get("/api/categories")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data == mock_categories_data
    mock_db_manager.get_all_categories.assert_called_once()


async def test_get_categories_empty(client, mock_db_manager: AsyncMock):
    """Test retrieval of an empty list of categories."""
    mock_db_manager.get_all_categories.return_value = []

    response = client.get("/api/categories")

    assert response.status_code == 200
    assert response.json() == []
    mock_db_manager.get_all_categories.assert_called_once()


async def test_get_categories_db_error(client, mock_db_manager: AsyncMock):
    """Test handling of a database error when fetching categories."""
    mock_db_manager.get_all_categories.side_effect = Exception("Database connection error")

    response = client.get("/api/categories")

    assert response.status_code == 500
    assert "Failed to fetch categories" in response.json()["detail"]
    mock_db_manager.get_all_categories.assert_called_once()


async def test_create_category_success(client, mock_db_manager: AsyncMock):
    """Test successful creation of a new category."""
    category_data = {
        "name": "New Category",
        "description": "A new test category",
        "color": "#0000FF",
    }
    mock_created_category = {"id": 3, **category_data, "count": 0}
    mock_db_manager.create_category.return_value = mock_created_category

    response = client.post("/api/categories", json=category_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "New Category"
    assert response_data["id"] == 3

    validated_category_data = CategoryCreate(**category_data).model_dump()
    mock_db_manager.create_category.assert_called_once_with(validated_category_data)


def test_create_category_validation_error(client):
    """Test validation error for creating a category with missing name."""
    category_data = {"description": "A category without a name", "color": "#123456"}
    response = client.post("/api/categories", json=category_data)
    assert response.status_code == 422


def test_create_category_db_error(client, mock_db_manager: AsyncMock):
    """Test handling of a database error when creating a category."""
    category_data = {"name": "Error Category", "description": "Test DB error", "color": "#ABCDEF"}
    mock_db_manager.create_category.side_effect = Exception("Database write error")

    response = client.post("/api/categories", json=category_data)

    assert response.status_code == 500
    assert "Failed to create category" in response.json()["detail"]
    validated_category_data = CategoryCreate(**category_data).model_dump()
    mock_db_manager.create_category.assert_called_once_with(validated_category_data)
