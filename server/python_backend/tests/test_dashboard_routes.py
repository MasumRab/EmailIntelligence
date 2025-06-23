from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from server.python_backend.main import app

# Mock DatabaseManager methods
mock_db_manager_dashboard = MagicMock()
mock_db_manager_dashboard.get_dashboard_stats = AsyncMock()

# Mock PerformanceMonitor (instance used in dashboard_routes)
# The @performance_monitor.track decorator is on get_dashboard_stats
# The get_performance_overview route calls performance_monitor.get_real_time_dashboard()
mock_performance_monitor_dashboard_instance = MagicMock()
mock_performance_monitor_dashboard_instance.get_real_time_dashboard = AsyncMock()


@pytest.fixture(scope="module", autouse=True)
def mock_dashboard_dependencies():
    patches = [
        # Patch the instance of PerformanceMonitor used in dashboard_routes
        patch(
            "server.python_backend.dashboard_routes.performance_monitor",
            mock_performance_monitor_dashboard_instance,
        )
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()


@pytest.fixture
def client_dashboard():
    from server.python_backend.database import get_db

    app.dependency_overrides[get_db] = lambda: mock_db_manager_dashboard
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]  # Clean up


def test_get_dashboard_stats(client_dashboard):
    # This is the dict that db.get_dashboard_stats() is expected to return
    mock_stats_data_from_db = {
        "totalEmails": 1000,
        "unreadEmails": 150,
        "importantEmails": 50,
        "spamEmails": 20,
        "totalCategoryTypes": 10,
        "topCategories": [{"name": "Work", "color": "#ff0000", "count": 300}],
        "autoLabeled": 800,  # Placeholder from DB logic
        "timeSaved": "10 hours",  # Placeholder from DB logic
        "weeklyGrowth": {  # Placeholder from DB logic
            "totalEmails": 100,
            "autoLabeled": 80,
            "categories": 2,
            "timeSaved": 1,
        },
    }
    # Set the correct mock return value *before* the first API call
    mock_stats_data_from_db_for_model = {
        "total_emails": 1000,
        "auto_labeled": 800,
        "categories": 10,
        "time_saved": "10 hours",
        "weekly_growth": {"emails": 100, "percentage": 0.1},
    }
    mock_db_manager_dashboard.get_dashboard_stats.return_value = mock_stats_data_from_db_for_model
    # Reset call count specifically for the upcoming assertion
    mock_db_manager_dashboard.get_dashboard_stats.reset_mock()

    response = client_dashboard.get("/api/dashboard/stats")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["total_emails"] == mock_stats_data_from_db_for_model["total_emails"]
    assert response_json["auto_labeled"] == mock_stats_data_from_db_for_model["auto_labeled"]
    assert response_json["time_saved"] == mock_stats_data_from_db_for_model["time_saved"]
    assert response_json["categories"] == mock_stats_data_from_db_for_model["categories"]
    assert (
        response_json["weekly_growth"]["emails"]
        == mock_stats_data_from_db_for_model["weekly_growth"]["emails"]
    )
    assert (
        response_json["weekly_growth"]["percentage"]
        == mock_stats_data_from_db_for_model["weekly_growth"]["percentage"]
    )

    mock_db_manager_dashboard.get_dashboard_stats.assert_called_once()


def test_get_dashboard_stats_db_error(client_dashboard):
    # Reset the mock for this specific test to ensure clean state
    mock_db_manager_dashboard.get_dashboard_stats.reset_mock()
    mock_db_manager_dashboard.get_dashboard_stats.side_effect = Exception("DB Stats Error")

    response = client_dashboard.get("/api/dashboard/stats")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to fetch dashboard stats"


def test_get_performance_overview(client_dashboard):
    mock_overview_data = {"status": "healthy", "efficiency": 0.9}
    mock_performance_monitor_dashboard_instance.get_real_time_dashboard.return_value = (
        mock_overview_data
    )

    response = client_dashboard.get("/api/performance/overview")  # Path defined in dashboard_routes
    assert response.status_code == 200
    assert response.json() == mock_overview_data
    mock_performance_monitor_dashboard_instance.get_real_time_dashboard.assert_called_once()


def test_get_performance_overview_error(client_dashboard):
    mock_performance_monitor_dashboard_instance.get_real_time_dashboard.side_effect = Exception(
        "Perf Error"
    )

    response = client_dashboard.get("/api/performance/overview")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to fetch performance data"
