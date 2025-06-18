import io
import unittest
from http.client import HTTPResponse
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from googleapiclient.errors import HttpError

from server.python_backend.main import (  # Assuming get_db is for DatabaseManager, not directly used here but good to keep consistent
    app,
    get_db,
)
from server.python_backend.models import GmailSyncRequest, SmartRetrievalRequest

# Mock DatabaseManager (though not directly used by these endpoints, it's good practice if other parts of app setup need it)
mock_db_manager_gmail = MagicMock()


async def override_get_db_gmail():
    return mock_db_manager_gmail


# If get_db is already overridden globally, this might cause issues if not managed.
# For simplicity in this subtask, we assume a fresh app instance or careful override management.
# A better approach might be to have specific test app instances if overrides conflict.
# For now, let's ensure it doesn't break other tests by being specific if needed.
# However, the previous tests already set app.dependency_overrides[get_db].
# Let's assume that override is fine and doesn't conflict.


class TestGmailAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # It's crucial to patch the *instance* of GmailAIService and PerformanceMonitor
        # that are created and used in main.py, or patch their classes before instantiation.
        # Patching at the source of where they are imported in main.py is usually most reliable.

        self.mock_gmail_service_patch = patch(
            "server.python_backend.main.gmail_service", autospec=True
        )
        self.mock_performance_monitor_patch = patch(
            "server.python_backend.main.performance_monitor", autospec=True
        )

        self.mock_gmail_service = self.mock_gmail_service_patch.start()
        self.mock_performance_monitor = self.mock_performance_monitor_patch.start()

        # Configure async method mocks
        self.mock_gmail_service.sync_gmail_emails = AsyncMock()
        self.mock_gmail_service.execute_smart_retrieval = AsyncMock()
        self.mock_gmail_service.get_retrieval_strategies = AsyncMock()
        self.mock_gmail_service.get_performance_metrics = AsyncMock()

        # Ensure the 'track' attribute on the mocked performance_monitor instance is also a mock
        # that can be called as a decorator and returns a callable.
        # The actual decorator logic is complex, so for testing endpoint logic,
        # we often just need it to not break the decoration process.
        # A simple way is to have it return the function it decorates.
        self.mock_performance_monitor.track = MagicMock(side_effect=lambda func: func)
        # If specific calls to record_sync_performance are to be tested:
        # self.mock_performance_monitor_instance = self.mock_performance_monitor.return_value # Get the instance created by app
        # self.mock_performance_monitor_instance.record_sync_performance = AsyncMock() # Mock on the instance
        # Corrected mocking: record_sync_performance should be a method of the mock_performance_monitor itself
        self.mock_performance_monitor.record_sync_performance = AsyncMock()

    def tearDown(self):
        self.mock_gmail_service_patch.stop()
        self.mock_performance_monitor_patch.stop()
        # Clear any global dependency overrides if they were specific to this test class
        # For now, assuming the global override of get_db is acceptable.

    def test_sync_gmail_success(self):
        print("Running test_sync_gmail_success")
        request_data = {
            "maxEmails": 10,
            "queryFilter": "is:unread",
            "includeAIAnalysis": True,
            "strategies": [],
        }
        mock_sync_result = {
            "success": True,
            "processed_count": 5,
            "batch_info": {"batch_id": "batch123", "timestamp": "2023-10-27T10:00:00Z"},
            "statistics": {"analyzed": 5, "categorized": 5},
        }
        self.mock_gmail_service.sync_gmail_emails.return_value = mock_sync_result

        response = self.client.post("/api/gmail/sync", json=request_data)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["processedCount"], 5)
        self.assertEqual(data["emailsCreated"], 5)  # Approximation in main.py
        self.assertEqual(data["batchInfo"]["batchId"], "batch123")  # Changed batch_id to batchId
        self.mock_gmail_service.sync_gmail_emails.assert_called_once_with(
            max_emails=request_data["maxEmails"],
            query_filter=request_data["queryFilter"],
            include_ai_analysis=request_data["includeAIAnalysis"],
        )
        self.mock_performance_monitor.record_sync_performance.assert_called_once()

    def test_sync_gmail_nlp_failure(self):
        print("Running test_sync_gmail_nlp_failure")
        request_data = {"maxEmails": 10}  # Using defaults for other fields
        mock_sync_result = {
            "success": False,
            "error": "NLP service error",
            "statistics": {},
        }
        self.mock_gmail_service.sync_gmail_emails.return_value = mock_sync_result

        response = self.client.post("/api/gmail/sync", json=request_data)

        self.assertEqual(response.status_code, 200)  # Endpoint itself succeeds, but reports failure
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "NLP service error")
        self.mock_performance_monitor.record_sync_performance.assert_called_once()

    def test_sync_gmail_google_api_error_401(self):
        print("Running test_sync_gmail_google_api_error_401")
        request_data = {"maxEmails": 10}
        # Simulate HttpError from googleapiclient
        mock_resp = MagicMock(spec=HTTPResponse)
        mock_resp.status = 401
        mock_resp.reason = "Unauthorized"  # Added reason
        error_content = b'{"error": {"message": "Auth error"}}'

        self.mock_gmail_service.sync_gmail_emails.side_effect = HttpError(
            resp=mock_resp, content=error_content
        )

        response = self.client.post("/api/gmail/sync", json=request_data)

        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(
            data["detail"],
            "Gmail API authentication failed. Check credentials or token.",
        )
        self.mock_performance_monitor.record_sync_performance.assert_not_called()

    def test_sync_gmail_google_api_error_500(self):
        print("Running test_sync_gmail_google_api_error_500")
        request_data = {"maxEmails": 10}
        mock_resp = MagicMock(spec=HTTPResponse)
        mock_resp.status = 500
        mock_resp.reason = "Internal Server Error"  # Added reason
        error_content = b'{"error": {"message": "Server error"}}'

        self.mock_gmail_service.sync_gmail_emails.side_effect = HttpError(
            resp=mock_resp, content=error_content
        )

        response = self.client.post("/api/gmail/sync", json=request_data)

        self.assertEqual(response.status_code, 502)  # Treated as Bad Gateway
        data = response.json()
        self.assertEqual(
            data["detail"],
            "Gmail API returned an unexpected error. Please try again later.",
        )
        self.mock_performance_monitor.record_sync_performance.assert_not_called()

    def test_sync_gmail_generic_exception(self):
        print("Running test_sync_gmail_generic_exception")
        request_data = {"maxEmails": 10}
        self.mock_gmail_service.sync_gmail_emails.side_effect = Exception("Some unexpected error")

        response = self.client.post("/api/gmail/sync", json=request_data)

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertTrue(
            "Gmail sync failed due to an unexpected error: Some unexpected error" in data["detail"]
        )
        self.mock_performance_monitor.record_sync_performance.assert_not_called()

    def test_smart_retrieval_success(self):
        print("Running test_smart_retrieval_success")
        request_data = {
            "strategies": ["urgent"],
            "maxApiCalls": 50,
            "timeBudgetMinutes": 10,
        }
        mock_retrieval_result = {
            "status": "completed",
            "emails_found": 5,
            "details": "...",
        }
        self.mock_gmail_service.execute_smart_retrieval.return_value = mock_retrieval_result

        response = self.client.post("/api/gmail/smart-retrieval", json=request_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_retrieval_result)
        self.mock_gmail_service.execute_smart_retrieval.assert_called_once_with(
            strategies=request_data["strategies"],
            max_api_calls=request_data["maxApiCalls"],
            time_budget_minutes=request_data["timeBudgetMinutes"],
        )

    def test_smart_retrieval_google_api_error(self):
        print("Running test_smart_retrieval_google_api_error")
        request_data = {"strategies": ["urgent"]}
        mock_resp = MagicMock(spec=HTTPResponse)
        mock_resp.status = 403
        mock_resp.reason = "Forbidden"  # Added reason
        error_content = b'{"error": {"message": "Permission issue"}}'
        self.mock_gmail_service.execute_smart_retrieval.side_effect = HttpError(
            resp=mock_resp, content=error_content
        )

        response = self.client.post("/api/gmail/smart-retrieval", json=request_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "Gmail API permission denied. Ensure API is enabled and scopes are correct.",
        )

    def test_smart_retrieval_generic_exception(self):
        print("Running test_smart_retrieval_generic_exception")
        request_data = {"strategies": ["urgent"]}
        self.mock_gmail_service.execute_smart_retrieval.side_effect = Exception(
            "Smart retrieval failed"
        )

        response = self.client.post("/api/gmail/smart-retrieval", json=request_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn(
            "Smart retrieval failed due to an unexpected error: Smart retrieval failed",
            response.json()["detail"],
        )

    def test_get_retrieval_strategies_success(self):
        print("Running test_get_retrieval_strategies_success")
        mock_strategies = ["urgent", "follow-up", "unread_sender_x"]
        self.mock_gmail_service.get_retrieval_strategies.return_value = mock_strategies

        response = self.client.get("/api/gmail/strategies")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"strategies": mock_strategies})
        self.mock_gmail_service.get_retrieval_strategies.assert_called_once()

    def test_get_retrieval_strategies_exception(self):
        print("Running test_get_retrieval_strategies_exception")
        self.mock_gmail_service.get_retrieval_strategies.side_effect = Exception(
            "Error fetching strategies"
        )

        response = self.client.get("/api/gmail/strategies")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Failed to fetch strategies"})

    def test_get_gmail_performance_success(self):
        print("Running test_get_gmail_performance_success")
        mock_metrics = {"api_calls": 100, "avg_latency_ms": 250}
        self.mock_gmail_service.get_performance_metrics.return_value = mock_metrics

        response = self.client.get("/api/gmail/performance")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_metrics)
        self.mock_gmail_service.get_performance_metrics.assert_called_once()

    def test_get_gmail_performance_no_data(self):
        print("Running test_get_gmail_performance_no_data")
        self.mock_gmail_service.get_performance_metrics.return_value = (
            None  # Or {} as per main.py logic
        )

        response = self.client.get("/api/gmail/performance")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"status": "no_data"}
        )  # main.py returns this if metrics is None or empty
        self.mock_gmail_service.get_performance_metrics.assert_called_once()

    def test_get_gmail_performance_exception(self):
        print("Running test_get_gmail_performance_exception")
        self.mock_gmail_service.get_performance_metrics.side_effect = Exception(
            "Error fetching metrics"
        )

        response = self.client.get("/api/gmail/performance")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Failed to fetch performance metrics"})


if __name__ == "__main__":
    unittest.main()
