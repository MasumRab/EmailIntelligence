from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import pytest
from fastapi.testclient import TestClient

# Adjust import path to go up one level then into python_backend package
from backend.python_backend.main import app  # Assuming 'app' is your FastAPI instance in main.py


# Helper to create valid mock email data
def create_mock_email(email_id: int, subject: str, **kwargs) -> dict:
    """Creates a mock email dictionary that satisfies EmailResponse model."""
    now = datetime.now().isoformat()
    email_data = {
        "id": email_id,
        "messageId": f"msg_{email_id}",
        "threadId": f"thread_{email_id}",
        "sender": "test@example.com",
        "senderEmail": "test@example.com",
        "subject": subject,
        "content": f"Content for email {email_id}",
        "preview": f"Preview for email {email_id}",
        "time": now,
        "category": "Test Category",
        "categoryId": 1,
        "labels": [],
        "confidence": 90,
        "isImportant": False,
        "isStarred": False,
        "isUnread": True,
        "hasAttachments": False,
        "attachmentCount": 0,
        "sizeEstimate": 1234,
        "aiAnalysis": {},
        "filterResults": {},
    }
    email_data.update(kwargs)
    return email_data

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
mock_db_manager.search_emails_by_category = AsyncMock()

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
        patch("backend.python_backend.email_routes.ai_engine", mock_ai_engine),
        patch("backend.python_backend.email_routes.filter_manager", mock_filter_manager),
        # performance_monitor is commented out in email_routes.py, so no need to mock it
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()


# Fixture for TestClient with dependency overrides
@pytest.fixture
def client():
    from backend.python_backend.database import (  # Import here to ensure it's the one FastAPI uses
        get_db,
    )

    app.dependency_overrides[get_db] = lambda: mock_db_manager
    return TestClient(app)


def test_get_all_emails(client):
    mock_emails_data = [create_mock_email(1, "Test 1")]
    mock_db_manager.get_all_emails.return_value = mock_emails_data

    response = client.get("/api/emails")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Test 1"
    mock_db_manager.get_all_emails.assert_called_once()


def test_search_emails(client):
    mock_emails_data = [create_mock_email(2, "Search Result")]
    mock_db_manager.search_emails.return_value = mock_emails_data

    response = client.get("/api/emails?search=testquery")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Search Result"
    mock_db_manager.search_emails.assert_called_once_with("testquery")


def test_get_emails_by_category(client):
    mock_emails_data = [create_mock_email(3, "Category Email", categoryId=1)]
    mock_db_manager.get_emails_by_category.return_value = mock_emails_data

    response = client.get("/api/emails?category_id=1")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Category Email"
    mock_db_manager.get_emails_by_category.assert_called_once_with(1)


def test_search_emails_in_category(client):
    """Test searching for emails within a specific category."""
    mock_emails_data = [create_mock_email(4, "Search in Category", categoryId=2)]
    mock_db_manager.search_emails_by_category.return_value = mock_emails_data

    response = client.get("/api/emails?search=testquery&category_id=2")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Search in Category"
    mock_db_manager.search_emails_by_category.assert_called_once_with("testquery", 2)


def test_get_email_by_id_found(client):
    mock_email_data = create_mock_email(1, "Test Email Detail")
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
    now_str = datetime.now().isoformat()
    new_email_data = {
        "sender": "new@example.com",
        "senderEmail": "new@example.com",
        "subject": "New Email",
        "content": "Email content",
        "time": now_str,
    }
    mock_ai_analysis_result = MagicMock()
    mock_ai_analysis_result.confidence = 0.95
    mock_ai_analysis_result.category_id = 1
    mock_ai_analysis_result.suggested_labels = ["test"]
    mock_ai_analysis_result.to_dict.return_value = {"some_ai_field": "value"}
    mock_ai_engine.analyze_email.return_value = mock_ai_analysis_result
    mock_filter_manager.apply_filters_to_email_data.return_value = {"actions_taken": []}

    created_email_db_dict = create_mock_email(
        1, "New Email", categoryId=1, confidence=95, labels=["test"]
    )
    mock_db_manager.create_email.return_value = created_email_db_dict
    mock_db_manager.get_email_by_id.return_value = created_email_db_dict

    response = client.post("/api/emails", json=new_email_data)

    assert response.status_code == 200
    assert response.json()["subject"] == "New Email"
    mock_ai_engine.analyze_email.assert_called_once()
    mock_filter_manager.apply_filters_to_email_data.assert_called_once()
    mock_db_manager.create_email.assert_called_once()


def test_update_email(client):
    update_data = {"subject": "Updated Subject"}
    updated_email_db_dict = create_mock_email(1, "Updated Subject")
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


def test_get_emails_db_error(client):
    """Test that a database error is handled gracefully."""
    # We need to import psycopg2 to raise the correct error type
    try:
        import psycopg2
    except ImportError:
        # If psycopg2 is not installed in the test environment, we can't run this test.
        # A more robust solution would be to mock the error class itself,
        # but for this case, let's assume it's available or create a mock error class.
        class MockPsycopg2Error(Exception):
            pass
        psycopg2 = MagicMock()
        psycopg2.Error = MockPsycopg2Error

    mock_db_manager.get_all_emails.side_effect = psycopg2.Error("Database connection failed")

    response = client.get("/api/emails")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database service unavailable."}

    # Reset the mock to avoid affecting other tests
    mock_db_manager.get_all_emails.side_effect = None
