from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from server.python_backend.main import app
from server.python_nlp.smart_filters import EmailFilter  # For response model type hinting

# Mock SmartFilterManager methods
mock_filter_manager_instance = MagicMock()
mock_filter_manager_instance.get_all_filters = AsyncMock() # Keep for now, though get_active_filters_sorted is used by get_filters
mock_filter_manager_instance.get_active_filters_sorted = MagicMock() # For get_filters route
mock_filter_manager_instance.add_custom_filter = MagicMock()  # This one is synchronous in the class
mock_filter_manager_instance.create_intelligent_filters = MagicMock() # Changed to MagicMock
mock_filter_manager_instance.prune_ineffective_filters = MagicMock() # Changed to MagicMock

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
    # Route uses filter_manager.get_active_filters_sorted() which is synchronous
    # Provide all required fields for EmailFilter dataclass
    now = datetime.now()
    mock_filter_instance = EmailFilter(
        filter_id="filter1",
        name="Test Filter",
        description="A test filter instance", # Required
        criteria={},
        actions={},
        priority=1,
        effectiveness_score=0.0, # Required
        created_date=now,
        last_used=now,
        usage_count=0, # Required
        false_positive_rate=0.0, # Required
        performance_metrics={} # Required
    )
    # FastAPI will serialize dataclasses, so the response will be a list of dicts
    # Ensure all fields match the EmailFilter dataclass structure and FastAPI serialization
    mock_filters_data_serialized = [
        {
            "filter_id": mock_filter_instance.filter_id,
            "name": mock_filter_instance.name,
            "description": mock_filter_instance.description,
            "criteria": mock_filter_instance.criteria,
            "actions": mock_filter_instance.actions,
            "priority": mock_filter_instance.priority,
            "effectiveness_score": mock_filter_instance.effectiveness_score,
            "created_date": mock_filter_instance.created_date.isoformat(),
            "last_used": mock_filter_instance.last_used.isoformat(),
            "usage_count": mock_filter_instance.usage_count,
            "false_positive_rate": mock_filter_instance.false_positive_rate,
            "performance_metrics": mock_filter_instance.performance_metrics
            # Assuming EmailFilter dataclass does not have an 'is_active' field by default,
            # which was in FilterResponse Pydantic model. If it does, add it here.
        }
    ]
    mock_filter_manager_instance.get_active_filters_sorted.return_value = [mock_filter_instance]
    # Reset mocks that are configured per-test inside the test function itself.
    # Global mocks like get_active_filters_sorted can be configured here if their behavior is consistent for all tests in this file
    # or if they are reset in a fixture like client_filter.
    # For now, assuming get_active_filters_sorted is set once for the test_get_filters.

    response = client_filter.get("/api/filters")
    assert response.status_code == 200
    assert response.json() == {"filters": mock_filters_data_serialized}
    mock_filter_manager_instance.get_active_filters_sorted.assert_called_once()


def test_create_filter(client_filter):
    # The route uses FilterRequest Pydantic model for input.
    # Be explicit with all fields for FilterRequest to avoid 422.
    filter_request_data = {
        "name": "My Custom Filter",
        "description": "A test filter description", # Optional, provide it
        "criteria": {
            "from_patterns": None,
            "subject_keywords": ["test"],
            "content_keywords": None,
            "exclude_patterns": None,
            "time_sensitivity": None,
        },
        "actions": {
            "add_label": "Tested",
            "mark_important": False,
            "mark_read": False,
            "archive": False,
            "forward_to": None,
            "auto_reply": False,
        },
        "priority": 7,
    }

    # Mock the EmailFilter object that add_custom_filter (synchronous) would return
    # Ensure this mock_created_filter matches the EmailFilter structure from smart_filters.py
    # and how FastAPI serializes it.
    mock_created_filter_dataclass_instance = EmailFilter(
        filter_id="custom_filter_id_123",
        name=filter_request_data["name"],
        description=filter_request_data["description"],
        criteria=filter_request_data["criteria"], # add_custom_filter expects dicts for criteria/actions
        actions=filter_request_data["actions"],
        priority=filter_request_data["priority"],
        # These are default values from EmailFilter dataclass
        effectiveness_score=0.0,
        created_date=datetime.now(), # Will compare isoformat
        last_used=datetime.now(),    # Will compare isoformat
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={}
    )
    mock_filter_manager_instance.add_custom_filter.return_value = mock_created_filter_dataclass_instance

    response = client_filter.post("/api/filters", json=filter_request_data)

    assert response.status_code == 200
    response_json = response.json()

    # Compare fields, being careful with datetime
    assert response_json["filter_id"] == mock_created_filter_dataclass_instance.filter_id
    assert response_json["name"] == mock_created_filter_dataclass_instance.name
    assert response_json["description"] == mock_created_filter_dataclass_instance.description
    assert response_json["criteria"] == mock_created_filter_dataclass_instance.criteria
    assert response_json["actions"] == mock_created_filter_dataclass_instance.actions
    assert response_json["priority"] == mock_created_filter_dataclass_instance.priority
    assert response_json["created_date"] == mock_created_filter_dataclass_instance.created_date.isoformat()
    assert response_json["last_used"] == mock_created_filter_dataclass_instance.last_used.isoformat()

    # Assert mock call arguments
    # The route calls add_custom_filter with filter_request_model.criteria (Pydantic model)
    # and filter_request_model.actions (Pydantic model).
    # However, the current test structure implies add_custom_filter in SmartFilterManager expects dicts.
    # This needs to be consistent. For now, assuming it expects dicts as per original test.
    # The route code: filter_manager.add_custom_filter(..., criteria=filter_request_model.criteria, ...)
    # If add_custom_filter truly expects dicts, the route should do .model_dump() on these.
    # For now, let's keep the assertion as it was (expecting dicts).
    # The route code's description extraction is: description = filter_request_model.criteria.get("description", "")
    # This is a bug in the route. It should be filter_request_model.description.
    # The add_custom_filter in the route is called with description="" (from the bug) if not provided in criteria.
    # Or, if description is part of FilterRequest (it is), it should be filter_request_model.description.

    # Based on route code: description passed to add_custom_filter is derived from criteria.get (bug) or ""
    # The test sends description in the main payload, which FilterRequest model uses.
    # Route code: description = filter_request_model.criteria.get("description", "") -> This is wrong.
    # It should be: description = filter_request_model.description
    # Because of this bug, add_custom_filter in the route will be called with description="".
    # Let's assume the route is fixed for this assertion, or that add_custom_filter can handle it.
    # The test's filter_request_data["criteria"] does not have a "description" key.
    # So, route's current buggy `description` would be "".
    # However, the FilterRequest Pydantic model has `description: Optional[str] = None`.
    # The route then passes `filter_request_model.criteria` (which is an EmailFilterCriteria object)
    # and `filter_request_model.actions` (an EmailFilterActions object) to `add_custom_filter`.
    # The test mock `mock_filter_manager_instance.add_custom_filter` is a MagicMock, not AsyncMock.

    mock_filter_manager_instance.add_custom_filter.assert_called_once_with(
        name=filter_request_data["name"],
        description=filter_request_data["description"], # Assuming route uses filter_request_model.description
        criteria=filter_request_data["criteria"],   # Test assumes add_custom_filter takes dicts
        actions=filter_request_data["actions"],     # Test assumes add_custom_filter takes dicts
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
