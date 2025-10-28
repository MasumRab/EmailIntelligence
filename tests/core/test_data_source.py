"""
Tests for DataSource abstraction layer.

This module contains comprehensive unit tests for the DataSource abstract base class
and its implementations, ensuring proper interface compliance and functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, List, Any, Optional

from src.core.data_source import DataSource
from src.core.notmuch_data_source import NotmuchDataSource
from src.core.database import DatabaseManager


class TestDataSourceInterface:
    """Test the DataSource abstract base class interface."""

    def test_data_source_is_abstract(self):
        """Test that DataSource cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DataSource()

    def test_data_source_has_abstract_methods(self):
        """Test that all required abstract methods are defined."""
        # Check that these methods exist and are abstract
        required_methods = [
            'create_email',
            'get_email_by_id',
            'get_all_categories',
            'create_category',
            'get_emails',
            'update_email_by_message_id',
            'get_email_by_message_id',
            'get_all_emails',
            'search_emails',
            'get_emails_by_category',
            'update_email',
            'delete_email'
        ]

        for method_name in required_methods:
            assert hasattr(DataSource, method_name), f"Missing abstract method: {method_name}"


class TestNotmuchDataSource:
    """Test the NotmuchDataSource implementation."""

    @pytest.fixture
    def notmuch_ds(self):
        """Create a NotmuchDataSource instance."""
        return NotmuchDataSource()

    @pytest.mark.asyncio
    async def test_create_email(self, notmuch_ds):
        """Test create_email method."""
        email_data = {"subject": "Test", "content": "Test content"}
        result = await notmuch_ds.create_email(email_data)
        assert result is None  # Mock implementation returns None

    @pytest.mark.asyncio
    async def test_get_email_by_id(self, notmuch_ds):
        """Test get_email_by_id method."""
        result = await notmuch_ds.get_email_by_id(1)
        assert result is None  # Mock implementation returns None

    @pytest.mark.asyncio
    async def test_get_all_categories(self, notmuch_ds):
        """Test get_all_categories method."""
        result = await notmuch_ds.get_all_categories()
        assert isinstance(result, list)
        assert len(result) == 0  # Mock implementation returns empty list

    @pytest.mark.asyncio
    async def test_create_category(self, notmuch_ds):
        """Test create_category method."""
        category_data = {"name": "Test Category"}
        result = await notmuch_ds.create_category(category_data)
        assert result is None  # Mock implementation returns None

    @pytest.mark.asyncio
    async def test_get_emails(self, notmuch_ds):
        """Test get_emails method with various parameters."""
        # Test default parameters
        result = await notmuch_ds.get_emails()
        assert isinstance(result, list)
        assert len(result) == 0

        # Test with parameters
        result = await notmuch_ds.get_emails(limit=10, offset=5, category_id=1, is_unread=True)
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_all_emails(self, notmuch_ds):
        """Test get_all_emails method."""
        result = await notmuch_ds.get_all_emails()
        assert isinstance(result, list)
        assert len(result) == 0

        # Test with parameters
        result = await notmuch_ds.get_all_emails(limit=25, offset=10)
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_search_emails(self, notmuch_ds):
        """Test search_emails method."""
        result = await notmuch_ds.search_emails("test query")
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_emails_by_category(self, notmuch_ds):
        """Test get_emails_by_category method."""
        result = await notmuch_ds.get_emails_by_category("work")
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_update_email(self, notmuch_ds):
        """Test update_email method."""
        update_data = {"is_read": True}
        result = await notmuch_ds.update_email(1, update_data)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_email(self, notmuch_ds):
        """Test delete_email method."""
        result = await notmuch_ds.delete_email(1)
        assert result is None

    @pytest.mark.asyncio
    async def test_interface_compliance(self, notmuch_ds):
        """Test that NotmuchDataSource properly implements DataSource interface."""
        # All methods should exist and be callable
        methods_to_test = [
            ('create_email', [{"test": "data"}]),
            ('get_email_by_id', [1]),
            ('get_all_categories', []),
            ('create_category', [{"name": "test"}]),
            ('get_emails', []),
            ('get_all_emails', []),
            ('search_emails', ["query"]),
            ('get_emails_by_category', ["test"]),
            ('update_email', [1, {"test": "update"}]),
            ('delete_email', [1]),
        ]

        for method_name, args in methods_to_test:
            method = getattr(notmuch_ds, method_name)
            assert callable(method), f"Method {method_name} is not callable"

            # Test that method can be called (even if it returns None/empty)
            if args:
                result = await method(*args)
            else:
                result = await method()

            # Result should be of expected type (None for single items, list for collections)
            if method_name in ['get_all_categories', 'get_emails', 'get_all_emails', 'search_emails', 'get_emails_by_category']:
                assert isinstance(result, list)
            else:
                assert result is None or isinstance(result, dict)


class TestDatabaseManagerDataSource:
    """Test DatabaseManager as a DataSource implementation."""

    @pytest.fixture
    def mock_db_manager(self):
        """Create a mocked DatabaseManager instance."""
        db_manager = DatabaseManager()

        # Mock the database connection and operations
        db_manager._db = AsyncMock()
        db_manager._ensure_initialized = AsyncMock()

        return db_manager

    @pytest.mark.asyncio
    async def test_database_manager_implements_datasource(self, mock_db_manager):
        """Test that DatabaseManager properly implements DataSource interface."""
        # Should have all required methods
        required_methods = [
            'create_email', 'get_email_by_id', 'get_all_categories', 'create_category',
            'get_emails', 'update_email_by_message_id', 'get_email_by_message_id',
            'get_all_emails', 'search_emails', 'get_emails_by_category',
            'update_email', 'delete_email'
        ]

        for method_name in required_methods:
            assert hasattr(mock_db_manager, method_name), f"Missing method: {method_name}"
            assert callable(getattr(mock_db_manager, method_name)), f"Method {method_name} is not callable"

    @pytest.mark.asyncio
    async def test_database_manager_create_email(self, mock_db_manager):
        """Test DatabaseManager create_email method."""
        mock_db_manager._db.create_email = AsyncMock(return_value={"id": 1, "subject": "Test"})

        email_data = {"subject": "Test Email", "content": "Test content"}
        result = await mock_db_manager.create_email(email_data)

        mock_db_manager._db.create_email.assert_called_once_with(email_data)
        assert result == {"id": 1, "subject": "Test"}

    @pytest.mark.asyncio
    async def test_database_manager_get_email_by_id(self, mock_db_manager):
        """Test DatabaseManager get_email_by_id method."""
        mock_db_manager._db.get_email_by_id = AsyncMock(return_value={"id": 1, "subject": "Test"})

        result = await mock_db_manager.get_email_by_id(1)

        mock_db_manager._db.get_email_by_id.assert_called_once_with(1, True)
        assert result == {"id": 1, "subject": "Test"}

    @pytest.mark.asyncio
    async def test_database_manager_get_email_by_id_without_content(self, mock_db_manager):
        """Test DatabaseManager get_email_by_id method without content."""
        mock_db_manager._db.get_email_by_id = AsyncMock(return_value={"id": 1, "subject": "Test"})

        result = await mock_db_manager.get_email_by_id(1, include_content=False)

        mock_db_manager._db.get_email_by_id.assert_called_once_with(1, False)
        assert result == {"id": 1, "subject": "Test"}


class TestDataSourceFactory:
    """Test the data source factory functions."""

    @pytest.mark.asyncio
    async def test_get_data_source_default(self, monkeypatch):
        """Test get_data_source with default configuration."""
<<<<<<< HEAD
        from src.core.factory import get_data_source
=======
        from src.core.factory import get_data_source, _data_source_instance
>>>>>>> c51e307b (feat: complete 6 HIGH priority tasks)

        # Reset global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment variable
        monkeypatch.setenv("DATA_SOURCE_TYPE", "default")

        # Mock DatabaseManager
        mock_db = AsyncMock()
        mock_db._ensure_initialized = AsyncMock()

        with monkeypatch.context() as m:
            m.setattr("src.core.factory.DatabaseManager", lambda: mock_db)

            data_source = await get_data_source()
            assert data_source is mock_db

    @pytest.mark.asyncio
    async def test_get_data_source_notmuch(self, monkeypatch):
        """Test get_data_source with notmuch configuration."""
<<<<<<< HEAD
        from src.core.factory import get_data_source
=======
        from src.core.factory import get_data_source, _data_source_instance
>>>>>>> c51e307b (feat: complete 6 HIGH priority tasks)

        # Reset global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment variable
        monkeypatch.setenv("DATA_SOURCE_TYPE", "notmuch")

        data_source = await get_data_source()
        assert isinstance(data_source, NotmuchDataSource)

    @pytest.mark.asyncio
    async def test_get_data_source_singleton(self, monkeypatch):
        """Test that get_data_source returns singleton instance."""
<<<<<<< HEAD
        from src.core.factory import get_data_source
=======
        from src.core.factory import get_data_source, _data_source_instance
>>>>>>> c51e307b (feat: complete 6 HIGH priority tasks)

        # Reset global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment variable
        monkeypatch.setenv("DATA_SOURCE_TYPE", "notmuch")

        # Get first instance
        ds1 = await get_data_source()
        # Get second instance
        ds2 = await get_data_source()

        # Should be the same instance
        assert ds1 is ds2
        assert isinstance(ds1, NotmuchDataSource)


class TestDataSourceIntegration:
    """Integration tests for data source implementations."""

    @pytest.mark.asyncio
    async def test_notmuch_datasource_method_signatures(self):
        """Test that NotmuchDataSource methods have correct signatures."""
        ds = NotmuchDataSource()

        # Test method signatures match the abstract base class
        import inspect

        # Check a few key methods
        sig_create = inspect.signature(ds.create_email)
        assert 'email_data' in sig_create.parameters

        sig_get_emails = inspect.signature(ds.get_emails)
        assert 'limit' in sig_get_emails.parameters
        assert 'offset' in sig_get_emails.parameters
        assert 'category_id' in sig_get_emails.parameters
        assert 'is_unread' in sig_get_emails.parameters

    @pytest.mark.asyncio
    async def test_datasource_polymorphism(self):
        """Test that different data sources can be used interchangeably."""
        # Create instances of different data source types
        notmuch_ds = NotmuchDataSource()

        # Both should implement the same interface
        methods = ['create_email', 'get_email_by_id', 'get_all_emails', 'search_emails']

        for method_name in methods:
            assert hasattr(notmuch_ds, method_name)
            method = getattr(notmuch_ds, method_name)
            assert callable(method)

    @pytest.mark.asyncio
    async def test_error_handling_in_mocked_datasource(self):
        """Test error handling in data source operations."""
        ds = NotmuchDataSource()

        # All operations should complete without throwing exceptions
        # (even if they return None/empty results)

        try:
            await ds.create_email({})
            await ds.get_email_by_id(1)
            await ds.get_all_emails()
            await ds.search_emails("test")
            await ds.update_email(1, {})
            await ds.delete_email(1)
        except Exception as e:
            pytest.fail(f"Data source operation raised unexpected exception: {e}")
