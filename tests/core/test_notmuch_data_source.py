"""
Tests for NotmuchDataSource implementation.

This module contains comprehensive tests for the NotmuchDataSource class,
which provides a functional implementation of the DataSource interface for Notmuch.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from src.core.notmuch_data_source import NotmuchDataSource
from src.core.database import DatabaseManager


class TestNotmuchDataSourceInitialization:
    """Test NotmuchDataSource initialization and basic properties."""

    @patch("src.core.notmuch_data_source.notmuch")
    def test_notmuch_data_source_creation(self, mock_notmuch):
        """Test that NotmuchDataSource can be created."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        ds = NotmuchDataSource()
        assert ds is not None
        assert isinstance(ds, NotmuchDataSource)

    @patch("src.core.notmuch_data_source.notmuch")
    def test_notmuch_data_source_inherits_from_data_source(self, mock_notmuch):
        """Test that NotmuchDataSource properly inherits from DataSource."""
        from src.core.data_source import DataSource

        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        ds = NotmuchDataSource(db_manager=AsyncMock(spec=DatabaseManager))
        assert isinstance(ds, DataSource)


class TestNotmuchDataSourceEmailOperations:
    """Test email-related operations in NotmuchDataSource."""

    @pytest.fixture
    def mock_db_manager(self):
        """Create a mocked DatabaseManager instance for NotmuchDataSource."""
        db_manager = AsyncMock(spec=DatabaseManager)
        db_manager._ensure_initialized = AsyncMock()
        return db_manager

    @pytest.fixture
    @patch("src.core.notmuch_data_source.notmuch")
    def data_source(self, mock_notmuch, mock_db_manager):
        """Create a fresh NotmuchDataSource for each test."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db
        return NotmuchDataSource(db_manager=mock_db_manager)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_create_email(self, mock_notmuch):
        """Test create_email method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        email_data = {
            "subject": "Test Email",
            "content": "This is test content",
            "sender": "test@example.com",
        }

        result = await data_source.create_email(email_data)

        # Should return None (read-only implementation)
        assert result is None

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_email_by_id(self, mock_notmuch):
        """Test get_email_by_id method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.get_email_by_id(123)

        assert result is None  # Not implemented for notmuch (uses message IDs instead)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_email_by_id_without_content(self, mock_notmuch):
        """Test get_email_by_id with include_content=False."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.get_email_by_id(123, include_content=False)

        assert result is None  # Not implemented for notmuch (uses message IDs instead)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_all_emails(self, mock_notmuch):
        """Test get_all_emails method."""
        # Mock the notmuch database with search results
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_message = MagicMock()

        mock_message.get_message_id.return_value = "test@example.com"
        mock_message.get_header.side_effect = lambda x: {
            "subject": "Test Subject",
            "from": "sender@example.com",
        }.get(x, "")
        mock_message.get_date.return_value = 1234567890
        mock_message.get_tags.return_value = ["inbox", "unread"]

        mock_query.search_messages.return_value = [mock_message]
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.get_all_emails()

        assert isinstance(result, list)
        # The result will depend on the mock setup

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_all_emails_with_parameters(self, mock_notmuch):
        """Test get_all_emails with limit and offset."""
        # Mock the notmuch database with search results
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_message = MagicMock()

        mock_message.get_message_id.return_value = "test2@example.com"
        mock_message.get_header.side_effect = lambda x: {
            "subject": "Test Subject 2",
            "from": "sender2@example.com",
        }.get(x, "")
        mock_message.get_date.return_value = 1234567891
        mock_message.get_tags.return_value = ["inbox"]

        mock_query.search_messages.return_value = [mock_message]
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.get_all_emails(limit=25, offset=10)

        assert isinstance(result, list)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_update_email(self, mock_notmuch):
        """Test update_email method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        update_data = {"is_read": True, "tags": ["important"]}
        result = await data_source.update_email(123, update_data)

        assert result is None  # Not implemented for read-only source

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_delete_email(self, mock_notmuch):
        """Test delete_email method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.delete_email(123)

        assert result is False  # Not implemented for read-only source


class TestNotmuchDataSourceSearchOperations:
    """Test search and query operations in NotmuchDataSource."""

    @pytest.fixture
    def mock_db_manager(self):
        """Create a mocked DatabaseManager instance for NotmuchDataSource."""
        db_manager = AsyncMock(spec=DatabaseManager)
        db_manager._ensure_initialized = AsyncMock()
        return db_manager

    @pytest.fixture
    @patch("src.core.notmuch_data_source.notmuch")
    def data_source(self, mock_notmuch, mock_db_manager):
        """Create a fresh NotmuchDataSource for each test."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db
        return NotmuchDataSource(db_manager=mock_db_manager)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_search_emails(self, mock_notmuch):
        """Test search_emails method."""
        # Mock the notmuch database with search results
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_message = MagicMock()

        mock_message.get_message_id.return_value = "search@example.com"
        mock_message.get_header.side_effect = lambda x: {
            "subject": "Search Result",
            "from": "searcher@example.com",
        }.get(x, "")
        mock_message.get_date.return_value = 1234567892
        mock_message.get_tags.return_value = ["search", "result"]

        mock_query.search_messages.return_value = [mock_message]
        mock_query.count_messages.return_value = 1
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.search_emails("important meeting")

        assert isinstance(result, list)
        # Should return results based on mock

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_search_emails_empty_query(self, mock_notmuch):
        """Test search_emails with empty query."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_query.search_messages.return_value = []
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.search_emails("")

        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_emails_by_category(self, mock_notmuch):
        """Test get_emails_by_category method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.get_emails_by_category("work")

        assert isinstance(result, list)
        assert len(result) == 0  # Not implemented for notmuch (uses string tags)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_emails_with_filters(self, mock_notmuch):
        """Test get_emails method with various filters."""
        # Mock the notmuch database with search results
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_message = MagicMock()

        mock_message.get_message_id.return_value = "filtered@example.com"
        mock_message.get_header.side_effect = lambda x: {
            "subject": "Filtered Email",
            "from": "filter@example.com",
        }.get(x, "")
        mock_message.get_date.return_value = 1234567893
        mock_message.get_tags.return_value = ["inbox", "unread"]

        mock_query.search_messages.return_value = [mock_message]
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource(db_manager=AsyncMock(spec=DatabaseManager))
        result = await data_source.get_emails(
            limit=20, offset=5, category_id=1, is_unread=True
        )

        assert isinstance(result, list)


class TestNotmuchDataSourceCategoryOperations:
    """Test category-related operations in NotmuchDataSource."""

    @pytest.fixture
    def mock_db_manager(self):
        """Create a mocked DatabaseManager instance for NotmuchDataSource."""
        db_manager = AsyncMock(spec=DatabaseManager)
        db_manager._ensure_initialized = AsyncMock()
        return db_manager

    @pytest.fixture
    @patch("src.core.notmuch_data_source.notmuch")
    def data_source(self, mock_notmuch, mock_db_manager):
        """Create a fresh NotmuchDataSource for each test."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db
        return NotmuchDataSource(db_manager=mock_db_manager)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_all_categories(self, mock_notmuch):
        """Test get_all_categories method."""
        # Mock the notmuch database with tags
        mock_db = MagicMock()
        mock_db.get_all_tags.return_value = ["inbox", "work", "personal"]
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        result = await data_source.get_all_categories()

        assert isinstance(result, list)
        # Should return tags as categories

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_create_category(self, mock_notmuch):
        """Test create_category method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        category_data = {
            "name": "Important",
            "color": "#FF0000",
            "description": "High priority emails",
        }

        result = await data_source.create_category(category_data)

        assert result is None  # Not implemented for read-only source


class TestNotmuchDataSourceMessageOperations:
    """Test message ID-based operations in NotmuchDataSource."""

    @pytest.fixture
    def mock_db_manager(self):
        """Create a mocked DatabaseManager instance for NotmuchDataSource."""
        db_manager = AsyncMock(spec=DatabaseManager)
        db_manager._ensure_initialized = AsyncMock()
        return db_manager

    @pytest.fixture
    @patch("src.core.notmuch_data_source.notmuch")
    def data_source(self, mock_notmuch, mock_db_manager):
        """Create a fresh NotmuchDataSource for each test."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db
        return NotmuchDataSource(db_manager=mock_db_manager)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_email_by_message_id(self, mock_notmuch):
        """Test get_email_by_message_id method."""
        # Mock the notmuch database with a message
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_message = MagicMock()

        mock_message.get_message_id.return_value = "<abc123@example.com>"
        mock_message.get_header.side_effect = lambda x: {
            "subject": "Test Message",
            "from": "sender@example.com",
            "to": "recipient@example.com",
        }.get(x, "")
        mock_message.get_date.return_value = 1234567894
        mock_message.get_tags.return_value = ["inbox"]
        mock_message.get_filename.return_value = "/tmp/test.eml"

        mock_query.search_messages.return_value = [mock_message]
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        # Mock the email file reading
        import builtins

        original_open = builtins.open

        def mock_open(filename, *args, **kwargs):
            if filename == "/tmp/test.eml":
                mock_file = MagicMock()
                mock_file.__enter__ = lambda: mock_file
                mock_file.__exit__ = lambda *args: None
                mock_file.read.return_value = (
                    "Subject: Test Message\n\nThis is the content."
                )
                return mock_file
            return original_open(filename, *args, **kwargs)

        with patch("builtins.open", side_effect=mock_open):
            data_source = NotmuchDataSource(db_manager=AsyncMock(spec=DatabaseManager))
            message_id = "<abc123@example.com>"
            result = await data_source.get_email_by_message_id(message_id)

            assert result is not None
            assert result["message_id"] == "<abc123@example.com>"

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_email_by_message_id_without_content(self, mock_notmuch):
        """Test get_email_by_message_id with include_content=False."""
        # Mock the notmuch database with a message
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_message = MagicMock()

        mock_message.get_message_id.return_value = "<abc123@example.com>"
        mock_message.get_header.side_effect = lambda x: {
            "subject": "Test Message",
            "from": "sender@example.com",
            "to": "recipient@example.com",
        }.get(x, "")
        mock_message.get_date.return_value = 1234567894
        mock_message.get_tags.return_value = ["inbox"]
        mock_message.get_filename.return_value = "/tmp/test.eml"

        mock_query.search_messages.return_value = [mock_message]
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        # Mock the email file reading
        import builtins

        original_open = builtins.open

        def mock_open(filename, *args, **kwargs):
            if filename == "/tmp/test.eml":
                mock_file = MagicMock()
                mock_file.__enter__ = lambda: mock_file
                mock_file.__exit__ = lambda *args: None
                mock_file.read.return_value = (
                    "Subject: Test Message\n\nThis is the content."
                )
                return mock_file
            return original_open(filename, *args, **kwargs)

        with patch("builtins.open", side_effect=mock_open):
            data_source = NotmuchDataSource(db_manager=AsyncMock(spec=DatabaseManager))
            message_id = "<abc123@example.com>"
            result = await data_source.get_email_by_message_id(
                message_id, include_content=False
            )

            assert result is not None

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_update_email_by_message_id(self, mock_notmuch):
        """Test update_email_by_message_id method."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource()
        message_id = "<abc123@example.com>"
        update_data = {"tags": ["replied"], "is_read": True}

        result = await data_source.update_email_by_message_id(message_id, update_data)

        assert result is None  # Not implemented for read-only source


class TestNotmuchDataSourceDashboard:
    """Test dashboard statistics operations in NotmuchDataSource."""

    @pytest.fixture
    def mock_db_manager(self):
        """Create a mocked DatabaseManager instance for NotmuchDataSource."""
        db_manager = AsyncMock(spec=DatabaseManager)
        db_manager._ensure_initialized = AsyncMock()
        return db_manager

    @pytest.fixture
    @patch("src.core.notmuch_data_source.notmuch")
    def data_source(self, mock_notmuch, mock_db_manager):
        """Create a fresh NotmuchDataSource for each test."""
        # Mock the notmuch database
        mock_db = MagicMock()
        mock_notmuch.Database.return_value = mock_db
        return NotmuchDataSource(db_manager=mock_db_manager)

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_dashboard_aggregates(self, mock_notmuch):
        """Test get_dashboard_aggregates method."""
        # Mock the notmuch database with query results
        mock_db = MagicMock()
        mock_query = MagicMock()

        # Mock query counts
        mock_query.count_messages.side_effect = [
            100,
            20,
            15,
            5,
        ]  # total, unread, auto-labeled, categories
        mock_db.create_query.return_value = mock_query
        mock_db.get_all_tags.return_value = [
            "inbox",
            "work",
            "personal",
            "unread",
            "sent",
        ]
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource(db_manager=AsyncMock(spec=DatabaseManager))
        result = await data_source.get_dashboard_aggregates()

        assert isinstance(result, dict)
        assert "total_emails" in result
        assert "auto_labeled" in result
        assert "categories_count" in result
        assert "unread_count" in result
        assert "weekly_growth" in result

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_category_breakdown(self, mock_notmuch):
        """Test get_category_breakdown method."""
        # Mock the notmuch database with tags and query results
        mock_db = MagicMock()
        mock_query = MagicMock()

        # Mock tags and query counts
        mock_db.get_all_tags.return_value = [
            "work",
            "personal",
            "inbox",
            "unread",
            "project",
        ]
        mock_query.count_messages.side_effect = [
            30,
            20,
            15,
            10,
            5,
        ]  # Counts for each tag
        mock_db.create_query.return_value = mock_query
        mock_notmuch.Database.return_value = mock_db

        data_source = NotmuchDataSource(db_manager=AsyncMock(spec=DatabaseManager))
        result = await data_source.get_category_breakdown(limit=5)

        assert isinstance(result, dict)
        # Should return category breakdown based on tags

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_dashboard_aggregates_no_db(self, mock_notmuch):
        """Test get_dashboard_aggregates method when database is not available."""
        # Mock the notmuch database as None
        mock_notmuch.Database.return_value = None

        data_source = NotmuchDataSource()
        result = await data_source.get_dashboard_aggregates()

        assert isinstance(result, dict)
        assert result["total_emails"] == 0
        assert result["auto_labeled"] == 0

    @pytest.mark.asyncio
    @patch("src.core.notmuch_data_source.notmuch")
    async def test_get_category_breakdown_no_db(self, mock_notmuch):
        """Test get_category_breakdown method when database is not available."""
        # Mock the notmuch database as None
        mock_notmuch.Database.return_value = None

        data_source = NotmuchDataSource()
        result = await data_source.get_category_breakdown(limit=5)

        assert isinstance(result, dict)
        assert len(result) == 0
