from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from server.python_backend.main import app
from server.python_nlp.smart_filters import EmailFilter  # For response model type hinting

# Mock SmartFilterManager methods
mock_filter_manager_instance = MagicMock()
mock_filter_manager_instance.get_all_filters = AsyncMock()
mock_filter_manager_instance.add_custom_filter = MagicMock()  # This one is synchronous in the class
mock_filter_manager_instance.create_intelligent_filters = AsyncMock()
mock_filter_manager_instance.prune_ineffective_filters = AsyncMock()

# Mock DatabaseManager (for generate_intelligent_filters which uses get_db)
mock_db_manager_filter = MagicMock()
mock_db_manager_filter.get_recent_emails = AsyncMock()

# Mock PerformanceMonitor
mock_performance_monitor_filter_instance = MagicMock()


@pytest.fixture(scope="module", autouse=True)
def mock_filter_dependencies():
    patches = [
        patch("server.python_backend.filter_routes.filter_manager", mock_filter_manager_instance),
        patch(
            "server.python_backend.filter_routes.performance_monitor",
            mock_performance_monitor_filter_instance,
        ),
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()


@pytest.fixture
def client_filter():
    from server.python_backend.database import get_db

    app.dependency_overrides[get_db] = lambda: mock_db_manager_filter
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]


def test_get_filters(client_filter):
    mock_filters_data = [{"filter_id": "filter1", "name": "Test Filter"}]  # Simplified
    mock_filter_manager_instance.get_all_filters.return_value = mock_filters_data

    response = client_filter.get("/api/filters")
    assert response.status_code == 200
    assert response.json() == {"filters": mock_filters_data}
    mock_filter_manager_instance.get_all_filters.assert_called_once()


def test_create_filter(client_filter):
    # Note: EmailFilter dataclass is complex. We'll mock the return of add_custom_filter.
    # The route uses FilterRequest Pydantic model for input.
    filter_request_data = {
        "name": "My Custom Filter",
        "criteria": {"subject_keywords": ["test"]},
        "actions": {"add_label": "Tested"},
        "priority": 7,
    }
    # Mock the EmailFilter object that add_custom_filter would return
    mock_created_filter = EmailFilter(
        filter_id="custom_filter_id_123",
        name=filter_request_data["name"],
        description=None,  # Or add if part of request
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
    # FastAPI serializes dataclasses. Response should match the dict version of mock_created_filter
    # Need to be careful with datetime objects in comparison.
    response_json = response.json()
    assert response_json["filter_id"] == mock_created_filter.filter_id
    assert response_json["name"] == mock_created_filter.name
    mock_filter_manager_instance.add_custom_filter.assert_called_once_with(
        name=filter_request_data["name"],
        description=None,  # Assuming description is optional and defaults to None if not in request
        criteria=filter_request_data["criteria"],
        actions=filter_request_data["actions"],
        priority=filter_request_data["priority"],
    )


def test_generate_intelligent_filters(client_filter):
    mock_db_manager_filter.get_recent_emails.return_value = [
        {"id": 1, "subject": "Sample"}
    ]  # Sample email data
    mock_generated_filters_data = [{"filter_id": "gen1", "name": "Generated Filter"}]  # Simplified
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
    mock_filter_manager_instance.prune_ineffective_filters.return_value = mock_prune_results

    response = client_filter.post("/api/filters/prune")
    assert response.status_code == 200
    assert response.json() == mock_prune_results
    mock_filter_manager_instance.prune_ineffective_filters.assert_called_once()
