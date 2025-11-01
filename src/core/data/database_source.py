from typing import Any, Dict, List

from ..database import DatabaseManager, get_db
from .data_source import DataSource


class DatabaseDataSource(DataSource):
    """
    A data source for emails that uses the database.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    @classmethod
    async def create(cls):
        db_manager = await get_db()
        return cls(db_manager)

    async def get_emails(
        self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches a list of emails from the database.
        """
        return await self.db.get_emails(
            limit=limit, offset=offset, category_id=category_id, is_unread=is_unread
        )

    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new email in the database.
        """
        return await self.db.create_email(email_data)

    async def update_email(self, email_id: Any, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing email in the database.
        """
        return await self.db.update_email(email_id, email_data)

    async def get_email_by_id(self, email_id: Any) -> Dict[str, Any]:
        """
        Fetches a single email by its ID from the database.
        """
        return await self.db.get_email_by_id(email_id)

    async def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for emails matching a query in the database.
        """
        return await self.db.search_emails(query)

    async def add_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Adds tags to an email in the database.
        """
        email = await self.db.get_email_by_id(email_id)
        if not email:
            return False

        existing_tags = email.get("tags", [])
        new_tags = list(set(existing_tags + tags))

        updated_email = await self.db.update_email(email_id, {"tags": new_tags})
        return updated_email is not None

    async def remove_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Removes tags from an email in the database.
        """
        email = await self.db.get_email_by_id(email_id)
        if not email:
            return False

        existing_tags = email.get("tags", [])
        updated_tags = [tag for tag in existing_tags if tag not in tags]

        updated_email = await self.db.update_email(email_id, {"tags": updated_tags})
        return updated_email is not None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Fetches all categories from the database.
        """
        return await self.db.get_all_categories()

    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new category in the database.
        """
        return await self.db.create_category(category_data)


async def get_database_data_source() -> DatabaseDataSource:
    """
    Provides a singleton instance of the DatabaseDataSource.
    """
    return await DatabaseDataSource.create()
