from typing import Any, Dict, List

from .data_source import DataSource


class NotmuchDataSource(DataSource):
    """
    A mock data source for notmuch.
    """

    async def get_emails(
        self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches a list of emails from notmuch.
        """
        return [{"id": 1, "subject": "Test Email from notmuch"}]

    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new email in notmuch.
        """
        return {"id": 2, "subject": "New Email in notmuch"}

    async def update_email(self, email_id: Any, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing email in notmuch.
        """
        return {"id": email_id, "subject": "Updated Email in notmuch"}

    async def get_email_by_id(self, email_id: Any) -> Dict[str, Any]:
        """
        Fetches a single email by its ID from notmuch.
        """
        return {"id": email_id, "subject": "Test Email from notmuch"}

    async def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for emails matching a query in notmuch.
        """
        return [{"id": 1, "subject": "Test Email from notmuch"}]

    async def add_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Adds tags to an email in notmuch.
        """
        return True

    async def remove_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Removes tags from an email in notmuch.
        """
        return True

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Fetches all categories from notmuch.
        """
        return [{"id": 1, "name": "Inbox", "color": "#000000"}]

    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new category in notmuch.
        """
        return {
            "id": 2,
            "name": category_data.get("name", "New Category"),
            "color": category_data.get("color", "#000000"),
        }
