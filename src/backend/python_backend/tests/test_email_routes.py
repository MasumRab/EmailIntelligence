from datetime import datetime
from unittest.mock import MagicMock

import pytest


def create_mock_email(email_id: int, subject: str, **kwargs) -> dict:
    """Helper to create a valid mock email dictionary."""
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


def test_create_email(client, mock_db_manager, mock_workflow_engine):
    new_email_data = {
        "sender": "new@example.com",
        "senderEmail": "new@example.com",
        "subject": "New Email",
        "content": "Email content",
        "time": datetime.now().isoformat(),
    }

    processed_data_from_workflow = new_email_data.copy()
    processed_data_from_workflow.update(
        {
            "confidence": 95,
            "categoryId": 1,
            "labels": ["test"],
            "analysisMetadata": {"some_ai_field": "value"},
            "filterResults": {"actions_taken": []},
            "workflow_status": "processed_by_default_workflow",
        }
    )
    mock_workflow_engine.run_workflow.return_value = processed_data_from_workflow

    # The database receives the processed data. We need to pop the subject
    # because it's a positional argument in the helper.
    subject = processed_data_from_workflow.pop("subject")
    created_email_from_db = create_mock_email(1, subject, **processed_data_from_workflow)
    mock_db_manager.create_email.return_value = created_email_from_db

    # Restore the subject for the original dictionary that we'll check against
    processed_data_from_workflow["subject"] = subject

    response = client.post("/api/emails", json=new_email_data)

    assert response.status_code == 200
    assert response.json()["subject"] == "New Email"

    # Assert that run_workflow was called once.
    mock_workflow_engine.run_workflow.assert_called_once()

    # Inspect the arguments to check the core data.
    call_args, _ = mock_workflow_engine.run_workflow.call_args
    workflow_input_data = call_args[0]
    assert workflow_input_data["subject"] == new_email_data["subject"]
    assert workflow_input_data["content"] == new_email_data["content"]

    # Verify the database was called with the processed data.
    mock_db_manager.create_email.assert_called_once_with(processed_data_from_workflow)


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
    class MockDBError(Exception):
        pass

    mock_db_manager.get_all_emails.side_effect = MockDBError("Database connection failed")

    response = client.get("/api/emails")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database service unavailable."}


def test_plugin_workflow_e2e(client_with_real_workflows, mock_db_manager, mock_ai_engine):
    """
    Tests the full end-to-end flow of activating and using a workflow from a plugin.
    This uses a client with a real workflow engine to test discovery.
    """
    # 1. Activate the workflow from the example plugin
    activate_response = client_with_real_workflows.put("/api/workflows/active/example_uppercase")
    assert activate_response.status_code == 200
    assert (
        activate_response.json()["message"] == "Active legacy workflow set to 'example_uppercase'."
    )

    # 2. Prepare the email data
    new_email_data = {
        "sender": "plugin.test@example.com",
        "senderEmail": "plugin.test@example.com",
        "subject": "a subject to be uppercased",
        "content": "This is a test of the plugin workflow.",
        "time": datetime.now().isoformat(),
    }

    # The database create_email method needs to be mocked to return a valid email dictionary
    # The real workflow will add 'workflow_status' and change the subject.
    processed_data = new_email_data.copy()
    processed_data["subject"] = "A SUBJECT TO BE UPPERCASED"
    processed_data["workflow_status"] = "processed_by_example_uppercase_workflow"

    # We need to mock the return value from the db create call
    mock_db_manager.create_email.return_value = create_mock_email(10, **processed_data)

    # 3. Create the email, which will trigger the newly activated workflow
    create_response = client_with_real_workflows.post("/api/emails", json=new_email_data)

    # 4. Assert that the workflow was correctly applied
    assert create_response.status_code == 200
    response_data = create_response.json()
    assert response_data["subject"] == "A SUBJECT TO BE UPPERCASED"

    # Also assert that the AI engine was NOT called, since the uppercase workflow doesn't use it
    mock_ai_engine.analyze_email.assert_not_called()
