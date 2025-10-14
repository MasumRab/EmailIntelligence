from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DataSource(ABC):
    """
    Abstract base class for a data source.
    """

    @abstractmethod
    async def get_emails(self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None) -> List[Dict[str, Any]]:
        """
        Fetches a list of emails.

        Args:
            limit: The maximum number of emails to return.
            offset: The starting offset for the emails.
            category_id: Optional category ID to filter emails.
            is_unread: Optional flag to filter unread emails.

        Returns:
            A list of email objects.
        """
        pass

    @abstractmethod
    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new email.

        Args:
            email_data: The data for the new email.

        Returns:
            The created email object.
        """
        pass

    @abstractmethod
    async def update_email(self, email_id: Any, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing email.

        Args:
            email_id: The ID of the email to update.
            email_data: The data to update the email with.

        Returns:
            The updated email object.
        """
        pass

    @abstractmethod
    async def get_email_by_id(self, email_id: Any) -> Dict[str, Any]:
        """
        Fetches a single email by its ID.

        Args:
            email_id: The ID of the email to fetch.

        Returns:
            The email object, or None if not found.
        """
        pass

    @abstractmethod
    async def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for emails matching a query.

        Args:
            query: The search query.

        Returns:
            A list of matching email objects.
        """
        pass

    @abstractmethod
    async def add_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Adds tags to an email.

        Args:
            email_id: The ID of the email to tag.
            tags: A list of tags to add.

        Returns:
            True if the tags were added successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def remove_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Removes tags from an email.

        Args:
            email_id: The ID of the email to remove tags from.
            tags: A list of tags to remove.

        Returns:
            True if the tags were removed successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Fetches all categories.
        """
        pass

    @abstractmethod
    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new category.
        """
        pass
