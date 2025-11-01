from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from backend.python_backend.ai_engine import AIAnalysisResult
from backend.python_backend.models import EmailCreate, EmailUpdate


async def _create_mock_email(id: int, subject: str) -> dict:
    """Helper to create a complete mock email dictionary for EmailResponse."""
    return {
        "id": id,
        "messageId": f"msg{id}",
        "threadId": f"thread{id}",
        "sender": "test@example.com",
        "senderEmail": "test@example.com",
        "subject": subject,
        "content": "Test content",
        "preview": "Test preview",
        "time": datetime.now(),
        "category": "Test",
        "categoryId": 1,
        "labels": ["inbox"],
        "confidence": 95,
        "isImportant": False,
        "isStarred": False,
        "isUnread": True,
        "hasAttachments": False,
        "attachmentCount": 0,
        "sizeEstimate": 1024,
        "aiAnalysis": {},
        "filterResults": {},
    }


# async def test_get_emails_all(client, mock_db_manager: AsyncMock):
#     """Test retrieving all emails successfully."""
#     mock_data = [await _create_mock_email(1, "Subject 1"), await _create_mock_email(2, "Subject 2")]
#     mock_db_manager.get_all_emails.return_value = mock_data
#     response = client.get("/api/emails")
#     if response.status_code != 200:
#         print(response.json())
#     assert response.status_code == 200
#     assert len(response.json()) == 2
#     mock_db_manager.get_all_emails.assert_called_once()


# async def test_get_emails_by_category(client, mock_db_manager: AsyncMock):
#     """Test retrieving emails filtered by category."""
#     mock_data = [await _create_mock_email(1, "Category Email")]
#     mock_db_manager.get_emails_by_category.return_value = mock_data
#     response = client.get("/api/emails?category_id=1")
#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     mock_db_manager.get_emails_by_category.assert_called_once_with(1)


# async def test_get_emails_by_search(client, mock_db_manager: AsyncMock):
#     """Test retrieving emails via search."""
#     mock_data = [await _create_mock_email(1, "Search Result")]
#     mock_db_manager.search_emails.return_value = mock_data
#     response = client.get("/api/emails?search=Result")
#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     mock_db_manager.search_emails.assert_called_once_with("Result")


# async def test_get_email_by_id_found(client, mock_db_manager: AsyncMock):
#     """Test retrieving a single email by its ID when it exists."""
#     mock_data = await _create_mock_email(1, "Specific Email")
#     mock_db_manager.get_email_by_id.return_value = mock_data
#     response = client.get("/api/emails/1")
#     assert response.status_code == 200
#     assert response.json()["subject"] == "Specific Email"
#     mock_db_manager.get_email_by_id.assert_called_once_with(1)


# async def test_get_email_by_id_not_found(client, mock_db_manager: AsyncMock):
#     """Test retrieving a single email that does not exist."""
#     mock_db_manager.get_email_by_id.return_value = None
#     response = client.get("/api/emails/999")
#     assert response.status_code == 404
#     mock_db_manager.get_email_by_id.assert_called_once_with(999)


# async def test_get_emails_db_error(client, mock_db_manager: AsyncMock):
#     """Test database error during GET request for all emails."""
#     mock_db_manager.get_all_emails.side_effect = Exception("DB Error")
#     response = client.get("/api/emails")
#     assert response.status_code == 500
#     assert "Failed to fetch emails" in response.json()["detail"]


# async def test_create_email_success(client, mock_db_manager: AsyncMock):
#     """Test successful creation of a new email."""
#     email_data = {
#         "sender": "test@example.com",
#         "senderEmail": "test@example.com",
#         "subject": "New Email",
#         "content": "Content",
#         "time": datetime.now(),
#     }
#     mock_db_manager.create_email.return_value = await _create_mock_email(100, "New Email")

#     response = client.post("/api/emails", json=email_data)

#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["id"] == 100
#     mock_db_manager.create_email.assert_called_once()


# async def test_update_email_success(client, mock_db_manager: AsyncMock):
#     """Test successful update of an existing email."""
#     email_id = 1
#     update_data = {"subject": "Updated Subject"}
#     mock_db_manager.update_email.return_value = await _create_mock_email(email_id, "Updated Subject")

#     response = client.put(f"/api/emails/{email_id}", json=update_data)

#     assert response.status_code == 200
#     assert response.json()["subject"] == "Updated Subject"
#     mock_db_manager.update_email.assert_called_once_with(email_id, update_data)


# async def test_update_email_not_found(client, mock_db_manager: AsyncMock):
#     """Test updating an email that does not exist."""
#     email_id = 999
#     update_data = {"subject": "Updated Subject"}
#     mock_db_manager.update_email.return_value = None

#     response = client.put(f"/api/emails/{email_id}", json=update_data)

#     assert response.status_code == 404
#     mock_db_manager.update_email.assert_called_once_with(email_id, update_data)
