from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

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


class DatabaseEmailRepository(EmailRepository):
    """Email repository implementation using DatabaseManager."""

    def __init__(self, db_manager: DataSource):
        self.db_manager = db_manager

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.db_manager.create_email(email_data)

    async def get_email_by_id(self, email_id: int, include_content: bool = True) -> Optional[Dict[str, Any]]:
        return await self.db_manager.get_email_by_id(email_id, include_content)

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        return await self.db_manager.get_emails(limit, offset, category_id, is_unread)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.db_manager.search_emails(search_term, limit)

    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.db_manager.update_email(email_id, update_data)

    async def shutdown(self) -> None:
        await self.db_manager.shutdown()


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