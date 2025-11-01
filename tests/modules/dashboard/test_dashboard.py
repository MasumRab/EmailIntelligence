import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from src.core.factory import get_data_source
from src.main import create_app

# Mock data
mock_emails = [
    {"is_read": True, "category": "Work"},
    {"is_read": False, "category": "Personal"},
    {"is_read": True, "category": "Work"},
    {"is_read": False, "category": "Uncategorized"},
]

mock_performance_log = [
    {"operation": "get_emails", "duration_seconds": 0.1},
    {"operation": "get_emails", "duration_seconds": 0.2},
    {"operation": "create_email", "duration_seconds": 0.3},
]

# Create a mock data source
mock_data_source = MagicMock()
mock_data_source.get_all_emails = AsyncMock(return_value=mock_emails)


async def override_get_data_source():
    return mock_data_source


# Create the app with the mocked dependency
app = create_app()
app.dependency_overrides[get_data_source] = override_get_data_source
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_mock_log():
    # Setup: create a mock performance log file
    import os

    log_file = "performance_metrics_log.jsonl"
    with open(log_file, "w") as f:
        for entry in mock_performance_log:
            f.write(json.dumps(entry) + "\n")

    assert os.path.exists(log_file)

    yield

    # Teardown: remove the mock log file
    os.remove(log_file)


def test_get_dashboard_stats():
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200

    data = response.json()

    assert data["total_emails"] == 4
    assert data["unread_emails"] == 2
    assert data["categorized_emails"] == {"Work": 2, "Personal": 1, "Uncategorized": 1}
    assert "get_emails" in data["performance_metrics"]
    assert "create_email" in data["performance_metrics"]
    assert data["performance_metrics"]["get_emails"] == pytest.approx(0.15)
    assert data["performance_metrics"]["create_email"] == pytest.approx(0.3)
