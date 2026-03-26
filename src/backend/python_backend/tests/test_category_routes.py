import pytest


def test_get_all_categories(client, mock_db_manager):
    """Test retrieving all categories successfully."""
    mock_categories_data = [
        {"id": 1, "name": "Work", "description": "Work related", "color": "#ff0000", "count": 5}
    ]
    mock_db_manager.get_all_categories.return_value = mock_categories_data

    response = client.get("/api/categories")
    assert response.status_code == 200
    assert response.json() == mock_categories_data
    mock_db_manager.get_all_categories.assert_called_once()


def test_get_all_categories_db_error(client, mock_db_manager):
    """Test error handling when fetching all categories fails."""
    mock_db_manager.get_all_categories.side_effect = Exception("DB Error")

    response = client.get("/api/categories")
    assert response.status_code == 503
    assert response.json() == {"detail": "Database service unavailable."}


def test_create_category(client, mock_db_manager):
    """Test creating a new category successfully."""
    new_category_data = {"name": "Personal", "description": "Personal stuff", "color": "#00ff00"}
    created_category_db_dict = {**new_category_data, "id": 2, "count": 0}
    mock_db_manager.create_category.return_value = created_category_db_dict

    response = client.post("/api/categories", json=new_category_data)

    assert response.status_code == 200
    assert response.json()["name"] == "Personal"
    assert response.json()["id"] == 2
    mock_db_manager.create_category.assert_called_once_with(new_category_data)


def test_create_category_db_error(client, mock_db_manager):
    """Test error handling when creating a category fails."""
    new_category_data = {"name": "ErrorCategory", "description": "Test error", "color": "#0000ff"}
    mock_db_manager.create_category.side_effect = Exception("DB Create Error")

    response = client.post("/api/categories", json=new_category_data)
    assert response.status_code == 503
    assert response.json() == {"detail": "Database service unavailable."}
