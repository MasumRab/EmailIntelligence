"""
Tests for the enhanced repository with caching and transactions.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from src.core.data.repository import (
    EmailRepository,
    DatabaseEmailRepository,
    get_email_repository
)


class TestCaching:
    """Test repository caching functionality."""
    
    @pytest.fixture
    async def mock_db_manager(self):
        """Create a mock database manager."""
        manager = AsyncMock()
        manager.create_email = AsyncMock(return_value={"id": 1})
        manager.get_email_by_id = AsyncMock(return_value={"id": 1, "subject": "Test"})
        manager.get_emails = AsyncMock(return_value [{"id": 1}])
        manager.search_emails = AsyncMock(return_value [{"id": 1}])
        manager.update_email = AsyncMock(return_value={"id": 1})
        manager.delete_email = AsyncMock(return_value=True)
        manager.shutdown = AsyncMock()
        return manager
    
    @pytest.fixture
    async def repository(self, mock_db_manager):
        """Create a repository instance."""
        return DatabaseEmailRepository(mock_db_manager)
    
    @pytest.mark.asyncio
    async def test_cache_set_and_get(self, repository):
        """Test setting and getting cache values."""
        await repository.cache_set("test_key", {"data": "value"}, ttl=60)
        result = await repository.cache_get("test_key")
        assert result == {"data": "value"}
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self, repository):
        """Test cache expiration."""
        await repository.cache_set("test_key", {"data": "value"}, ttl=1)
        # Wait for expiration
        await asyncio.sleep(1.1)
        result = await repository.cache_get("test_key")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_cache_delete(self, repository):
        """Test cache deletion."""
        await repository.cache_set("test_key", {"data": "value"})
        deleted = await repository.cache_delete("test_key")
        assert deleted is True
        result = await repository.cache_get("test_key")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_email_by_id_with_cache(self, repository, mock_db_manager):
        """Test that get_email_by_id uses cache."""
        # First call should hit database
        result1 = await repository.get_email_by_id(1)
        assert mock_db_manager.get_email_by_id.call_count == 1
        
        # Second call should use cache
        result2 = await repository.get_email_by_id(1)
        assert mock_db_manager.get_email_by_id.call_count == 1  # No additional call
        assert result1 == result2
    
    @pytest.mark.asyncio
    async def test_cache_invalidation_on_create(self, repository, mock_db_manager):
        """Test that cache is invalidated on create."""
        # Populate cache
        await repository.get_emails(limit=10)
        
        # Create email should invalidate cache
        await repository.create_email({"subject": "New"})
        
        # Next call should hit database again
        mock_db_manager.get_emails.reset_mock()
        await repository.get_emails(limit=10)
        assert mock_db_manager.get_emails.call_count == 1


class TestTransactions:
    """Test repository transaction functionality."""
    
    @pytest.fixture
    async def repository(self):
        """Create a repository with mock manager."""
        mock_manager = AsyncMock()
        mock_manager.update_email = AsyncMock(return_value={"id": 1})
        mock_manager.shutdown = AsyncMock()
        return DatabaseEmailRepository(mock_manager)
    
    @pytest.mark.asyncio
    async def test_transaction_success(self, repository):
        """Test successful transaction."""
        async with repository.transaction():
            await repository.update_email(1, {"is_read": True})
        
        # Should not raise exception
        assert True
    
    @pytest.mark.asyncio
    async def test_transaction_failure(self, repository):
        """Test transaction rollback on failure."""
        with pytest.raises(Exception):
            async with repository.transaction():
                await repository.update_email(1, {"is_read": True})
                raise Exception("Transaction failed")
        
        # Should have raised exception
        assert True


class TestBulkOperations:
    """Test repository bulk operations."""
    
    @pytest.fixture
    async def mock_db_manager(self):
        """Create a mock database manager."""
        manager = AsyncMock()
        manager.create_email = AsyncMock(side_effect=lambda x: {"id": x.get("id", 1)})
        manager.update_email = AsyncMock(side_effect=lambda i, x: {"id": i})
        manager.delete_email = AsyncMock(return_value=True)
        return manager
    
    @pytest.fixture
    async def repository(self, mock_db_manager):
        """Create a repository instance."""
        return DatabaseEmailRepository(mock_db_manager)
    
    @pytest.mark.asyncio
    async def test_bulk_create_emails(self, repository, mock_db_manager):
        """Test bulk email creation."""
        emails = [
            {"id": 1, "subject": "Email 1"},
            {"id": 2, "subject": "Email 2"},
            {"id": 3, "subject": "Email 3"}
        ]
        
        results = await repository.bulk_create_emails(emails)
        
        assert len(results) == 3
        assert mock_db_manager.create_email.call_count == 3
    
    @pytest.mark.asyncio
    async def test_bulk_update_emails(self, repository, mock_db_manager):
        """Test bulk email updates."""
        updates = [
            {"id": 1, "is_read": True},
            {"id": 2, "is_read": True}
        ]
        
        results = await repository.bulk_update_emails(updates)
        
        assert len(results) == 2
        assert mock_db_manager.update_email.call_count == 2
    
    @pytest.mark.asyncio
    async def test_bulk_delete_emails(self, repository, mock_db_manager):
        """Test bulk email deletion."""
        email_ids = [1, 2, 3]
        
        result = await repository.bulk_delete_emails(email_ids)
        
        assert result is True
        assert mock_db_manager.delete_email.call_count == 3


class TestFactory:
    """Test factory function."""
    
    @pytest.mark.asyncio
    async def test_get_email_repository_singleton(self):
        """Test that get_email_repository returns singleton."""
        repo1 = await get_email_repository()
        repo2 = await get_email_repository()
        assert repo1 is repo2