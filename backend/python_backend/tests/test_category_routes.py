from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.python_backend.main import app  # Main FastAPI app

# Mock DatabaseManager methods used by category_routes
mock_db_manager_cat = (
    MagicMock()
)  # Use a different name to avoid conflict if tests run in same session
mock_db_manager_cat.get_all_categories = AsyncMock()
mock_db_manager_cat.create_category = AsyncMock()
# update_category is not used by the current category_routes.py, but good to have if it were
mock_db_manager_cat.update_category = AsyncMock()


@pytest.fixture(scope="module", autouse=True)
def mock_cat_dependencies():
    with patch("backend.python_backend.category_routes.performance_monitor"):
        yield


@pytest.fixture
def client_cat():
    from backend.python_backend.database import get_db

    app.dependency_overrides[get_db] = lambda: mock_db_manager_cat
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]  # Clean up override


def test_get_all_categories(client_cat):
    mock_categories_data = [
        {"id": 1, "name": "Work", "description": "Work related", "color": "#ff0000", "count": 5}
    ]
    mock_db_manager_cat.get_all_categories.return_value = mock_categories_data

    response = client_cat.get("/api/categories")
    assert response.status_code == 200
    assert response.json() == mock_categories_data
    mock_db_manager_cat.get_all_categories.assert_called_once()


def test_get_all_categories_db_error(client_cat):
    mock_db_manager_cat.get_all_categories.side_effect = Exception(
        "DB Error"
    )  # Simulate generic exception

    response = client_cat.get("/api/categories")
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Failed to fetch categories"
    }  # Match error detail in route


def test_create_category(client_cat):
    new_category_data = {"name": "Personal", "description": "Personal stuff", "color": "#00ff00"}
    # This is what db.create_category is expected to return (a dict)
    created_category_db_dict = {**new_category_data, "id": 2, "count": 0}
    mock_db_manager_cat.create_category.return_value = created_category_db_dict

    response = client_cat.post("/api/categories", json=new_category_data)

    assert response.status_code == 200  # Route returns CategoryResponse, not 201
    assert response.json()["name"] == "Personal"
    assert response.json()["id"] == 2
    mock_db_manager_cat.create_category.assert_called_once_with(new_category_data)


def test_create_category_db_error(client_cat):
    new_category_data = {"name": "ErrorCategory", "description": "Test error", "color": "#0000ff"}
    mock_db_manager_cat.create_category.side_effect = Exception("DB Create Error")

    response = client_cat.post("/api/categories", json=new_category_data)
    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to create category"}


# Note: category_routes.py does not currently have PUT /api/categories/{id}
# If it were added, tests would be similar to update_email in test_email_routes.py