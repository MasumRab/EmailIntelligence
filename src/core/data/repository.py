from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.core.data_source import DataSource


class EmailRepository(ABC):
    """Abstract base class for email repository."""

    @abstractmethod
    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new email record."""
        pass

    @abstractmethod
    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its ID."""
        pass

    @abstractmethod
    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Retrieves all categories."""
        pass

    @abstractmethod
    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new category."""
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
    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its message ID."""
        pass

    @abstractmethod
    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its message ID."""
        pass

    @abstractmethod
    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves all emails with pagination."""
        pass

    @abstractmethod
    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Retrieves emails by category."""
        pass

    @abstractmethod
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails."""
        pass

    @abstractmethod
    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its internal ID."""
        pass


class DatabaseEmailRepository(EmailRepository):
    """Database implementation of email repository."""

    def __init__(self, data_source: DataSource):
        self.data_source = data_source

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new email record."""
        return await self.data_source.create_email(email_data)

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its ID."""
        return await self.data_source.get_email_by_id(email_id, include_content)

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Retrieves all categories."""
        return await self.data_source.get_all_categories()

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new category."""
        return await self.data_source.create_category(category_data)

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves emails with filtering and pagination."""
        return await self.data_source.get_emails(limit, offset, category_id, is_unread)

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its message ID."""
        return await self.data_source.update_email_by_message_id(message_id, update_data)

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its message ID."""
        return await self.data_source.get_email_by_message_id(message_id, include_content)

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves all emails with pagination."""
        return await self.data_source.get_all_emails(limit, offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Retrieves emails by category."""
        return await self.data_source.get_emails_by_category(category_id, limit, offset)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails."""
        return await self.data_source.search_emails(search_term, limit)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its internal ID."""
        return await self.data_source.update_email(email_id, update_data)


import asyncio
import time
from typing import Any, Dict, List, Optional


class CachingEmailRepository(EmailRepository):
    """Caching wrapper for EmailRepository that adds caching to frequently accessed data."""

    def __init__(self, repository: EmailRepository, cache_ttl: int = 30):
        """
        Initialize the caching repository.

        Args:
            repository: The underlying EmailRepository to wrap
            cache_ttl: Time to live for cached data in seconds (default: 30 seconds)
        """
        self.repository = repository
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_lock = asyncio.Lock()

    def _get_cache_key(self, method: str, *args, **kwargs) -> str:
        """Generate a cache key from method name and parameters."""
        # Create a string representation of args and kwargs
        params = str((args, sorted(kwargs.items())))
        return f"{method}:{params}"

    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry is still valid based on TTL."""
        if 'timestamp' not in cache_entry:
            return False
        return time.time() - cache_entry['timestamp'] < self.cache_ttl

    async def _get_cached(self, method: str, *args, **kwargs):
        """Get cached result if available and valid."""
        key = self._get_cache_key(method, *args, **kwargs)
        async with self._cache_lock:
            if key in self._cache and self._is_cache_valid(self._cache[key]):
                return self._cache[key]['data']
        return None

    async def _set_cached(self, method: str, result, *args, **kwargs):
        """Cache the result."""
        key = self._get_cache_key(method, *args, **kwargs)
        async with self._cache_lock:
            self._cache[key] = {
                'data': result,
                'timestamp': time.time()
            }

    async def _invalidate_cache(self):
        """Invalidate all cached data."""
        async with self._cache_lock:
            self._cache.clear()

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new email record."""
        # Invalidate cache when creating a new email
        await self._invalidate_cache()
        result = await self.repository.create_email(email_data)
        return result

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its ID."""
        # This shouldn't be cached as it's typically called for specific records
        return await self.repository.get_email_by_id(email_id, include_content)

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Retrieves all categories."""
        # Check cache first
        cached = await self._get_cached('get_all_categories')
        if cached is not None:
            return cached
        
        # Get from underlying repository and cache it
        result = await self.repository.get_all_categories()
        await self._set_cached('get_all_categories', result)
        return result

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new category."""
        # Invalidate cache when creating a new category
        await self._invalidate_cache()
        result = await self.repository.create_category(category_data)
        return result

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves emails with filtering and pagination."""
        # Check cache first
        cached = await self._get_cached('get_emails', limit=limit, offset=offset, category_id=category_id, is_unread=is_unread)
        if cached is not None:
            return cached
        
        # Get from underlying repository and cache it
        result = await self.repository.get_emails(limit, offset, category_id, is_unread)
        await self._set_cached('get_emails', result, limit=limit, offset=offset, category_id=category_id, is_unread=is_unread)
        return result

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its message ID."""
        # Invalidate cache when updating an email
        await self._invalidate_cache()
        result = await self.repository.update_email_by_message_id(message_id, update_data)
        return result

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its message ID."""
        # This shouldn't be cached as it's typically called for specific records
        return await self.repository.get_email_by_message_id(message_id, include_content)

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves all emails with pagination."""
        # Check cache first
        cached = await self._get_cached('get_all_emails', limit=limit, offset=offset)
        if cached is not None:
            return cached
        
        # Get from underlying repository and cache it
        result = await self.repository.get_all_emails(limit, offset)
        await self._set_cached('get_all_emails', result, limit=limit, offset=offset)
        return result

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Retrieves emails by category."""
        # Check cache first
        cached = await self._get_cached('get_emails_by_category', category_id=category_id, limit=limit, offset=offset)
        if cached is not None:
            return cached
        
        # Get from underlying repository and cache it
        result = await self.repository.get_emails_by_category(category_id, limit, offset)
        await self._set_cached('get_emails_by_category', result, category_id=category_id, limit=limit, offset=offset)
        return result

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails."""
        # Don't cache search results as they're typically one-offs
        return await self.repository.search_emails(search_term, limit)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its internal ID."""
        # Invalidate cache when updating an email
        await self._invalidate_cache()
        result = await self.repository.update_email(email_id, update_data)
        return result


# Additional repository implementations could be added here
# For example, a logging repository that adds logging to another repository