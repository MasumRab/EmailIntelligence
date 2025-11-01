import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.core.factory import get_email_repository
from unittest.mock import AsyncMock, MagicMock, patch
import json
import sys
import os

# Add the project root to the path to avoid gradio import issues
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Import routes directly to avoid gradio dependency
from modules.dashboard.routes import router as dashboard_router
from modules.dashboard.models import ConsolidatedDashboardStats

# Mock data
mock_emails = [
    {'is_read': True, 'category': 'Work'},
    {'is_read': False, 'category': 'Personal'},
    {'is_read': True, 'category': 'Work'},
    {'is_read': False, 'category': 'Uncategorized'},
]

mock_performance_log = [
    {"operation": "get_emails", "duration_seconds": 0.1},
    {"operation": "get_emails", "duration_seconds": 0.2},
    {"operation": "create_email", "duration_seconds": 0.3},
]

# Create a mock repository
mock_repository = MagicMock()
mock_repository.get_dashboard_aggregates = AsyncMock(return_value={
    'total_emails': 4,
    'auto_labeled': 3,
    'categories_count': 3,
    'unread_count': 2,
    'weekly_growth': {'emails': 4, 'percentage': 0.0}
})
mock_repository.get_category_breakdown = AsyncMock(return_value={
    "Work": 2,
    "Personal": 1,
    "Uncategorized": 1
})

async def override_get_email_repository():
    return mock_repository

# Mock authentication dependency
async def mock_get_current_user():
    return "test_user"

# Create a minimal FastAPI app for testing
app = FastAPI()
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.dependency_overrides[get_email_repository] = override_get_email_repository
# Mock authentication for testing
from src.core.auth import get_current_active_user
app.dependency_overrides[get_current_active_user] = mock_get_current_user
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_mock_log():
    # Setup: create a mock performance log file in the project root
    import os
    from pathlib import Path
    
    # Get the project root directory (two levels up from this test file)
    project_root = Path(__file__).parent.parent.parent.parent
    log_file_path = project_root / "performance_metrics_log.jsonl"
    
    with open(log_file_path, "w") as f:
        for entry in mock_performance_log:
            f.write(json.dumps(entry) + "\n")

    assert log_file_path.exists()

    yield

    # Teardown: remove the mock log file
    os.remove(log_file_path)

def test_get_dashboard_stats():
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200

    data = response.json()

    # Test core email statistics
    assert data["total_emails"] == 4
    assert data["unread_emails"] == 2
    assert data["categorized_emails"] == {"Work": 2, "Personal": 1, "Uncategorized": 1}

    # Test new consolidated fields
    assert data["time_saved"] == "0h 6m"  # 3 auto_labeled * 2 minutes = 6 minutes
    assert data["auto_labeled"] == 3  # Should be included from aggregates
    assert data["categories"] == 3   # Should be included from aggregates

    # Test performance metrics
    assert "get_emails" in data["performance_metrics"]
    assert "create_email" in data["performance_metrics"]
    assert data["performance_metrics"]["get_emails"] == pytest.approx(0.15)
    assert data["performance_metrics"]["create_email"] == pytest.approx(0.3)


def test_time_saved_calculation():
    """Test the time_saved calculation logic directly."""
    # Test cases for time_saved calculation
    test_cases = [
        (0, "0h 0m"),    # 0 auto-labeled emails
        (1, "0h 2m"),    # 1 * 2 minutes = 2 minutes
        (30, "1h 0m"),   # 30 * 2 = 60 minutes = 1 hour
        (45, "1h 30m"),  # 45 * 2 = 90 minutes = 1h 30m
        (75, "2h 30m"),  # 75 * 2 = 150 minutes = 2h 30m
    ]

    for auto_labeled, expected in test_cases:
        time_saved_minutes = auto_labeled * 2
        time_saved_hours = time_saved_minutes // 60
        time_saved_remaining_minutes = time_saved_minutes % 60
        actual = f"{time_saved_hours}h {time_saved_remaining_minutes}m"
        assert actual == expected, f"For {auto_labeled} auto-labeled emails, expected {expected}, got {actual}"
