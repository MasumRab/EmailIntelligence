import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from server.python_backend.main import app, get_db # Assuming get_db is the dependency injector for DatabaseManager
from server.python_backend.models import CategoryCreate # Pydantic model

# Mock DatabaseManager for dependency injection
mock_db_manager = MagicMock()

async def override_get_db():
    return mock_db_manager

app.dependency_overrides[get_db] = override_get_db

class TestCategoryAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Reset mocks before each test
        mock_db_manager.reset_mock()
        # Ensure async methods are AsyncMock
        mock_db_manager.get_all_categories = AsyncMock()
        mock_db_manager.create_category = AsyncMock()

    def test_get_categories_success(self):
        print("Running test_get_categories_success")
        mock_categories_data = [
            {"id": 1, "name": "Work", "description": "Work related emails", "color": "#FF0000", "count": 10},
            {"id": 2, "name": "Personal", "description": "Personal emails", "color": "#00FF00", "count": 25}
        ]
        mock_db_manager.get_all_categories.return_value = mock_categories_data

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Work")
        self.assertEqual(data[1]["name"], "Personal")
        mock_db_manager.get_all_categories.assert_called_once()

    def test_get_categories_empty(self):
        print("Running test_get_categories_empty")
        mock_db_manager.get_all_categories.return_value = []

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)
        mock_db_manager.get_all_categories.assert_called_once()

    def test_get_categories_db_error(self):
        print("Running test_get_categories_db_error")
        mock_db_manager.get_all_categories.side_effect = Exception("Database connection error")

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch categories", data["detail"])
        mock_db_manager.get_all_categories.assert_called_once()

    def test_create_category_success(self):
        print("Running test_create_category_success")
        category_data = {"name": "New Category", "description": "A new test category", "color": "#0000FF"}

        # The endpoint returns the created_category directly from db.create_category
        # which is expected to be a dict by the test setup (and how Pydantic models are often used)
        # Let's assume db.create_category returns a dict including an 'id'
        mock_created_category = {"id": 3, **category_data, "count": 0} # count is part of CategoryResponse
        mock_db_manager.create_category.return_value = mock_created_category

        response = self.client.post("/api/categories", json=category_data)

        self.assertEqual(response.status_code, 200) # FastAPI default for successful POST if no status_code is specified in @app.post
        data = response.json()
        self.assertEqual(data["name"], "New Category")
        self.assertEqual(data["description"], "A new test category")
        self.assertEqual(data["color"], "#0000FF")
        self.assertIn("id", data) # Ensure ID is returned
        self.assertEqual(data["id"], 3)
        # In main.py, create_category calls db.create_category(category.dict())
        # where category is CategoryCreate.
        # The test's category_data is compatible with CategoryCreate.
        validated_category_data = CategoryCreate(**category_data).model_dump()
        mock_db_manager.create_category.assert_called_once_with(validated_category_data)


    def test_create_category_validation_error_missing_name(self):
        print("Running test_create_category_validation_error_missing_name")
        # Missing required 'name' field
        category_data = {"description": "A category without a name", "color": "#123456"}
        response = self.client.post("/api/categories", json=category_data)
        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        response_data = response.json()
        self.assertIn("detail", response_data)
        self.assertTrue(any("name" in error['loc'] and error['type'] == 'missing' for error in response_data['detail']))

    def test_create_category_validation_error_invalid_color(self):
        print("Running test_create_category_validation_error_invalid_color")
        # Invalid color format (assuming CategoryCreate might have validation for color format)
        # For this example, let's assume a basic string check. Pydantic would catch type errors if 'color' was not a string.
        # If there's specific regex validation in CategoryCreate for color, this test would be more specific.
        # The current CategoryCreate model only defines 'name', 'description', 'color' as strings.
        # Let's test sending a non-string type for color to trigger Pydantic's type validation.
        category_data = {"name": "Invalid Color Category", "description": "Test", "color": 123}
        response = self.client.post("/api/categories", json=category_data)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()
        self.assertIn("detail", response_data)
        # Pydantic v2 type error for string is 'string_type'
        self.assertTrue(any("color" in error['loc'] and "string_type" in error['type'] for error in response_data['detail']))


    def test_create_category_db_error(self):
        print("Running test_create_category_db_error")
        category_data = {"name": "Error Category", "description": "Test DB error", "color": "#ABCDEF"}
        mock_db_manager.create_category.side_effect = Exception("Database write error")

        response = self.client.post("/api/categories", json=category_data)

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create category", data["detail"])
        validated_category_data = CategoryCreate(**category_data).model_dump()
        mock_db_manager.create_category.assert_called_once_with(validated_category_data)

if __name__ == '__main__':
    unittest.main()
