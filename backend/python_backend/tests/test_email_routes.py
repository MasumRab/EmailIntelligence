from datetime import datetime
from unittest.mock import MagicMock
import pytest

def create_mock_email(email_id: int, subject: str, **kwargs) -> dict:
    """Helper to create a valid mock email dictionary."""
    now = datetime.now().isoformat()
    email_data = {
        "id": email_id, "messageId": f"msg_{email_id}", "threadId": f"thread_{email_id}",
        "sender": "test@example.com", "senderEmail": "test@example.com", "subject": subject,
        "content": f"Content for email {email_id}", "preview": f"Preview for email {email_id}",
        "time": now, "category": "Test Category", "categoryId": 1, "labels": [],
        "confidence": 90, "isImportant": False, "isStarred": False, "isUnread": True,
        "hasAttachments": False, "attachmentCount": 0, "sizeEstimate": 1234,
        "aiAnalysis": {}, "filterResults": {},
    }
    email_data.update(kwargs)
    return email_data

def test_get_all_emails(client, mock_db_manager):
    mock_emails_data = [create_mock_email(1, "Test 1")]
    mock_db_manager.get_all_emails.return_value = mock_emails_data

    response = client.get("/api/emails")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Test 1"
    mock_db_manager.get_all_emails.assert_called_once()

def test_search_emails(client, mock_db_manager):
    mock_emails_data = [create_mock_email(2, "Search Result")]
    mock_db_manager.search_emails.return_value = mock_emails_data

    response = client.get("/api/emails?search=testquery")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Search Result"
    mock_db_manager.search_emails.assert_called_once_with("testquery")

def test_get_emails_by_category(client, mock_db_manager):
    mock_emails_data = [create_mock_email(3, "Category Email", categoryId=1)]
    mock_db_manager.get_emails_by_category.return_value = mock_emails_data

    response = client.get("/api/emails?category_id=1")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Category Email"
    mock_db_manager.get_emails_by_category.assert_called_once_with(1)

def test_search_emails_in_category(client, mock_db_manager):
    mock_emails_data = [create_mock_email(4, "Search in Category", categoryId=2)]
    mock_db_manager.search_emails_by_category.return_value = mock_emails_data

    response = client.get("/api/emails?search=testquery&category_id=2")
    assert response.status_code == 200
    assert response.json()[0]["subject"] == "Search in Category"
    mock_db_manager.search_emails_by_category.assert_called_once_with("testquery", 2)

def test_get_email_by_id_found(client, mock_db_manager):
    mock_email_data = create_mock_email(1, "Test Email Detail")
    mock_db_manager.get_email_by_id.return_value = mock_email_data

    response = client.get("/api/emails/1")
    assert response.status_code == 200
    assert response.json()["subject"] == "Test Email Detail"
    mock_db_manager.get_email_by_id.assert_called_once_with(1)

def test_get_email_by_id_not_found(client, mock_db_manager):
    mock_db_manager.get_email_by_id.return_value = None
    response = client.get("/api/emails/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Email not found"}

def test_create_email(client, mock_db_manager, mock_ai_engine, mock_filter_manager):
    new_email_data = {
        "sender": "new@example.com", "senderEmail": "new@example.com",
        "subject": "New Email", "content": "Email content", "time": datetime.now().isoformat(),
    }

    mock_ai_result = MagicMock()
    mock_ai_result.confidence = 0.95
    mock_ai_result.category_id = 1
    mock_ai_result.suggested_labels = ["test"]
    mock_ai_result.to_dict.return_value = {"some_ai_field": "value"}
    mock_ai_engine.analyze_email.return_value = mock_ai_result

    mock_filter_manager.apply_filters_to_email_data.return_value = {"actions_taken": []}

    created_email = create_mock_email(1, "New Email", categoryId=1, confidence=95, labels=["test"])
    mock_db_manager.create_email.return_value = created_email
    mock_db_manager.get_email_by_id.return_value = created_email

    response = client.post("/api/emails", json=new_email_data)

    assert response.status_code == 200
    assert response.json()["subject"] == "New Email"
    mock_ai_engine.analyze_email.assert_called_once()
    mock_filter_manager.apply_filters_to_email_data.assert_called_once()
    mock_db_manager.create_email.assert_called_once()

def test_update_email(client, mock_db_manager):
    update_data = {"subject": "Updated Subject"}
    updated_email = create_mock_email(1, "Updated Subject")
    mock_db_manager.update_email.return_value = updated_email

    response = client.put("/api/emails/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["subject"] == "Updated Subject"
    mock_db_manager.update_email.assert_called_once_with(1, update_data)

def test_update_email_not_found(client, mock_db_manager):
    mock_db_manager.update_email.return_value = None
    response = client.put("/api/emails/99", json={"subject": "test"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Email not found"}

def test_get_emails_db_error(client, mock_db_manager):
    # Dynamically create a mock error to avoid a hard dependency on psycopg2
    class MockDBError(Exception):
        pass

    mock_db_manager.get_all_emails.side_effect = MockDBError("Database connection failed")

    response = client.get("/api/emails")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database service unavailable."}