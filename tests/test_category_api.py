import unittest
from unittest.mock import AsyncMock, patch  # Removed MagicMock

from fastapi.testclient import TestClient

from server.python_backend.database import get_db  # Corrected import
from server.python_backend.main import app  # App import remains the same
from server.python_backend.models import CategoryCreate  # Pydantic model

# Mock DatabaseManager for dependency injection
mock_db_category_instance = AsyncMock()

async def override_get_db_for_category():
    return mock_db_category_instance

class TestCategoryAPI(unittest.TestCase):

    def setUp(self):
        # Store original dependencies
        self.original_dependencies = app.dependency_overrides.copy()
        app.dependency_overrides[get_db] = override_get_db_for_category

        self.client = TestClient(app)

        # Reset and configure methods on our instance for each test
        mock_db_category_instance.reset_mock()
        # Ensure methods are AsyncMocks; they are by default if parent is AsyncMock
        # Explicitly setting them as AsyncMock() ensures they are fresh for each test if needed,
        # but reset_mock() on the parent should clear call history.
        # If the parent mock_db_category_instance is reset, its auto-created method mocks are also reset.
        # However, explicitly assigning them ensures they are indeed AsyncMocks if there's any doubt.
        mock_db_category_instance.get_all_categories = AsyncMock()
        mock_db_category_instance.create_category = AsyncMock()

    def tearDown(self):
        # Restore original dependencies
        app.dependency_overrides = self.original_dependencies

    def test_get_categories_success(self):
        print("Running test_get_categories_success")
        mock_categories_data = [
            {
                "id": 1,
                "name": "Work",
                "description": "Work related emails",  # Line 40
                "color": "#FF0000",
                "count": 10,
            },
            {
                "id": 2,
                "name": "Personal",
                "description": "Personal emails",  # Line 47
                "color": "#00FF00",
                "count": 25,
            },
        ]
        # mock_db_category_instance.get_all_categories.return_value = mock_categories_data
        async def mock_get_all_categories_async(*args, **kwargs):
            # Ensure data matches CategoryResponse fields
            return [
                {
                    "id": 1, "name": "Work", "description": "Work related emails",
                    "color": "#FF0000", "count": 10
                },
                {
                    "id": 2, "name": "Personal", "description": "Personal emails",
                    "color": "#00FF00", "count": 25
                },
            ]
        mock_db_category_instance.get_all_categories.side_effect = mock_get_all_categories_async


        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Work")
        self.assertEqual(data[1]["name"], "Personal")
        mock_db_category_instance.get_all_categories.assert_called_once()

    def test_get_categories_empty(self):
        print("Running test_get_categories_empty")
        # mock_db_category_instance.get_all_categories.return_value = []
        async def mock_get_all_categories_empty_async(*args, **kwargs):
            return [] # This is fine, an empty list is valid
        mock_db_category_instance.get_all_categories.side_effect = mock_get_all_categories_empty_async

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)
        mock_db_category_instance.get_all_categories.assert_called_once()

    async def async_raise_db_connection_error(self, *args, **kwargs):
        raise Exception("Database connection error")

    def test_get_categories_db_error(self):
        print("Running test_get_categories_db_error")
        # Ensure the method is an AsyncMock before setting side_effect
        mock_db_category_instance.get_all_categories = AsyncMock()
        mock_db_category_instance.get_all_categories.side_effect = (
            self.async_raise_db_connection_error
        )

        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch categories", data["detail"])
        mock_db_category_instance.get_all_categories.assert_called_once()

    def test_create_category_success(self):
        print("Running test_create_category_success")
        category_data = {
            "name": "New Category",
            "description": "A new test category",
            "color": "#0000FF",
        }

        # The endpoint returns the created_category directly from db.create_category
        # which is expected to be a dict by the test setup
        # (and how Pydantic models are often used)
        # Let's assume db.create_category returns a dict including an 'id'
        mock_created_category = {
            "id": 3,
            **category_data,
            "count": 0, # Ensure 'count' is present as per CategoryResponse
        }
        # mock_db_category_instance.create_category.return_value = mock_created_category
        async def mock_create_category_async(*args, **kwargs):
            # args[0] will be the category_data dict passed from the route
            # Ensure the returned dict matches CategoryResponse
            input_data = args[0] # This is category.model_dump() from the route
            return {
                "id": 3, # Mocked ID
                "name": input_data["name"],
                "description": input_data.get("description"),
                "color": input_data.get("color", "#6366f1"), # Use default if not provided
                "count": 0 # Default count for new category
            }
        mock_db_category_instance.create_category.side_effect = mock_create_category_async

        response = self.client.post("/api/categories", json=category_data)

        # FastAPI default for successful POST is 200
        self.assertEqual(response.status_code, 200)
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
        mock_db_category_instance.create_category.assert_called_once_with(
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
        # Check for specific error details for missing 'name'
        found_error = False
        for error in response_data["detail"]:
            if "name" in error.get("loc", []) and error.get("type") == "missing":
                found_error = True
                break
        self.assertTrue(found_error, "Validation error for missing name not found.")

    def test_create_category_validation_error_invalid_color(self):
        print("Running test_create_category_validation_error_invalid_color")
        # Assuming CategoryCreate might have validation for color format.
        # For this example, let's assume a basic string check.
        # Pydantic would catch type errors if 'color' was not a string.
        # If there's specific regex validation in CategoryCreate for color,
        # this test would be more specific. The current CategoryCreate model
        # only defines 'name', 'description', 'color' as strings.
        # Let's test sending a non-string type for color to trigger
        # Pydantic's type validation.
        category_data = {
            "name": "Invalid Color Category",
            "description": "Test",
            "color": 123,  # Non-string to trigger type validation
        }
        response = self.client.post("/api/categories", json=category_data)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()
        self.assertIn("detail", response_data)
        # Check for specific error details for invalid 'color' type
        # Pydantic v2 type error for string is 'string_type'
        found_error = False
        for error in response_data["detail"]:
            if "color" in error.get("loc", []) and "string_type" in error.get("type", ""):
                found_error = True
                break
        self.assertTrue(found_error, "Validation error for invalid color type not found.")

    def test_create_category_db_error(self):
        print("Running test_create_category_db_error")
        category_data = {
            "name": "Error Category",
            "description": "Test DB error",
            "color": "#ABCDEF",
        }
        # This line was problematic because mock_db_manager was not defined in this scope.
        # mock_db_category_instance.create_category.side_effect = Exception("Database write error")
        # This was also a duplicate test method name. Correcting the one below.

        # response = self.client.post("/api/categories", json=category_data)

        # self.assertEqual(response.status_code, 500)
        # data = response.json()
        # self.assertIn("Failed to create category", data["detail"])
        # validated_category_data = CategoryCreate(**category_data).model_dump()
        # mock_db_category_instance.create_category.assert_called_once_with(validated_category_data) # Corrected to use mock_db_category_instance

    async def async_raise_db_write_error(self, *args, **kwargs):
        raise Exception("Database write error")

    def test_create_category_db_error_corrected(self): # Corrected test name
        print("Running test_create_category_db_error_corrected")
        category_data = {
            "name": "Error Category",
            "description": "Test DB error",
            "color": "#ABCDEF",
        }
        # Ensure the method is an AsyncMock
        mock_db_category_instance.create_category = AsyncMock()
        mock_db_category_instance.create_category.side_effect = (
            self.async_raise_db_write_error
        )

        response = self.client.post("/api/categories", json=category_data)

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create category", data["detail"])
        validated_category_data = CategoryCreate(**category_data).model_dump()
        mock_db_category_instance.create_category.assert_called_once_with(
            validated_category_data
        )


if __name__ == "__main__":
    unittest.main()
