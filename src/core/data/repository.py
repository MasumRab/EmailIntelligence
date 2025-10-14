from typing import List, Dict, Any
from .data_source import DataSource
from .database_source import get_database_data_source

class EmailRepository:
    """
    A repository for managing emails from various data sources.
    """

    def __init__(self, data_source: DataSource):
        self.data_source = data_source

    async def get_emails(self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None) -> List[Dict[str, Any]]:
        """
        Fetches a list of emails from the current data source.
        """
        return await self.data_source.get_emails(limit=limit, offset=offset, category_id=category_id, is_unread=is_unread)

    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new email in the current data source.
        """
        return await self.data_source.create_email(email_data)

    async def update_email(self, email_id: Any, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing email in the current data source.
        """
        return await self.data_source.update_email(email_id, email_data)

    async def get_email_by_id(self, email_id: Any) -> Dict[str, Any]:
        """
        Fetches a single email by its ID from the current data source.
        """
        return await self.data_source.get_email_by_id(email_id)

    async def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for emails matching a query in the current data source.
        """
        return await self.data_source.search_emails(query)

    async def add_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Adds tags to an email in the current data source.
        """
        return await self.data_source.add_tags(email_id, tags)

    async def remove_tags(self, email_id: Any, tags: List[str]) -> bool:
        """
        Removes tags from an email in the current data source.
        """
        return await self.data_source.remove_tags(email_id, tags)

async def get_email_repository() -> EmailRepository:
    """
    Provides a singleton instance of the EmailRepository, configured with the
    appropriate data source.
    """
    # This is where the logic to select the data source would go.
    # For now, we'll hardcode it to use the DatabaseDataSource.
    database_data_source = await get_database_data_source()
    return EmailRepository(data_source=database_data_source)
