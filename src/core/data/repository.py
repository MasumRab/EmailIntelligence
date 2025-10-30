from abc import ABC, abstractmethod
<<<<<<< HEAD
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, AsyncGenerator
=======
from typing import Any, Dict, List, Optional
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

from .data_source import DataSource


class EmailRepository(ABC):
    """Abstract base class for email repository operations."""

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
    async def shutdown(self) -> None:
        """Performs any necessary cleanup."""
        pass

<<<<<<< HEAD
    # Caching methods
    @abstractmethod
    async def cache_get(self, key: str) -> Optional[Any]:
        """Retrieves a value from cache by key."""
        pass

    @abstractmethod
    async def cache_set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Sets a value in the cache with an optional TTL."""
        pass

    # Transaction methods
    @abstractmethod
    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator['EmailRepository', None]:
        """Provides a transaction context manager."""
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

=======
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

class DatabaseEmailRepository(EmailRepository):
    """Email repository implementation using DatabaseManager."""

    def __init__(self, db_manager: DataSource):
        self.db_manager = db_manager
<<<<<<< HEAD
        # Simple in-memory cache using a dictionary
        self._cache: Dict[str, tuple] = {}  # key -> (value, expiry_timestamp)

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.db_manager.create_email(email_data)
        # Clear relevant cache entries when creating a new email
        await self._invalidate_cache_for_email_operations()
        return result

    async def get_email_by_id(self, email_id: int, include_content: bool = True) -> Optional[Dict[str, Any]]:
        cache_key = f"email:{email_id}:{include_content}"
        cached_result = await self.cache_get(cache_key)
        if cached_result is not None:
            return cached_result

        result = await self.db_manager.get_email_by_id(email_id, include_content)
        if result:
            await self.cache_set(cache_key, result, ttl=300)  # Cache for 5 minutes
        return result
=======

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.db_manager.create_email(email_data)

    async def get_email_by_id(self, email_id: int, include_content: bool = True) -> Optional[Dict[str, Any]]:
        return await self.db_manager.get_email_by_id(email_id, include_content)
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
<<<<<<< HEAD
        # Create a cache key based on parameters
        cache_key = f"emails:{limit}:{offset}:{category_id}:{is_unread}"
        cached_result = await self.cache_get(cache_key)
        if cached_result is not None:
            return cached_result

        result = await self.db_manager.get_emails(limit, offset, category_id, is_unread)
        if result:
            await self.cache_set(cache_key, result, ttl=300)  # Cache for 5 minutes
        return result

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        cache_key = f"search:{search_term}:{limit}"
        cached_result = await self.cache_get(cache_key)
        if cached_result is not None:
            return cached_result

        result = await self.db_manager.search_emails(search_term, limit)
        if result:
            await self.cache_set(cache_key, result, ttl=300)  # Cache for 5 minutes
        return result

    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.db_manager.update_email(email_id, update_data)
        # Clear relevant cache entries when updating an email
        await self._invalidate_cache_for_email_operations()
        return result
=======
        return await self.db_manager.get_emails(limit, offset, category_id, is_unread)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.db_manager.search_emails(search_term, limit)

    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.db_manager.update_email(email_id, update_data)
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

    async def shutdown(self) -> None:
        await self.db_manager.shutdown()

<<<<<<< HEAD
    async def cache_get(self, key: str) -> Optional[Any]:
        """Retrieves a value from cache by key."""
        import time
        if key in self._cache:
            value, expiry = self._cache[key]
            if expiry > time.time():
                return value
            else:
                # Remove expired entry
                del self._cache[key]
        return None

    async def cache_set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Sets a value in the cache with an optional TTL."""
        import time
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)
        return True

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator['DatabaseEmailRepository', None]:
        """Provides a transaction context manager."""
        # For this implementation, we'll use a simple approach
        # In a more sophisticated implementation, we might use actual DB transactions
        old_cache = self._cache.copy()  # Backup cache state
        try:
            yield self
        except Exception as e:
            # Restore cache state in case of error
            self._cache = old_cache
            raise e

    async def bulk_create_emails(self, emails_data: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
        """Creates multiple emails in a single operation."""
        results = []
        for email_data in emails_data:
            result = await self.create_email(email_data)
            results.append(result)
        # Clear relevant cache entries
        await self._invalidate_cache_for_email_operations()
        return results

    async def bulk_update_emails(self, updates: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
        """Updates multiple emails in a single operation."""
        results = []
        for update_data in updates:
            email_id = update_data.get("id")
            if email_id is not None:
                # Remove 'id' from update_data to pass only the fields to update
                update_fields = {k: v for k, v in update_data.items() if k != "id"}
                result = await self.update_email(email_id, update_fields)
                results.append(result)
            else:
                results.append(None)
        # Clear relevant cache entries
        await self._invalidate_cache_for_email_operations()
        return results

    async def bulk_delete_emails(self, email_ids: List[int]) -> bool:
        """Deletes multiple emails in a single operation."""
        # For this implementation, we'll just update the emails to be marked as deleted
        # Since the database manager doesn't have a delete method, we'll update the emails
        # to mark them as deleted
        import datetime
        for email_id in email_ids:
            await self.update_email(email_id, {"deleted": True, "deleted_at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        
        # Clear relevant cache entries
        await self._invalidate_cache_for_email_operations()
        return True

    async def _invalidate_cache_for_email_operations(self):
        """Helper method to clear relevant cache entries after email operations."""
        # Simple approach: clear the entire cache
        # In a production system, we'd want to be more strategic about what to invalidate
        self._cache.clear()

=======
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

# Factory function
_email_repo_instance: Optional[EmailRepository] = None


async def get_email_repository() -> EmailRepository:
    """
    Provides the singleton instance of the EmailRepository.
    """
    global _email_repo_instance
    if _email_repo_instance is None:
        from .factory import get_data_source
        data_source = await get_data_source()
        _email_repo_instance = DatabaseEmailRepository(data_source)
    return _email_repo_instance
