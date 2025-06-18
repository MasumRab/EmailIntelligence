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
    mock_db_manager_dashboard.get_dashboard_stats.return_value = mock_stats_data_from_db

    response = client_dashboard.get("/api/dashboard/stats")
    assert response.status_code == 200

    # The response model is models.DashboardStats, which uses aliases.
    # Pydantic should handle the conversion from the db_dict keys to the aliased field names if necessary on serialization.
    # However, when comparing, ensure the response JSON matches the aliased names.
    # models.DashboardStats: totalEmails (alias total_emails), autoLabeled (alias auto_labeled), timeSaved (alias time_saved)
    # weeklyGrowth (alias weekly_growth) which itself has {emails, percentage}
    # The db_dict returns camelCase. The Pydantic model DashboardStats uses Field(alias=...)
    # So, the JSON response should have the aliased names if serialization respects aliases.
    # Let's check a few key fields.
    response_json = response.json()
    assert response_json["total_emails"] == mock_stats_data_from_db["totalEmails"]
    assert response_json["auto_labeled"] == mock_stats_data_from_db["autoLabeled"]
    assert response_json["time_saved"] == mock_stats_data_from_db["timeSaved"]
    # The weeklyGrowth structure is different between db_dict and models.DashboardStats.
    # db_dict: "weeklyGrowth": {"totalEmails": 100, "autoLabeled": 80, "categories": 2, "timeSaved": 1}
    # models.DashboardStats.weeklyGrowth: WeeklyGrowth (model) with {emails: int, percentage: float}
    # This means db.get_dashboard_stats needs to return a dict compatible with models.WeeklyGrowth for this field.
    # For this test, we assume the structure returned by db mock is what pydantic expects for DashboardStats model.
    # This implies the db_dict for weeklyGrowth should align with the Pydantic WeeklyGrowth model.
    # Let's adjust the mock_stats_data_from_db to reflect what DashboardStats model expects for weeklyGrowth.
    mock_stats_data_from_db_for_model = {
        "total_emails": 1000,
        "auto_labeled": 800,
        "categories": 10,
        "time_saved": "10 hours",
        "weekly_growth": {"emails": 100, "percentage": 0.1},  # This matches models.WeeklyGrowth
        # Other fields like unreadEmails, importantEmails from db.get_dashboard_stats are not in DashboardStats model.
    }
    mock_db_manager_dashboard.get_dashboard_stats.return_value = mock_stats_data_from_db_for_model

    response = client_dashboard.get("/api/dashboard/stats")  # Re-run with corrected mock
    assert response.status_code == 200
    response_json_rerun = response.json()
    assert response_json_rerun["total_emails"] == mock_stats_data_from_db_for_model["total_emails"]
    assert (
        response_json_rerun["weekly_growth"]["emails"]
        == mock_stats_data_from_db_for_model["weekly_growth"]["emails"]
    )

    mock_db_manager_dashboard.get_dashboard_stats.assert_called_once()


def test_get_dashboard_stats_db_error(client_dashboard):
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
