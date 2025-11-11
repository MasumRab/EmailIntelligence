<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.core.data_source import DataSource
from src.core.caching import get_cache_manager, CacheConfig, CacheBackend
import asyncio
import time


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

    @abstractmethod
    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics for efficient server-side calculations.

        Returns:
            Dict containing:
            - total_emails: int - Total number of emails
            - auto_labeled: int - Number of auto-labeled emails
            - categories_count: int - Total number of categories
            - unread_count: int - Number of unread emails
            - weekly_growth: Dict[str, Any] - Weekly growth metrics
        """
        pass

    @abstractmethod
    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit.

        Args:
            limit: Maximum number of categories to return (top N by email count)

        Returns:
            Dict mapping category names to email counts, sorted by count descending
        """
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

    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics for efficient server-side calculations."""
        return await self.data_source.get_dashboard_aggregates()

    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit."""
        return await self.data_source.get_category_breakdown(limit)


class CachingEmailRepository(EmailRepository):
    """Caching wrapper for EmailRepository that adds Redis/memory caching to dashboard statistics."""

    def __init__(self, repository: EmailRepository, cache_ttl: int = 600):
        """
        Initialize the caching repository.

        Args:
            repository: The underlying EmailRepository to wrap
            cache_ttl: Time to live for cached data in seconds (default: 10 minutes)
        """
        self.repository = repository
        self.cache_ttl = cache_ttl
        self.cache_manager = get_cache_manager()
        self._cache_lock = asyncio.Lock()

        # Cache keys
        self._dashboard_key = "dashboard:aggregates"
        self._category_breakdown_key = "dashboard:category_breakdown"

    async def _invalidate_dashboard_cache(self):
        """Invalidate all dashboard-related cache entries"""
        await self.cache_manager.delete(self._dashboard_key)
        await self.cache_manager.delete(self._category_breakdown_key)

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new email record."""
        # Invalidate cache when data changes
        await self._invalidate_dashboard_cache()
        return await self.repository.create_email(email_data)

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its ID."""
        return await self.repository.get_email_by_id(email_id, include_content)

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Retrieves all categories."""
        return await self.repository.get_all_categories()

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new category."""
        # Invalidate cache when data changes
        async with self._cache_lock:
            self._dashboard_cache.clear()
            self._category_breakdown_cache.clear()
        return await self.repository.create_category(category_data)

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves emails with filtering and pagination."""
        return await self.repository.get_emails(limit, offset, category_id, is_unread)

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its message ID."""
        # Invalidate cache when data changes
        async with self._cache_lock:
            self._dashboard_cache.clear()
            self._category_breakdown_cache.clear()
        return await self.repository.update_email_by_message_id(message_id, update_data)

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its message ID."""
        return await self.repository.get_email_by_message_id(message_id, include_content)

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves all emails with pagination."""
        return await self.repository.get_all_emails(limit, offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Retrieves emails by category."""
        return await self.repository.get_emails_by_category(category_id, limit, offset)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails."""
        return await self.repository.search_emails(search_term, limit)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Updates an email by its internal ID."""
        # Invalidate cache when data changes
        await self._invalidate_dashboard_cache()
        return await self.repository.update_email(email_id, update_data)

    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics with Redis/memory caching."""
        # Try to get from cache first
        cached_data = await self.cache_manager.get(self._dashboard_key)
        if cached_data is not None:
            return cached_data.copy()

        # Fetch fresh data from repository
        data = await self.repository.get_dashboard_aggregates()

        # Cache the data with TTL
        await self.cache_manager.set(self._dashboard_key, data, ttl=self.cache_ttl)

        return data.copy()

    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with Redis/memory caching."""
        cache_key = f"{self._category_breakdown_key}:{limit}"

        # Try to get from cache first
        cached_data = await self.cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data.copy()

        # Fetch fresh data from repository
        data = await self.repository.get_category_breakdown(limit)

        # Cache the data with TTL
        await self.cache_manager.set(cache_key, data, ttl=self.cache_ttl)

        return data.copy()


# Additional repository implementations could be added here
# For example, a logging repository that adds logging to another repository
=======
>>>>>>> main
