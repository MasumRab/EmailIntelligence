import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from server.python_backend.main import app, get_db
from server.python_backend.models import DashboardStats # Import specific model - corrected name
from datetime import datetime
from psycopg2 import Error as Psycopg2Error # Import real psycopg2.Error

# Mock DatabaseManager for dependency injection
# This will use the same global mock_db_manager_filter instance if tests are run together,
# or a new one if run in isolation. For cleaner tests, a proper fixture setup is better.
# For now, we re-assert the override for clarity in this specific file's context.
# Standardizing to use the same mock_db_manager name as other API test files
mock_db_manager = AsyncMock()

async def override_get_db(): # Standardized name
    return mock_db_manager

app.dependency_overrides[get_db] = override_get_db # Standardized override

class TestDashboardAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        # Patch PerformanceMonitor instance used in main.py
        self.mock_performance_monitor_patch = patch('server.python_backend.main.performance_monitor', autospec=True)
        self.mock_performance_monitor = self.mock_performance_monitor_patch.start()

        # Configure async method mocks
        self.mock_performance_monitor.get_real_time_dashboard = AsyncMock()

        # Reset and configure mock_db_manager for this suite
        mock_db_manager.reset_mock() # Changed to mock_db_manager
        # Method of an AsyncMock is an AsyncMock by default.
        mock_db_manager.get_dashboard_stats = AsyncMock() # Changed to mock_db_manager

        # Mock performance_monitor.track decorator to just return the function
        self.track_patch = patch('server.python_backend.main.performance_monitor.track', MagicMock(side_effect=lambda func: func))
        self.track_patch.start()


    def tearDown(self):
        self.mock_performance_monitor_patch.stop()
        self.track_patch.stop()
        # Clean up dependency override if it was specific to this test class
        # For now, we assume the override is managed if tests are run together
        # or this is the last test file being set up for these dependencies.

    def test_get_dashboard_stats_success(self):
        print("Running test_get_dashboard_stats_success")
        mock_stats_data = {
            "totalEmails": 1000,
            "autoLabeled": 200,
            "categories": 5,
            "timeSaved": "10h 30m",
            "weeklyGrowth": {"week1": 50, "week2": 75} # Assuming this matches DashboardStatsResponse
        }
        mock_db_manager.get_dashboard_stats.return_value = mock_stats_data # Changed to mock_db_manager

        response = self.client.get("/api/dashboard/stats")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["totalEmails"], 1000)
        self.assertEqual(data["timeSaved"], "10h 30m")
        # Ensure the response matches the DashboardStatsResponse model structure if it's strictly enforced
        # For this test, we're checking key fields.
        mock_db_manager.get_dashboard_stats.assert_called_once() # Changed to mock_db_manager

    async def async_raise_db_error(self, *args, **kwargs):
        raise Exception("DB error")

    def test_get_dashboard_stats_db_error(self):
        print("Running test_get_dashboard_stats_db_error")
        mock_db_manager.get_dashboard_stats = AsyncMock() # Ensure it's a fresh AsyncMock # Changed to mock_db_manager
        mock_db_manager.get_dashboard_stats.side_effect = self.async_raise_db_error # Changed to mock_db_manager

        response = self.client.get("/api/dashboard/stats")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch dashboard stats", data["detail"])
        mock_db_manager.get_dashboard_stats.assert_called_once() # Changed to mock_db_manager

    # Removed @patch('psycopg2.Error', create=True)
    async def async_raise_psycopg2_error(self, *args, **kwargs):
        # It's important that the side_effect function itself doesn't try to re-instantiate
        # complex error objects if they are not needed for the test's core logic,
        # or ensure they are properly picklable/transmissible if used across boundaries.
        # Here, we just raise a pre-constructed or simple one.
        raise Psycopg2Error("Simulated DB error from async side_effect")

    def test_get_dashboard_stats_psycopg2_error(self): # Removed mock_psycopg2_error_type from params
        print("Running test_get_dashboard_stats_psycopg2_error")
        mock_db_manager.get_dashboard_stats = AsyncMock() # Ensure it's fresh # Changed to mock_db_manager
        mock_db_manager.get_dashboard_stats.side_effect = self.async_raise_psycopg2_error # Changed to mock_db_manager

        response = self.client.get("/api/dashboard/stats")

        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data["detail"], "Database service unavailable.")
        mock_db_manager.get_dashboard_stats.assert_called_once() # Changed to mock_db_manager


    def test_get_performance_overview_success(self):
        print("Running test_get_performance_overview_success")
        mock_performance_data = {
            "timestamp": "2023-01-01T12:00:00Z", # Example data matching PerformanceOverview
            "overallStatus": {"status": "healthy"},
            "quotaStatus": {"dailyUsage": {"percentage": 50, "remaining": 5000}},
            "strategyPerformance": [],
            "alerts": [],
            "recommendations": []
        }
        # Ensure the mock_performance_monitor instance (the one patched in main) has its method mocked
        # patched_monitor_instance = self.mock_performance_monitor_patch.start().return_value # REMOVED
        # patched_monitor_instance.get_real_time_dashboard = AsyncMock(return_value=mock_performance_data) # REMOVED
        # self.mock_performance_monitor_patch.stop() # REMOVED

        # Use self.mock_performance_monitor directly as it's the MagicMock replacing the instance in main
        self.mock_performance_monitor.get_real_time_dashboard.return_value = mock_performance_data

        response = self.client.get("/api/performance/overview")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_performance_data)
        self.mock_performance_monitor.get_real_time_dashboard.assert_called_once()

    async def async_raise_performance_monitor_error(self, *args, **kwargs):
        raise Exception("Performance monitor error")

    def test_get_performance_overview_error(self):
        print("Running test_get_performance_overview_error")
        # self.mock_performance_monitor.get_real_time_dashboard is already an AsyncMock from setUp
        self.mock_performance_monitor.get_real_time_dashboard.side_effect = self.async_raise_performance_monitor_error

        response = self.client.get("/api/performance/overview")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch performance data", data["detail"])
        self.mock_performance_monitor.get_real_time_dashboard.assert_called_once()

if __name__ == '__main__':
    unittest.main()
