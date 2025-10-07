import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_performance_monitor():
    """Fixture to mock the performance monitor used in dashboard routes."""
    with patch("server.python_backend.dashboard_routes.performance_monitor", new_callable=AsyncMock) as mock_pm:
        mock_pm.track = lambda func: func
        yield mock_pm

def test_get_dashboard_stats_success(client, mock_db_manager: AsyncMock, mock_performance_monitor):
    """Test successful retrieval of dashboard stats."""
    mock_stats_data = {
        "total_emails": 1000,
        "auto_labeled": 800,
        "categories": 5,
        "time_saved": "10h 30m",
        "weekly_growth": {"emails": 75, "percentage": 0.15},
    }
    mock_db_manager.get_dashboard_stats.return_value = mock_stats_data

    response = client.get("/api/dashboard/stats")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["total_emails"] == 1000
    assert response_data["time_saved"] == "10h 30m"
    assert response_data["weekly_growth"]["emails"] == 75
    mock_db_manager.get_dashboard_stats.assert_called_once()

def test_get_dashboard_stats_db_error(client, mock_db_manager: AsyncMock, mock_performance_monitor):
    """Test database error when fetching dashboard stats."""
    mock_db_manager.get_dashboard_stats.side_effect = Exception("DB Error")

    response = client.get("/api/dashboard/stats")

    assert response.status_code == 500
    assert "Failed to fetch dashboard stats" in response.json()["detail"]
    mock_db_manager.get_dashboard_stats.assert_called_once()

def test_get_performance_overview_success(client, mock_performance_monitor: AsyncMock):
    """Test successful retrieval of performance overview."""
    mock_performance_data = {
        "timestamp": "2023-01-01T12:00:00Z",
        "overallStatus": {"status": "healthy"},
        "quotaStatus": {"dailyUsage": {"percentage": 50, "remaining": 5000}},
        "strategyPerformance": [],
        "alerts": [],
        "recommendations": [],
    }
    mock_performance_monitor.get_real_time_dashboard.return_value = mock_performance_data

    response = client.get("/api/performance/overview")

    assert response.status_code == 200
    assert response.json()["overallStatus"] == {"status": "healthy"}
    mock_performance_monitor.get_real_time_dashboard.assert_called_once()

def test_get_performance_overview_error(client, mock_performance_monitor: AsyncMock):
    """Test error when fetching performance overview."""
    mock_performance_monitor.get_real_time_dashboard.side_effect = Exception("Performance monitor error")

    response = client.get("/api/performance/overview")

    assert response.status_code == 500
    assert "Failed to fetch performance data" in response.json()["detail"]
    mock_performance_monitor.get_real_time_dashboard.assert_called_once()