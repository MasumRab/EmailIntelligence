import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from server.python_backend.main import (  # Assuming get_db is the dependency injector for DatabaseManager
    app, get_db)
from server.python_backend.models import CategoryCreate  # Pydantic model

# Mock DatabaseManager for dependency injection
# REMOVED global mock_db_manager and override
# app.dependency_overrides[get_db] = override_get_db # REMOVED


# @patch('server.python_backend.main.get_db') # REMOVE class decorator
class TestCategoryAPI(unittest.TestCase):

    def setUp(self):  # REMOVE mock_get_db_globally from signature
        # Start patcher for get_db
        self.get_db_patcher = patch("server.python_backend.main.get_db")
        mock_get_db_main = self.get_db_patcher.start()  # Start the patch

        # Configure the mock that replaces the actual get_db function
        self.mock_db_instance = AsyncMock()  # This is the instance our app will receive
        mock_get_db_main.return_value = (
            self.mock_db_instance
        )  # Make get_db return our mock_db_instance

        self.client = TestClient(app)  # Initialize client after mock setup

        # Reset and configure methods on our instance for each test
        self.mock_db_instance.reset_mock()
        self.mock_db_instance.get_all_categories = (
            AsyncMock()
        )  # ensure methods are AsyncMocks
        self.mock_db_instance.create_category = AsyncMock()

    def tearDown(self):
        self.get_db_patcher.stop()  # Stop the patch

    def test_get_categories_success(self):
        print("Running test_get_categories_success")
        mock_categories_data = [
            {
                "id": 1,
                "name": "Work",
                "description": "Work related emails",
                "color": "#FF0000",
                "count": 10,
            },
            {
                "id": 2,
                "name": "Personal",
                "description": "Personal emails",
                "color": "#00FF00",
                "count": 25,
            },
        ]
        self.mock_db_instance.get_all_categories.return_value = mock_categories_data

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Work")
        self.assertEqual(data[1]["name"], "Personal")
        self.mock_db_instance.get_all_categories.assert_called_once()

    def test_get_categories_empty(self):
        print("Running test_get_categories_empty")
        self.mock_db_instance.get_all_categories.return_value = []

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)
        self.mock_db_instance.get_all_categories.assert_called_once()

    async def async_raise_db_connection_error(self, *args, **kwargs):
        raise Exception("Database connection error")

    def test_get_categories_db_error(self):
        print("Running test_get_categories_db_error")
        # Ensure the method is an AsyncMock before setting side_effect
        self.mock_db_instance.get_all_categories = AsyncMock()
        self.mock_db_instance.get_all_categories.side_effect = (
            self.async_raise_db_connection_error
        )

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch categories", data["detail"])
        self.mock_db_instance.get_all_categories.assert_called_once()

    def test_create_category_success(self):
        print("Running test_create_category_success")
        category_data = {
            "name": "New Category",
            "description": "A new test category",
            "color": "#0000FF",
        }

        # The endpoint returns the created_category directly from db.create_category
        # which is expected to be a dict by the test setup (and how Pydantic models are often used)
        # Let's assume db.create_category returns a dict including an 'id'
        mock_created_category = {
            "id": 3,
            **category_data,
            "count": 0,
        }  # count is part of CategoryResponse
        self.mock_db_instance.create_category.return_value = mock_created_category

        response = self.client.post("/api/categories", json=category_data)

        self.assertEqual(
            response.status_code, 200
        )  # FastAPI default for successful POST if no status_code is specified in @app.post
        data = response.json()
        self.assertEqual(data["name"], "New Category")
        self.assertEqual(data["description"], "A new test category")
        self.assertEqual(data["color"], "#0000FF")
        self.assertIn("id", data)  # Ensure ID is returned
        self.assertEqual(data["id"], 3)
        # In main.py, create_category calls db.create_category(category.dict())
        # where category is CategoryCreate.
        # The test's category_data is compatible with CategoryCreate.
        validated_category_data = CategoryCreate(**category_data).model_dump()
        self.mock_db_instance.create_category.assert_called_once_with(
            validated_category_data
        )

    def test_create_category_validation_error_missing_name(self):
        print("Running test_create_category_validation_error_missing_name")
        # Missing required 'name' field
        category_data = {"description": "A category without a name", "color": "#123456"}
        response = self.client.post("/api/categories", json=category_data)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity
        response_data = response.json()
        self.assertIn("detail", response_data)
        self.assertTrue(
            any(
                "name" in error["loc"] and error["type"] == "missing"
                for error in response_data["detail"]
            )
        )

    def test_create_category_validation_error_invalid_color(self):
        print("Running test_create_category_validation_error_invalid_color")
        # Invalid color format (assuming CategoryCreate might have validation for color format)
        # For this example, let's assume a basic string check. Pydantic would catch type errors if 'color' was not a string.
        # If there's specific regex validation in CategoryCreate for color, this test would be more specific.
        # The current CategoryCreate model only defines 'name', 'description', 'color' as strings.
        # Let's test sending a non-string type for color to trigger Pydantic's type validation.
        category_data = {
            "name": "Invalid Color Category",
            "description": "Test",
            "color": 123,
        }
        response = self.client.post("/api/categories", json=category_data)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()
        self.assertIn("detail", response_data)
        # Pydantic v2 type error for string is 'string_type'
        self.assertTrue(
            any(
                "color" in error["loc"] and "string_type" in error["type"]
                for error in response_data["detail"]
            )
        )

    def test_create_category_db_error(self):
        print("Running test_create_category_db_error")
        category_data = {
            "name": "Error Category",
            "description": "Test DB error",
            "color": "#ABCDEF",
        }
        mock_db_manager.create_category.side_effect = Exception("Database write error")

        response = self.client.post("/api/categories", json=category_data)

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create category", data["detail"])
        validated_category_data = CategoryCreate(**category_data).model_dump()
        mock_db_manager.create_category.assert_called_once_with(validated_category_data)

    async def async_raise_db_write_error(self, *args, **kwargs):
        raise Exception("Database write error")

    def test_create_category_db_error(self):
        print("Running test_create_category_db_error")
        category_data = {
            "name": "Error Category",
            "description": "Test DB error",
            "color": "#ABCDEF",
        }
        # Ensure the method is an AsyncMock
        self.mock_db_instance.create_category = AsyncMock()
        self.mock_db_instance.create_category.side_effect = (
            self.async_raise_db_write_error
        )

        response = self.client.post("/api/categories", json=category_data)

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create category", data["detail"])
        validated_category_data = CategoryCreate(**category_data).model_dump()
        self.mock_db_instance.create_category.assert_called_once_with(
            validated_category_data
        )


if __name__ == "__main__":
    unittest.main()
