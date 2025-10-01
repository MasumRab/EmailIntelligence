from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.python_backend.main import app
from backend.python_nlp.smart_filters import EmailFilter

# Mock SmartFilterManager methods
mock_filter_manager_instance = MagicMock()
mock_filter_manager_instance.get_active_filters_sorted = MagicMock()
mock_filter_manager_instance.add_custom_filter = MagicMock()
mock_filter_manager_instance.create_intelligent_filters = AsyncMock()
mock_filter_manager_instance.prune_ineffective_filters = AsyncMock()

# Mock DatabaseManager
mock_db_manager_filter = MagicMock()
mock_db_manager_filter.get_recent_emails = AsyncMock()


@pytest.fixture(scope="module", autouse=True)
def mock_filter_dependencies():
    with patch(
        "backend.python_backend.filter_routes.filter_manager",
        mock_filter_manager_instance,
    ), patch("backend.python_backend.filter_routes.performance_monitor"):
        yield


@pytest.fixture
def client_filter():
    # Reset mocks before each test
    mock_filter_manager_instance.reset_mock()
    mock_filter_manager_instance.get_active_filters_sorted.reset_mock()
    mock_filter_manager_instance.add_custom_filter.reset_mock()
    mock_filter_manager_instance.create_intelligent_filters.reset_mock()
    mock_filter_manager_instance.prune_ineffective_filters.reset_mock()
    mock_db_manager_filter.reset_mock()

    from backend.python_backend.database import get_db

    app.dependency_overrides[get_db] = lambda: mock_db_manager_filter
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]


def test_get_filters(client_filter):
    """Test get_filters with the correct mock."""
    mock_filters_data = [{"filter_id": "filter1", "name": "Test Filter"}]
    mock_filter_manager_instance.get_active_filters_sorted.return_value = (
        mock_filters_data
    )

    response = client_filter.get("/api/filters")
    assert response.status_code == 200
    assert response.json() == {"filters": mock_filters_data}
    mock_filter_manager_instance.get_active_filters_sorted.assert_called_once()


def test_create_filter(client_filter):
    """Test create_filter with a fully valid payload."""
    filter_request_data = {
        "name": "My Custom Filter",
        "description": "A test filter",
        "criteria": {
            "from_patterns": ["*@example.com"],
            "subject_keywords": ["test"],
            "content_keywords": None,
            "exclude_patterns": None,
            "time_sensitivity": None,
        },
        "actions": {
            "add_label": "Tested",
            "mark_important": False,
            "mark_read": True,
            "archive": False,
            "forward_to": None,
            "auto_reply": False,
        },
        "priority": 7,
    }
    mock_created_filter = EmailFilter(
        filter_id="custom_filter_id_123",
        name=filter_request_data["name"],
        description=filter_request_data["description"],
        criteria=filter_request_data["criteria"],
        actions=filter_request_data["actions"],
        priority=filter_request_data["priority"],
        effectiveness_score=0.0,
        created_date=datetime.now(),
        last_used=datetime.now(),
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
    )
    mock_filter_manager_instance.add_custom_filter.return_value = mock_created_filter

    response = client_filter.post("/api/filters", json=filter_request_data)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == mock_created_filter.name


def test_generate_intelligent_filters(client_filter):
    mock_db_manager_filter.get_recent_emails.return_value = [{"id": 1, "subject": "Sample"}]
    mock_generated_filters_data = [{"filter_id": "gen1", "name": "Generated Filter"}]
    mock_filter_manager_instance.create_intelligent_filters.return_value = (
        mock_generated_filters_data
    )

    response = client_filter.post("/api/filters/generate-intelligent")
    assert response.status_code == 200
    assert response.json() == {
        "created_filters": len(mock_generated_filters_data),
        "filters": mock_generated_filters_data,
    }
    mock_db_manager_filter.get_recent_emails.assert_called_once_with(limit=1000)
    mock_filter_manager_instance.create_intelligent_filters.assert_called_once()


def test_prune_filters(client_filter):
    mock_prune_results = {"pruned_count": 5}
    mock_filter_manager_instance.prune_ineffective_filters.return_value = (
        mock_prune_results
    )

    response = client_filter.post("/api/filters/prune")
    assert response.status_code == 200
    assert response.json() == mock_prune_results
    mock_filter_manager_instance.prune_ineffective_filters.assert_called_once()