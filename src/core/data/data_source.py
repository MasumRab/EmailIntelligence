from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataSource(ABC):
    """Abstract base class for a data source."""

    @abstractmethod
    async def get_emails(
        self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None
    ) -> List[Dict[str, Any]]:
        """Fetches a list of emails."""
        pass

    @abstractmethod
    async def get_email_by_id(self, email_id: int) -> Dict[str, Any]:
        """Get a single email by ID."""
        pass

    @abstractmethod
    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new email."""
        pass

    @abstractmethod
    async def update_email(self, email_id: int, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing email."""
        pass

    @abstractmethod
    async def delete_email(self, email_id: int) -> bool:
        """Delete an email."""
        pass
