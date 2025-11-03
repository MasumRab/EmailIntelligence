import pytest
from unittest.mock import AsyncMock, patch
import json


@pytest.mark.asyncio
async def test_user_registration(client, mock_db_manager: AsyncMock):
    """Test user registration endpoint."""
    # Mock the database to return an empty users list (user doesn't exist)
    mock_db_manager.users_data = []
    mock_db_manager._save_data = AsyncMock()
    
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login(client, mock_db_manager: AsyncMock):
    """Test user login endpoint."""
    # Mock the database with a user that has a hashed password
    mock_db_manager.users_data = [
        {
            "id": 1,
            "username": "testuser",
            "hashed_password": "salted_hash_here",  # This would be a real hash in practice
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
    ]
    
    # Mock the verify_password function to return True
    with patch('src.core.auth.verify_password', return_value=True):
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login_invalid_credentials(client, mock_db_manager: AsyncMock):
    """Test user login with invalid credentials."""
    # Mock the database with a user
    mock_db_manager.users_data = [
        {
            "id": 1,
            "username": "testuser",
            "hashed_password": "salted_hash_here",
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
    ]
    
    # Mock the verify_password function to return False
    with patch('src.core.auth.verify_password', return_value=False):
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
    
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_protected_endpoint_without_auth(client):
    """Test that protected endpoints require authentication."""
    response = client.get("/api/emails")
    assert response.status_code == 403 or response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_auth(client, mock_db_manager: AsyncMock):
    """Test that protected endpoints work with valid authentication."""
    # Mock the database with an email
    mock_email = {
        "id": 1,
        "messageId": "msg1",
        "threadId": "thread1",
        "sender": "test@example.com",
        "senderEmail": "test@example.com",
        "subject": "Test Email",
        "content": "Test content",
        "preview": "Test preview",
        "time": "2023-01-01T00:00:00",
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
    
    mock_db_manager.get_all_emails = AsyncMock(return_value=[mock_email])
    
    # First, get a token
    mock_db_manager.users_data = [
        {
            "id": 1,
            "username": "testuser",
            "hashed_password": "salted_hash_here",
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
    ]
    
    with patch('src.core.auth.verify_password', return_value=True):
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword"
            }
        )
        
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Now test the protected endpoint with the token
    response = client.get(
        "/api/emails",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_legacy_token_endpoint(client, mock_db_manager: AsyncMock):
    """Test the legacy token endpoint."""
    # Mock the database with a user
    mock_db_manager.users_data = [
        {
            "id": 1,
            "username": "testuser",
            "hashed_password": "salted_hash_here",
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
    ]
    
    # Mock the verify_password function to return True
    with patch('src.core.auth.verify_password', return_value=True):
        response = client.post(
            "/token",
            data={
                "username": "testuser",
                "password": "testpassword"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"