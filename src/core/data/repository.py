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


# Additional repository implementations could be added here
# For example, a caching repository that adds caching layer on top of another repository