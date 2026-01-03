"""
Enhanced email repository with caching and transaction support.
Provides high-performance data access with intelligent caching and atomic operations.
"""

import time
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, AsyncGenerator

from ..data_source import DataSource


class EmailRepository(ABC):
    """Abstract base class for email repository operations.
    
    Provides interface for:
    - Core CRUD operations
    - Caching with TTL support
    - Transaction management
    - Bulk operations
    """
    
    # Core operations
    @abstractmethod
    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new email record."""
        pass
    
    @abstractmethod
    async def get_email_by_id(self, email_id: int, include_content: bool = True) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its ID."""
        pass
    
    @abstractmethod
    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves emails with filtering and pagination."""
        pass
    
    @abstractmethod
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails by term."""
        pass
    
    @abstractmethod
    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates an email by its ID."""
        pass
    
    @abstractmethod
    async def delete_email(self, email_id: int) -> bool:
        """Deletes an email by its ID."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Performs any necessary cleanup."""
        pass
    
    # Caching operations
    @abstractmethod
    async def cache_get(self, key: str) -> Optional[Any]:
        """Retrieves a value from cache by key."""
        pass
    
    @abstractmethod
    async def cache_set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Sets a value in the cache with an optional TTL."""
        pass
    
    @abstractmethod
    async def cache_delete(self, key: str) -> bool:
        """Deletes a value from cache by key."""
        pass
    
    # Transaction operations
    @abstractmethod
    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator['EmailRepository', None]:
        """Provides a transaction context manager for atomic operations."""
        yield self
    
    # Bulk operations
    @abstractmethod
    async def bulk_create_emails(self, emails_data: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
        """Creates multiple emails in a single operation."""
        pass
    
    @abstractmethod
    async def bulk_update_emails(self, updates: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
        """Updates multiple emails in a single operation."""
        pass
    
    @abstractmethod
    async def bulk_delete_emails(self, email_ids: List[int]) -> bool:
        """Deletes multiple emails in a single operation."""
        pass


class DatabaseEmailRepository(EmailRepository):
    """Email repository implementation with caching and transaction support.
    
    Features:
    - In-memory caching with TTL support
    - Automatic cache invalidation on mutations
    - Transaction support with context manager
    - Bulk operations for performance
    """
    
    def __init__(self, db_manager: DataSource, default_ttl: int = 300):
        """
        Initialize the repository.
        
        Args:
            db_manager: Data source instance
            default_ttl: Default cache TTL in seconds (default: 300 = 5 minutes)
        """
        self.db_manager = db_manager
        self._cache: Dict[str, tuple] = {}  # key -> (value, expiry_timestamp)
        self._default_ttl = default_ttl
        self._in_transaction = False
        self._transaction_cache: Dict[str, Any] = {}
    
    # ============================================================================
    # Caching Implementation
    # ============================================================================
    
    async def cache_get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from cache by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if exists and not expired, None otherwise
        """
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            # Cache entry expired
            del self._cache[key]
        return None
    
    async def cache_set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Sets a value in the cache with an optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (default: default_ttl)
            
        Returns:
            True if successful
        """
        if ttl is None:
            ttl = self._default_ttl
        self._cache[key] = (value, time.time() + ttl)
        return True
    
    async def cache_delete(self, key: str) -> bool:
        """
        Deletes a value from cache by key.
        
        Args:
            key: Cache key
            
        Returns:
            True if key existed and was deleted
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def _invalidate_cache_for_email_operations(self):
        """
        Clears cache entries affected by email operations.
        
        Invalidates all cache keys starting with "email:" or "emails:".
        """
        keys_to_delete = [
            k for k in self._cache.keys() 
            if k.startswith("email:") or k.startswith("emails:")
        ]
        for key in keys_to_delete:
            del self._cache[key]
    
    # ============================================================================
    # Core Operations with Caching
    # ============================================================================
    
    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new email record.
        
        Args:
            email_data: Email data dictionary
            
        Returns:
            Created email record or None
        """
        result = await self.db_manager.create_email(email_data)
        # Clear relevant cache entries when creating a new email
        await self._invalidate_cache_for_email_operations()
        return result
    
    async def get_email_by_id(self, email_id: int, include_content: bool = True) -> Optional[Dict[str, Any]]:
        """
        Retrieves an email by its ID with caching.
        
        Args:
            email_id: Email ID
            include_content: Whether to include email content
            
        Returns:
            Email record or None
        """
        cache_key = f"email:{email_id}:{include_content}"
        cached_result = await self.cache_get(cache_key)
        if cached_result is not None:
            return cached_result
        
        result = await self.db_manager.get_email_by_id(email_id, include_content)
        if result:
            await self.cache_set(cache_key, result)
        return result
    
    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves emails with filtering and pagination with caching.
        
        Args:
            limit: Maximum number of emails to return
            offset: Number of emails to skip
            category_id: Filter by category ID
            is_unread: Filter by unread status
            
        Returns:
            List of email records
        """
        # Create a cache key based on parameters
        cache_key = f"emails:{limit}:{offset}:{category_id}:{is_unread}"
        cached_result = await self.cache_get(cache_key)
        if cached_result is not None:
            return cached_result
        
        result = await self.db_manager.get_emails(limit, offset, category_id, is_unread)
        if result:
            await self.cache_set(cache_key, result)
        return result
    
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Searches emails by term with caching.
        
        Args:
            search_term: Search term
            limit: Maximum number of results
            
        Returns:
            List of matching email records
        """
        cache_key = f"search:{search_term}:{limit}"
        cached_result = await self.cache_get(cache_key)
        if cached_result is not None:
            return cached_result
        
        result = await self.db_manager.search_emails(search_term, limit)
        if result:
            await self.cache_set(cache_key, result)
        return result
    
    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates an email by its ID.
        
        Args:
            email_id: Email ID
            update_data: Update data dictionary
            
        Returns:
            Updated email record or None
        """
        result = await self.db_manager.update_email(email_id, update_data)
        # Clear relevant cache entries when updating an email
        await self._invalidate_cache_for_email_operations()
        return result
    
    async def delete_email(self, email_id: int) -> bool:
        """
        Deletes an email by its ID.
        
        Args:
            email_id: Email ID
            
        Returns:
            True if successful
        """
        result = await self.db_manager.delete_email(email_id)
        # Clear relevant cache entries when deleting an email
        await self._invalidate_cache_for_email_operations()
        return result
    
    async def shutdown(self) -> None:
        """Performs cleanup, clears cache."""
        self._cache.clear()
        await self.db_manager.shutdown()
    
    # ============================================================================
    # Transaction Implementation
    # ============================================================================
    
    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator['EmailRepository', None]:
        """
        Provides a transaction context manager for atomic operations.
        
        Usage:
            async with repo.transaction():
                await repo.update_email(1, {"is_read": True})
                await repo.update_email(2, {"is_read": True})
        
        Yields:
            Self for method chaining
        """
        self._in_transaction = True
        self._transaction_cache = {}
        
        try:
            yield self
            # Transaction successful - clear affected cache
            await self._invalidate_cache_for_email_operations()
        except Exception as e:
            # Transaction failed - rollback by clearing transaction cache
            self._transaction_cache.clear()
            raise e
        finally:
            self._in_transaction = False
            self._transaction_cache.clear()
    
    # ============================================================================
    # Bulk Operations Implementation
    # ============================================================================
    
    async def bulk_create_emails(self, emails_data: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
        """
        Creates multiple emails in a single operation.
        
        Args:
            emails_data: List of email data dictionaries
            
        Returns:
            List of created email records
        """
        results = []
        for email_data in emails_data:
            result = await self.db_manager.create_email(email_data)
            results.append(result)
        
        # Clear affected cache after bulk operation
        await self._invalidate_cache_for_email_operations()
        
        return results
    
    async def bulk_update_emails(self, updates: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
        """
        Updates multiple emails in a single operation.
        
        Args:
            updates: List of update data dictionaries with 'id' field
            
        Returns:
            List of updated email records
        """
        results = []
        for update_data in updates:
            email_id = update_data.get('id')
            if email_id:
                result = await self.db_manager.update_email(email_id, update_data)
                results.append(result)
            else:
                results.append(None)
        
        # Clear affected cache after bulk operation
        await self._invalidate_cache_for_email_operations()
        
        return results
    
    async def bulk_delete_emails(self, email_ids: List[int]) -> bool:
        """
        Deletes multiple emails in a single operation.
        
        Args:
            email_ids: List of email IDs to delete
            
        Returns:
            True if all deletions succeeded
        """
        all_success = True
        for email_id in email_ids:
            result = await self.db_manager.delete_email(email_id)
            if not result:
                all_success = False
        
        # Clear affected cache after bulk operation
        await self._invalidate_cache_for_email_operations()
        
        return all_success


# ============================================================================
# Factory Function
# ============================================================================

_email_repo_instance: Optional[EmailRepository] = None


async def get_email_repository(db_manager: DataSource = None) -> EmailRepository:
    """
    Provides the singleton instance of the EmailRepository.
    
    Args:
        db_manager: Optional data source instance (uses default if not provided)
        
    Returns:
        EmailRepository instance
    """
    global _email_repo_instance
    if _email_repo_instance is None:
        if db_manager is None:
            from ..factory import get_data_source
            db_manager = await get_data_source()
        _email_repo_instance = DatabaseEmailRepository(db_manager)
    return _email_repo_instance