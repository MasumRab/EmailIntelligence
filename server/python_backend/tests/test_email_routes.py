from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Adjust import path to go up one level then into python_backend package
from server.python_backend.main import \
    app  # Assuming 'app' is your FastAPI instance in main.py

# We need to ensure that dependencies in email_routes are mocked *before* TestClient(app) is called
# or that the TestClient uses dependency overrides.

# Mock external dependencies for email_routes
# These services are instantiated at the module level in email_routes.py
# So, they need to be patched there.

# Mock DatabaseManager methods used by email_routes
mock_db_manager = MagicMock()
mock_db_manager.search_emails = AsyncMock()
mock_db_manager.get_emails_by_category = AsyncMock()
mock_db_manager.get_all_emails = AsyncMock()
mock_db_manager.get_email_by_id = AsyncMock()
mock_db_manager.create_email = AsyncMock()
mock_db_manager.update_email = AsyncMock()

# Mock AdvancedAIEngine methods used by email_routes
mock_ai_engine = MagicMock()
mock_ai_engine.analyze_email = AsyncMock()

# Mock SmartFilterManager methods used by email_routes
mock_filter_manager = MagicMock()
mock_filter_manager.apply_filters_to_email_data = AsyncMock()

# Mock PerformanceMonitor as a decorator and instance
# The decorator @performance_monitor.track won't be easily mockable without deeper changes.
# For unit tests, we often test the handler functions directly without decorator effects,
# or ensure the decorator mock doesn't break things.
# If PerformanceMonitor is instantiated, mock its methods if called.
mock_performance_monitor_instance = MagicMock()


@pytest.fixture(scope="module", autouse=True)
def mock_dependencies():
    # Patch the locations where these are imported and used in email_routes.py
    # The paths for patching depend on how email_routes.py imports them.
    # Assuming:
    # from .database import get_db (FastAPI dependency) -> We'll override this in TestClient
    # ai_engine = AdvancedAIEngine() (module-level instance)
    # filter_manager = SmartFilterManager() (module-level instance)
    # performance_monitor = PerformanceMonitor() (module-level instance)

    patches = [
        patch('server.python_backend.email_routes.ai_engine', mock_ai_engine),
        patch('server.python_backend.email_routes.filter_manager', mock_filter_manager),
        patch('server.python_backend.email_routes.performance_monitor', mock_performance_monitor_instance)
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()

# Fixture for TestClient with dependency overrides
@pytest.fixture
def client():
    from server.python_backend.database import \
        get_db  # Import here to ensure it's the one FastAPI uses

    app.dependency_overrides[get_db] = lambda: mock_db_manager
    return TestClient(app)

def test_get_all_emails(client):
    mock_emails_data = [
        {"id": 1, "subject": "Test 1", "sender": "a@a.com", "senderEmail": "a@a.com", "content": "c", "preview":"p", "time":"t", "labels":[], "isImportant":False, "isStarred":False, "isUnread":True, "confidence":90}
    ]
    mock_db_manager.get_all_emails.return_value = mock_emails_data

    response = client.get("/api/emails")
    assert response.status_code == 200
    assert response.json() == mock_emails_data
    mock_db_manager.get_all_emails.assert_called_once()

def test_search_emails(client):
    mock_emails_data = [{"id": 2, "subject": "Search Result"}]
    mock_db_manager.search_emails.return_value = mock_emails_data

    response = client.get("/api/emails?search=testquery")
    assert response.status_code == 200
    # Pydantic models in routes might reformat the output, so check essential fields
    assert response.json()[0]["subject"] == "Search Result"
    mock_db_manager.search_emails.assert_called_once_with("testquery")

def test_get_emails_by_category(client):
    mock_emails_data = [{"id": 3, "subject": "Category Email"}]
    mock_db_manager.get_emails_by_category.return_value = mock_emails_data

    response = client.get("/api/emails?category_id=1")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Category Email"
    mock_db_manager.get_emails_by_category.assert_called_once_with(1)


def test_get_email_by_id_found(client):
    mock_email_data = {"id": 1, "subject": "Test Email Detail", "sender": "a@a.com", "senderEmail": "a@a.com", "content": "c", "preview":"p", "time":"t", "labels":[], "isImportant":False, "isStarred":False, "isUnread":True, "confidence":90}
    mock_db_manager.get_email_by_id.return_value = mock_email_data

    response = client.get("/api/emails/1")
    assert response.status_code == 200
    assert response.json()["subject"] == "Test Email Detail"
    mock_db_manager.get_email_by_id.assert_called_once_with(1)

def test_get_email_by_id_not_found(client):
    mock_db_manager.get_email_by_id.return_value = None

    response = client.get("/api/emails/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Email not found"}

def test_create_email(client):
    new_email_data = {
        "sender": "new@example.com",
        "senderEmail": "new@example.com",
        "subject": "New Email",
        "content": "Email content",
        "time": "2024-01-01T12:00:00Z" # Example datetime string
    }
    # Mock the return value of ai_engine.analyze_email
    mock_ai_analysis_result = MagicMock()
    mock_ai_analysis_result.confidence = 0.95
    mock_ai_analysis_result.category_id = 1
    mock_ai_analysis_result.suggested_labels = ["test"]
    mock_ai_analysis_result.to_dict.return_value = {"some_ai_field": "value"} # For analysisMetadata
    mock_ai_engine.analyze_email.return_value = mock_ai_analysis_result

    # Mock the return value of filter_manager.apply_filters_to_email_data
    mock_filter_manager.apply_filters_to_email_data.return_value = {"actions_taken": []}

    # Mock the return value of db.create_email (which returns a dict)
    # and db.get_email_by_id (which is called after creation)
    created_email_db_dict = {**new_email_data, "id": 1, "confidence": 95, "categoryId": 1, "labels": ["test"], "analysisMetadata": {"some_ai_field": "value"}}
    mock_db_manager.create_email.return_value = created_email_db_dict # Simulates what db.create_email returns
    mock_db_manager.get_email_by_id.return_value = created_email_db_dict # Simulates the re-fetch

    response = client.post("/api/emails", json=new_email_data)

    assert response.status_code == 200 # Route returns EmailResponse, not 201 directly
    assert response.json()["subject"] == "New Email"
    mock_ai_engine.analyze_email.assert_called_once()
    mock_filter_manager.apply_filters_to_email_data.assert_called_once()
    mock_db_manager.create_email.assert_called_once()


def test_update_email(client):
    update_data = {"subject": "Updated Subject"}
    updated_email_db_dict = {
        "id": 1, "subject": "Updated Subject", "sender": "a@a.com", "senderEmail": "a@a.com",
        "content": "c", "preview":"p", "time":"t", "labels":[], "isImportant":False,
        "isStarred":False, "isUnread":True, "confidence":90
    }
    mock_db_manager.update_email.return_value = updated_email_db_dict

    response = client.put("/api/emails/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["subject"] == "Updated Subject"
    mock_db_manager.update_email.assert_called_once_with(1, update_data)

def test_update_email_not_found(client):
    mock_db_manager.update_email.return_value = None
    response = client.put("/api/emails/99", json={"subject": "test"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Email not found"}
