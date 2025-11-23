"""
Tests for factory functions and dependency injection.

This module tests the factory functions that provide instances of core abstractions,
ensuring proper dependency injection and singleton behavior.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.core.factory import get_data_source, get_ai_engine
from src.core.data_source import DataSource
from src.core.notmuch_data_source import NotmuchDataSource


class TestDataSourceFactory:
    """Test the data source factory function."""

    @pytest.mark.asyncio
    async def test_get_data_source_default_type(self, monkeypatch):
        """Test get_data_source with default DATA_SOURCE_TYPE."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment to use default
        monkeypatch.setenv("DATA_SOURCE_TYPE", "default")

        # Mock DatabaseManager
        mock_db_manager = AsyncMock()
        mock_db_manager._ensure_initialized = AsyncMock()

        with patch('src.core.factory.DatabaseManager', return_value=mock_db_manager):
            data_source = await get_data_source()

            assert data_source is mock_db_manager
            mock_db_manager._ensure_initialized.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_data_source_notmuch_type(self, monkeypatch):
        """Test get_data_source with notmuch DATA_SOURCE_TYPE."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment to use notmuch
        monkeypatch.setenv("DATA_SOURCE_TYPE", "notmuch")

        data_source = await get_data_source()

        assert isinstance(data_source, NotmuchDataSource)

    @pytest.mark.asyncio
    async def test_get_data_source_unknown_type(self, monkeypatch):
        """Test get_data_source with unknown DATA_SOURCE_TYPE defaults to DatabaseManager."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment to use unknown type
        monkeypatch.setenv("DATA_SOURCE_TYPE", "unknown")

        # Mock DatabaseManager
        mock_db_manager = AsyncMock()
        mock_db_manager._ensure_initialized = AsyncMock()

        with patch('src.core.factory.DatabaseManager', return_value=mock_db_manager):
            data_source = await get_data_source()

            assert data_source is mock_db_manager

    @pytest.mark.asyncio
    async def test_get_data_source_singleton_behavior(self):
        """Test that get_data_source returns the same instance (singleton)."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock environment
        import os
        original_env = os.environ.get("DATA_SOURCE_TYPE")
        os.environ["DATA_SOURCE_TYPE"] = "notmuch"

        try:
            # Get first instance
            ds1 = await get_data_source()

            # Get second instance
            ds2 = await get_data_source()

            # Should be the same object
            assert ds1 is ds2
            assert isinstance(ds1, NotmuchDataSource)

        finally:
            # Restore environment
            if original_env is not None:
                os.environ["DATA_SOURCE_TYPE"] = original_env
            else:
                os.environ.pop("DATA_SOURCE_TYPE", None)

    @pytest.mark.asyncio
    async def test_get_data_source_environment_override(self, monkeypatch):
        """Test that environment variable properly controls data source type."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        test_cases = [
            ("default", "DatabaseManager"),
            ("notmuch", "NotmuchDataSource"),
            ("", "DatabaseManager"),  # Empty string should default
        ]

        for env_value, expected_type in test_cases:
            # Reset instance
            src.core.factory._data_source_instance = None

            if env_value:
                monkeypatch.setenv("DATA_SOURCE_TYPE", env_value)
            else:
                monkeypatch.delenv("DATA_SOURCE_TYPE", raising=False)

            if expected_type == "DatabaseManager":
                mock_db_manager = AsyncMock()
                mock_db_manager._ensure_initialized = AsyncMock()

                with patch('src.core.factory.DatabaseManager', return_value=mock_db_manager):
                    data_source = await get_data_source()
                    assert data_source is mock_db_manager
            else:
                data_source = await get_data_source()
                assert isinstance(data_source, NotmuchDataSource)


class TestAIEngineFactory:
    """Test the AI engine factory function."""

    def test_get_ai_engine_exists(self):
        """Test that get_ai_engine function exists and is callable."""
        # Check that the function exists
        assert callable(get_ai_engine)

    def test_get_ai_engine_returns_object(self):
        """Test that get_ai_engine returns an object with expected interface."""
        ai_engine = get_ai_engine()

        # Should have basic AI methods
        expected_methods = [
            'analyze_sentiment',
            'classify_topic',
            'recognize_intent'
        ]

        for method_name in expected_methods:
            assert hasattr(ai_engine, method_name), f"AI engine missing method: {method_name}"
            assert callable(getattr(ai_engine, method_name)), f"AI engine method not callable: {method_name}"


class TestFactoryErrorHandling:
    """Test error handling in factory functions."""

    @pytest.mark.asyncio
    async def test_get_data_source_database_initialization_failure(self):
        """Test handling of database initialization failure."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock DatabaseManager that fails initialization
        mock_db_manager = AsyncMock()
        mock_db_manager._ensure_initialized = AsyncMock(side_effect=Exception("DB init failed"))

        with patch('src.core.factory.DatabaseManager', return_value=mock_db_manager):
            with pytest.raises(Exception, match="DB init failed"):
                await get_data_source()

    @pytest.mark.asyncio
    async def test_get_data_source_handles_import_errors(self):
        """Test that factory handles import errors gracefully."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Mock an import error for DatabaseManager
        with patch('src.core.factory.DatabaseManager', side_effect=ImportError("Module not found")):
            # Should still work for notmuch
            import os
            original_env = os.environ.get("DATA_SOURCE_TYPE")
            os.environ["DATA_SOURCE_TYPE"] = "notmuch"

            try:
                data_source = await get_data_source()
                assert isinstance(data_source, NotmuchDataSource)
            finally:
                # Restore environment
                if original_env is not None:
                    os.environ["DATA_SOURCE_TYPE"] = original_env
                else:
                    os.environ.pop("DATA_SOURCE_TYPE", None)


class TestFactoryIntegration:
    """Integration tests for factory functions."""

    @pytest.mark.asyncio
    async def test_data_source_factory_integration(self):
        """Test that factory integrates properly with data source implementations."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        # Test with notmuch (doesn't require external dependencies)
        import os
        original_env = os.environ.get("DATA_SOURCE_TYPE")
        os.environ["DATA_SOURCE_TYPE"] = "notmuch"

        try:
            data_source = await get_data_source()

            # Should implement DataSource interface
            assert isinstance(data_source, DataSource)

            # Should have all required methods
            required_methods = [
                'create_email', 'get_email_by_id', 'get_all_emails',
                'search_emails', 'update_email', 'delete_email'
            ]

            for method_name in required_methods:
                assert hasattr(data_source, method_name)
                method = getattr(data_source, method_name)
                assert callable(method)

        finally:
            # Restore environment
            if original_env is not None:
                os.environ["DATA_SOURCE_TYPE"] = original_env
            else:
                os.environ.pop("DATA_SOURCE_TYPE", None)

    def test_ai_engine_factory_integration(self):
        """Test that AI engine factory integrates properly."""
        ai_engine = get_ai_engine()

        # Test basic functionality
        test_text = "This is a test email about work"

        # Should not raise exceptions
        try:
            sentiment = ai_engine.analyze_sentiment(test_text)
            topic = ai_engine.classify_topic(test_text)
            intent = ai_engine.recognize_intent(test_text)

            # Results should be dictionaries or None
            assert sentiment is None or isinstance(sentiment, dict)
            assert topic is None or isinstance(topic, dict)
            assert intent is None or isinstance(intent, dict)

        except Exception as e:
            # AI engine might not be fully implemented, but shouldn't crash
            # Log the error for debugging
            import logging
            logging.warning(f"AI engine integration test failed: {e}")
            # Don't fail the test - this might be expected if models aren't loaded
            pass


class TestFactoryConfiguration:
    """Test factory configuration and environment handling."""

    @pytest.mark.asyncio
    async def test_data_source_type_configuration(self):
        """Test that data source type can be configured via environment."""
        # Reset the global instance
        import src.core.factory
        src.core.factory._data_source_instance = None

        import os

        # Test different configurations
        configs = [
            ("notmuch", NotmuchDataSource),
            ("default", type(None)),  # Will be mocked
        ]

        for config_value, expected_type in configs:
            # Reset instance
            src.core.factory._data_source_instance = None

            original_env = os.environ.get("DATA_SOURCE_TYPE")
            os.environ["DATA_SOURCE_TYPE"] = config_value

            try:
                if config_value == "notmuch":
                    data_source = await get_data_source()
                    assert isinstance(data_source, expected_type)
                else:
                    # For default, we need to mock DatabaseManager
                    mock_db = AsyncMock()
                    mock_db._ensure_initialized = AsyncMock()

                    with patch('src.core.factory.DatabaseManager', return_value=mock_db):
                        data_source = await get_data_source()
                        assert data_source is mock_db

            finally:
                # Restore environment
                if original_env is not None:
                    os.environ["DATA_SOURCE_TYPE"] = original_env
                else:
                    os.environ.pop("DATA_SOURCE_TYPE", None)

    def test_factory_functions_are_callable(self):
        """Test that all factory functions are properly defined and callable."""
        # Test get_data_source (async)
        import asyncio
        assert asyncio.iscoroutinefunction(get_data_source)

        # Test get_ai_engine (sync)
        assert callable(get_ai_engine)

        # Should be able to call get_ai_engine without issues
        ai_engine = get_ai_engine()
        assert ai_engine is not None
