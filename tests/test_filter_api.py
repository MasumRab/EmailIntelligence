import unittest
from datetime import datetime  # Added import
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from psycopg2 import Error as Psycopg2Error  # Import psycopg2.Error

from server.python_backend.main import app, get_db
# from server.python_backend.models import FilterRequest # Not directly used in this version of the test for payload
from server.python_nlp.smart_filters import EmailFilter  # Changed import

# Mock DatabaseManager and SmartFilterManager
# Note: The get_db dependency is already overridden globally in test_email_api.py.
# We need to ensure that the mock_db_manager here is the same instance or that
# the override is handled per test suite if necessary.
# For simplicity, we'll assume the global override is in effect.
# If mock_db_manager was defined in test_email_api.py, it needs to be accessible here.
# A better way is to manage this in a conftest.py for pytest or a base test class.
# For now, let's redefine it here and ensure it's used.

mock_db_manager_filter = MagicMock()


async def override_get_db_filter():
    return mock_db_manager_filter


app.dependency_overrides[get_db] = override_get_db_filter


class TestFilterAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        # Patch SmartFilterManager instance used in main.py
        self.mock_filter_manager_patch = patch(
            "server.python_backend.main.filter_manager", autospec=True
        )
        self.mock_filter_manager = self.mock_filter_manager_patch.start()

        # Configure async method mocks for filter_manager
        self.mock_filter_manager.get_all_filters = AsyncMock()
        # add_custom_filter in SmartFilterManager is synchronous
        self.mock_filter_manager.add_custom_filter = MagicMock()
        self.mock_filter_manager.create_intelligent_filters = AsyncMock()
        self.mock_filter_manager.prune_ineffective_filters = AsyncMock()

        # Reset and configure mock_db_manager_filter for this suite
        mock_db_manager_filter.reset_mock()
        mock_db_manager_filter.get_recent_emails = AsyncMock()

        # Mock performance_monitor.track decorator to just return the function
        # to avoid issues with decorator logic during these tests.
        self.mock_performance_monitor_patch = patch(
            "server.python_backend.main.performance_monitor.track",
            MagicMock(side_effect=lambda func: func),
        )
        self.mock_performance_monitor_patch.start()

    def tearDown(self):
        self.mock_filter_manager_patch.stop()
        self.mock_performance_monitor_patch.stop()
        # It's good practice to clear overrides if they are specific to this test class
        # However, if get_db is globally overridden, this might cause issues if other tests rely on it.
        # For now, let's assume the override_get_db_filter is specific enough or managed.
        # A robust solution would involve a test setup that handles app instances and overrides per test suite.

    def test_get_filters_success(self):
        print("Running test_get_filters_success")
        mock_filters_data = [
            {
                "name": "Filter 1",
                "criteria": {"subject_contains": "urgent"},
                "actions": {"add_label": "IMPORTANT"},
                "priority": 1,
                "enabled": True,
                "id": "filter1",
                "description": "Marks urgent emails",
            },
            {
                "name": "Filter 2",
                "criteria": {"from_sender": "newsletter@example.com"},
                "actions": {"archive": True},
                "priority": 2,
                "enabled": True,
                "id": "filter2",
                "description": "Archives newsletters",
            },
        ]
        self.mock_filter_manager.get_all_filters.return_value = mock_filters_data

        response = self.client.get("/api/filters")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("filters", data)
        self.assertEqual(len(data["filters"]), 2)
        self.assertEqual(data["filters"][0]["name"], "Filter 1")
        self.mock_filter_manager.get_all_filters.assert_called_once()

    def test_get_filters_empty(self):
        print("Running test_get_filters_empty")
        self.mock_filter_manager.get_all_filters.return_value = []

        response = self.client.get("/api/filters")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("filters", data)
        self.assertEqual(len(data["filters"]), 0)
        self.mock_filter_manager.get_all_filters.assert_called_once()

    def test_get_filters_manager_error(self):
        print("Running test_get_filters_manager_error")
        self.mock_filter_manager.get_all_filters.side_effect = Exception(
            "Filter manager error"
        )

        response = self.client.get("/api/filters")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch filters", data["detail"])
        self.mock_filter_manager.get_all_filters.assert_called_once()

    def test_create_filter_success(self):
        print("Running test_create_filter_success")
        filter_payload = {
            "name": "New Test Filter",
            "criteria": {"subject_contains": "test", "description": "Test description"},
            "actions": {
                "add_label": "TEST_LABEL",
                "mark_important": True,
            },  # Example actions dict
            "priority": 5,
        }

        # Construct the expected EmailFilter object that add_custom_filter would return
        # The actual filter_id, created_date, last_used will be dynamic in the real method
        # For the mock, we define them to check the structure.
        expected_return_filter = EmailFilter(
            filter_id="custom_New_Test_Filter_mocked_time",  # Mocked, actual is dynamic
            name=filter_payload["name"],
            description=filter_payload["criteria"]["description"],
            criteria=filter_payload["criteria"],
            actions=filter_payload["actions"],
            priority=filter_payload["priority"],
            effectiveness_score=0.0,
            created_date=datetime.now(),  # Will be serialized to string in response
            last_used=datetime.now(),  # Will be serialized to string in response
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
        )
        self.mock_filter_manager.add_custom_filter.return_value = expected_return_filter

        response = self.client.post("/api/filters", json=filter_payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["name"], filter_payload["name"])
        self.assertEqual(data["criteria"], filter_payload["criteria"])
        self.assertEqual(
            data["actions"], filter_payload["actions"]
        )  # Check actions dict
        self.assertEqual(data["priority"], filter_payload["priority"])

        # Check for presence and type of other fields
        self.assertIn("filter_id", data)
        self.assertTrue(
            data["filter_id"].startswith("custom_New_Test_Filter")
        )  # Or check against expected_return_filter.filter_id
        self.assertEqual(data["effectiveness_score"], 0.0)
        self.assertIn("created_date", data)
        self.assertIsInstance(data["created_date"], str)  # Datetime is serialized
        self.assertIn("last_used", data)
        self.assertIsInstance(data["last_used"], str)  # Datetime is serialized
        self.assertEqual(data["usage_count"], 0)
        self.assertEqual(data["false_positive_rate"], 0.0)
        self.assertEqual(data["performance_metrics"], {})

        # Check that add_custom_filter was called correctly
        self.mock_filter_manager.add_custom_filter.assert_called_once_with(
            name=filter_payload["name"],
            description=filter_payload["criteria"]["description"],
            criteria=filter_payload["criteria"],
            actions=filter_payload["actions"],
            priority=filter_payload["priority"],
        )

    def test_create_filter_validation_error(self):
        print("Running test_create_filter_validation_error")
        # Missing 'name'
        filter_payload = {
            "criteria": {"subject_contains": "test"},
            "actions": {"type": "add_label", "label_name": "TEST_LABEL"},
            "priority": 5,
        }
        response = self.client.post("/api/filters", json=filter_payload)
        self.assertEqual(response.status_code, 422)

    def test_create_filter_manager_error(self):
        print("Running test_create_filter_manager_error")
        filter_payload = {
            "name": "Error Filter",
            "criteria": {
                "subject_contains": "error",
                "description": "Error description",
            },
            "actions": {"add_label": "ERROR_LABEL"},
            "priority": 1,
        }
        self.mock_filter_manager.add_custom_filter.side_effect = Exception(
            "Cannot add filter"
        )

        response = self.client.post("/api/filters", json=filter_payload)

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create filter", data["detail"])

        # Check that add_custom_filter was called with correct arguments even if it raised an exception
        self.mock_filter_manager.add_custom_filter.assert_called_once_with(
            name=filter_payload["name"],
            description=filter_payload["criteria"]["description"],
            criteria=filter_payload["criteria"],
            actions=filter_payload["actions"],
            priority=filter_payload["priority"],
        )

    def test_generate_intelligent_filters_success(self):
        print("Running test_generate_intelligent_filters_success")
        mock_emails_data = [
            {"id": 1, "subject": "Test Email", "content": "Some content"}
        ]
        mock_generated_filters = [
            {
                "name": "Intelligent Filter 1",
                "criteria": {"pattern": "xyz"},
                "action": "archive",
                "priority": 10,
                "enabled": True,
                "description": "Auto-generated",
            }
        ]

        mock_db_manager_filter.get_recent_emails.return_value = mock_emails_data
        self.mock_filter_manager.create_intelligent_filters.return_value = (
            mock_generated_filters
        )

        response = self.client.post("/api/filters/generate-intelligent")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["created_filters"], 1)
        self.assertEqual(len(data["filters"]), 1)
        self.assertEqual(data["filters"][0]["name"], "Intelligent Filter 1")

        mock_db_manager_filter.get_recent_emails.assert_called_once_with(limit=1000)
        self.mock_filter_manager.create_intelligent_filters.assert_called_once_with(
            mock_emails_data
        )

    def test_generate_intelligent_filters_db_error(self):
        print("Running test_generate_intelligent_filters_db_error")
        # Simulate a psycopg2 specific error
        db_error = Psycopg2Error("Simulated DB connection error")
        # db_error.pgcode = "08001" # pgcode is a readonly attribute after instantiation
        mock_db_manager_filter.get_recent_emails.side_effect = db_error

        response = self.client.post("/api/filters/generate-intelligent")

        self.assertEqual(response.status_code, 503)  # As per error handling in main.py
        data = response.json()
        self.assertEqual(data["detail"], "Database service unavailable.")
        mock_db_manager_filter.get_recent_emails.assert_called_once_with(limit=1000)
        self.mock_filter_manager.create_intelligent_filters.assert_not_called()

    def test_generate_intelligent_filters_manager_error(self):
        print("Running test_generate_intelligent_filters_manager_error")
        mock_emails_data = [
            {"id": 1, "subject": "Test Email", "content": "Some content"}
        ]
        mock_db_manager_filter.get_recent_emails.return_value = mock_emails_data
        self.mock_filter_manager.create_intelligent_filters.side_effect = Exception(
            "Filter generation failed"
        )

        response = self.client.post("/api/filters/generate-intelligent")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to generate filters", data["detail"])
        self.mock_filter_manager.create_intelligent_filters.assert_called_once_with(
            mock_emails_data
        )

    def test_prune_filters_success(self):
        print("Running test_prune_filters_success")
        mock_prune_results = {
            "pruned_count": 2,
            "details": "Removed 2 ineffective filters",
        }
        self.mock_filter_manager.prune_ineffective_filters.return_value = (
            mock_prune_results
        )

        response = self.client.post("/api/filters/prune")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_prune_results)
        self.mock_filter_manager.prune_ineffective_filters.assert_called_once()

    def test_prune_filters_manager_error(self):
        print("Running test_prune_filters_manager_error")
        self.mock_filter_manager.prune_ineffective_filters.side_effect = Exception(
            "Pruning error"
        )

        response = self.client.post("/api/filters/prune")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to prune filters", data["detail"])
        self.mock_filter_manager.prune_ineffective_filters.assert_called_once()


if __name__ == "__main__":
    unittest.main()
