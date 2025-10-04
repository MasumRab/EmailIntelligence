from datetime import datetime
import pytest
from backend.python_nlp.smart_filters import EmailFilter

def test_get_filters(client, mock_filter_manager):
    """Test retrieving active filters."""
    mock_filters_data = [{"filter_id": "filter1", "name": "Test Filter"}]
    mock_filter_manager.get_active_filters_sorted.return_value = mock_filters_data

    response = client.get("/api/filters")
    assert response.status_code == 200
    assert response.json() == {"filters": mock_filters_data}
    mock_filter_manager.get_active_filters_sorted.assert_called_once()

def test_create_filter(client, mock_filter_manager):
    """Test creating a custom filter."""
    filter_request_data = {
        "name": "My Custom Filter", "description": "A test filter",
        "criteria": {
            "from_patterns": ["*@example.com"], "subject_keywords": ["test"],
            "content_keywords": None, "exclude_patterns": None, "time_sensitivity": None,
        },
        "actions": {
            "add_label": "Tested", "mark_important": False, "mark_read": True,
            "archive": False, "forward_to": None, "auto_reply": False,
        },
        "priority": 7,
    }
    mock_created_filter = EmailFilter(
        filter_id="custom_filter_id_123", name=filter_request_data["name"],
        description=filter_request_data["description"], criteria=filter_request_data["criteria"],
        actions=filter_request_data["actions"], priority=filter_request_data["priority"],
        effectiveness_score=0.0, created_date=datetime.now(), last_used=datetime.now(),
        usage_count=0, false_positive_rate=0.0, performance_metrics={},
    )
    mock_filter_manager.add_custom_filter.return_value = mock_created_filter

    response = client.post("/api/filters", json=filter_request_data)

    assert response.status_code == 200
    assert response.json()["name"] == mock_created_filter.name

def test_generate_intelligent_filters(client, mock_db_manager, mock_filter_manager):
    """Test the intelligent filter generation endpoint."""
    mock_db_manager.get_recent_emails.return_value = [{"id": 1, "subject": "Sample"}]
    mock_generated_filters = [{"filter_id": "gen1", "name": "Generated Filter"}]
    mock_filter_manager.create_intelligent_filters.return_value = mock_generated_filters

    response = client.post("/api/filters/generate-intelligent")
    assert response.status_code == 200
    assert response.json() == {
        "created_filters": len(mock_generated_filters),
        "filters": mock_generated_filters,
    }
    mock_db_manager.get_recent_emails.assert_called_once_with(limit=1000)
    mock_filter_manager.create_intelligent_filters.assert_called_once()

def test_prune_filters(client, mock_filter_manager):
    """Test the filter pruning endpoint."""
    mock_prune_results = {"pruned_count": 5}
    mock_filter_manager.prune_ineffective_filters.return_value = mock_prune_results

    response = client.post("/api/filters/prune")
    assert response.status_code == 200
    assert response.json() == mock_prune_results
    mock_filter_manager.prune_ineffective_filters.assert_called_once()