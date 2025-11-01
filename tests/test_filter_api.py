from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.python_backend.models import EmailFilterActions, EmailFilterCriteria, FilterRequest
from backend.python_nlp.smart_filters import EmailFilter


@pytest.fixture
def mock_filter_manager():
    """Fixture to mock the SmartFilterManager used in filter routes."""
    with patch(
        "server.python_backend.filter_routes.filter_manager", new_callable=MagicMock
    ) as mock_fm:
        yield mock_fm


@pytest.fixture
def mock_performance_monitor():
    """Fixture to mock the performance monitor."""
    with patch(
        "server.python_backend.filter_routes.performance_monitor", new_callable=AsyncMock
    ) as mock_pm:
        mock_pm.track = lambda func: func
        yield mock_pm


def test_get_filters_success(client, mock_filter_manager, mock_performance_monitor):
    """Test successful retrieval of all filters."""
    mock_filters_data = [{"name": "Filter 1"}, {"name": "Filter 2"}]
    mock_filter_manager.get_active_filters_sorted.return_value = mock_filters_data

    response = client.get("/api/filters")

    assert response.status_code == 200
    assert response.json() == {"filters": mock_filters_data}
    mock_filter_manager.get_active_filters_sorted.assert_called_once()


def test_create_filter_success(client, mock_filter_manager, mock_performance_monitor):
    """Test successful creation of a new filter."""
    filter_payload = {
        "name": "New Filter",
        "description": "A test filter",
        "criteria": {"from_patterns": ["*@example.com"]},
        "actions": {"add_label": "TEST"},
        "priority": 1,
    }

    # Create a complete mock EmailFilter object
    mock_return_filter = EmailFilter(
        filter_id="new_id",
        name="New Filter",
        description="A test filter",
        criteria={"from_patterns": ["*@example.com"]},
        actions={"add_label": "TEST"},
        priority=1,
        created_date=datetime.now(),
        last_used=datetime.now(),
        usage_count=0,
        effectiveness_score=0.0,
        false_positive_rate=0.0,
        performance_metrics={},
    )
    mock_filter_manager.add_custom_filter.return_value = mock_return_filter

    response = client.post("/api/filters", json=filter_payload)

    assert response.status_code == 200
    assert response.json()["name"] == "New Filter"
    mock_filter_manager.add_custom_filter.assert_called_once()


def test_generate_intelligent_filters_success(
    client, mock_db_manager, mock_filter_manager, mock_performance_monitor
):
    """Test successful generation of intelligent filters."""
    mock_db_manager.get_recent_emails.return_value = [{"id": 1}]
    mock_filter_manager.create_intelligent_filters.return_value = [{"name": "Intelligent Filter"}]

    response = client.post("/api/filters/generate-intelligent")

    assert response.status_code == 200
    assert response.json()["created_filters"] == 1
    mock_db_manager.get_recent_emails.assert_called_once_with(limit=1000)
    mock_filter_manager.create_intelligent_filters.assert_called_once()


def test_prune_filters_success(client, mock_filter_manager, mock_performance_monitor):
    """Test successful pruning of filters."""
    mock_filter_manager.prune_ineffective_filters.return_value = {"pruned_count": 2}

    response = client.post("/api/filters/prune")

    assert response.status_code == 200
    assert response.json()["pruned_count"] == 2
    mock_filter_manager.prune_ineffective_filters.assert_called_once()
