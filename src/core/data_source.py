from abc import ABC, abstractmethod
from typing import Any


class DataSource(ABC):
    """Abstract base class for data sources."""

    @abstractmethod
    async def create_email(self, email_data: dict[str, Any]) -> dict[str, Any] | None:
        """Creates a new email record."""
        pass

    @abstractmethod
    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> dict[str, Any] | None:
        """Retrieves an email by its ID."""
        pass

    @abstractmethod
    async def get_all_categories(self) -> list[dict[str, Any]]:
        """Retrieves all categories."""
        pass

    @abstractmethod
    async def create_category(self, category_data: dict[str, Any]) -> dict[str, Any] | None:
        """Creates a new category."""
        pass

    @abstractmethod
    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: int | None = None,
        is_unread: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieves emails with filtering and pagination."""
        pass

    @abstractmethod
    async def update_email_by_message_id(
        self, message_id: str, update_data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Updates an email by its message ID."""
        pass

    @abstractmethod
    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> dict[str, Any] | None:
        """Retrieves an email by its message ID."""
        pass

    @abstractmethod
    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        """Retrieves all emails with pagination."""
        pass

    @abstractmethod
    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        """Retrieves emails by category."""
        pass

    @abstractmethod
    async def search_emails(self, search_term: str, limit: int = 50) -> list[dict[str, Any]]:
        """Searches emails."""
        pass

    @abstractmethod
    async def update_email(
        self, email_id: int, update_data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Updates an email by its internal ID."""
        pass

    @abstractmethod
    async def delete_email(self, email_id: int) -> bool:
        """Deletes an email by its internal ID."""
        pass

    @abstractmethod
    async def get_dashboard_aggregates(self) -> dict[str, Any]:
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
    async def get_category_breakdown(self, limit: int = 10) -> dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit.

        Args:
            limit: Maximum number of categories to return (top N by email count)

        Returns:
            Dict mapping category names to email counts, sorted by count descending
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Performs any necessary cleanup."""
        pass
