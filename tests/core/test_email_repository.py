from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.data.database_source import DatabaseDataSource
from src.core.data.repository import DatabaseEmailRepository


@pytest.fixture
def mock_db_manager():
    """Fixture to create a mock DatabaseManager."""
    mock = MagicMock()
    mock.get_emails = AsyncMock(return_value=[{"id": 1, "subject": "Test Email"}])
    mock.get_email_by_id = AsyncMock(return_value={"id": 1, "subject": "Test Email"})
    mock.search_emails_with_limit = AsyncMock(return_value=[{"id": 1, "subject": "Test Email"}])
    mock.create_email = AsyncMock(return_value={"id": 2, "subject": "New Email"})
    mock.update_email = AsyncMock(return_value={"id": 1, "subject": "Updated Email"})
    return mock


@pytest.fixture
def db_data_source(mock_db_manager):
    """Fixture to create a DatabaseDataSource with a mock DatabaseManager."""
    return DatabaseDataSource(mock_db_manager)


@pytest.fixture
def email_repository(db_data_source):
    """Fixture to create an EmailRepository with a mock DatabaseDataSource."""
    return DatabaseEmailRepository(db_data_source)


@pytest.mark.asyncio
async def test_get_emails(email_repository, mock_db_manager):
    """Test that get_emails calls the data source correctly."""
    await email_repository.get_emails(limit=50, offset=10, category_id=1, is_unread=True)
    mock_db_manager.get_emails.assert_called_once_with(
        limit=50, offset=10, category_id=1, is_unread=True
    )


@pytest.mark.asyncio
async def test_get_email_by_id(email_repository, mock_db_manager):
    """Test that get_email_by_id calls the data source correctly."""
    await email_repository.get_email_by_id(1)
    mock_db_manager.get_email_by_id.assert_called_once_with(1, include_content=True)


@pytest.mark.asyncio
async def test_search_emails(email_repository, mock_db_manager):
    """Test that search_emails calls the data source correctly."""
    await email_repository.search_emails("test")
    mock_db_manager.search_emails_with_limit.assert_called_once_with("test", limit=50)


@pytest.mark.asyncio
async def test_create_email(email_repository, mock_db_manager):
    """Test that create_email calls the data source correctly."""
    email_data = {"subject": "New Email"}
    await email_repository.create_email(email_data)
    mock_db_manager.create_email.assert_called_once_with(email_data)


@pytest.mark.asyncio
async def test_update_email(email_repository, mock_db_manager):
    """Test that update_email calls the data source correctly."""
    email_data = {"subject": "Updated Email"}
    await email_repository.update_email(1, email_data)
    mock_db_manager.update_email.assert_called_once_with(1, email_data)
