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
mock_db_manager_dashboard = MagicMock()

async def override_get_db_dashboard():
    return mock_db_manager_dashboard

app.dependency_overrides[get_db] = override_get_db_dashboard

class TestDashboardAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        # Patch PerformanceMonitor instance used in main.py
        self.mock_performance_monitor_patch = patch('server.python_backend.main.performance_monitor', autospec=True)
        self.mock_performance_monitor = self.mock_performance_monitor_patch.start()

        # Configure async method mocks
        self.mock_performance_monitor.get_real_time_dashboard = AsyncMock()

        # Reset and configure mock_db_manager_dashboard for this suite
        mock_db_manager_dashboard.reset_mock()
        mock_db_manager_dashboard.get_dashboard_stats = AsyncMock()

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
        mock_db_manager_dashboard.get_dashboard_stats.return_value = mock_stats_data

        response = self.client.get("/api/dashboard/stats")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["totalEmails"], 1000)
        self.assertEqual(data["timeSaved"], "10h 30m")
        # Ensure the response matches the DashboardStatsResponse model structure if it's strictly enforced
        # For this test, we're checking key fields.
        mock_db_manager_dashboard.get_dashboard_stats.assert_called_once()

    def test_get_dashboard_stats_db_error(self):
        print("Running test_get_dashboard_stats_db_error")
        mock_db_manager_dashboard.get_dashboard_stats.side_effect = Exception("DB error")

        response = self.client.get("/api/dashboard/stats")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch dashboard stats", data["detail"])
        mock_db_manager_dashboard.get_dashboard_stats.assert_called_once()

    # Removed @patch('psycopg2.Error', create=True)
    def test_get_dashboard_stats_psycopg2_error(self): # Removed mock_psycopg2_error_type from params
        print("Running test_get_dashboard_stats_psycopg2_error")
        # Create an instance of the real psycopg2.Error
        db_error_instance = Psycopg2Error("Simulated DB error")
        # db_error_instance.pgcode = "12345" # pgcode is read-only, main.py handles if not present
        mock_db_manager_dashboard.get_dashboard_stats.side_effect = db_error_instance

        response = self.client.get("/api/dashboard/stats")

        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data["detail"], "Database service unavailable.")
        mock_db_manager_dashboard.get_dashboard_stats.assert_called_once()


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

    def test_get_performance_overview_error(self):
        print("Running test_get_performance_overview_error")
        self.mock_performance_monitor.get_real_time_dashboard.side_effect = Exception("Performance monitor error")

        response = self.client.get("/api/performance/overview")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to fetch performance data", data["detail"])
        self.mock_performance_monitor.get_real_time_dashboard.assert_called_once()

if __name__ == '__main__':
    unittest.main()
