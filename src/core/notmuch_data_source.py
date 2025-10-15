from typing import Any, Dict, List, Optional

from .data_source import DataSource


class NotmuchDataSource(DataSource):
    """A mock data source for Notmuch, implementing the DataSource interface."""

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        print("NotmuchDataSource: create_email called")
        return None

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        print("NotmuchDataSource: get_email_by_id called")
        return None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        print("NotmuchDataSource: get_all_categories called")
        return []

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        print("NotmuchDataSource: create_category called")
        return None

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        print("NotmuchDataSource: get_emails called")
        return []

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        print("NotmuchDataSource: update_email_by_message_id called")
        return None

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        print("NotmuchDataSource: get_email_by_message_id called")
        return None

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        print("NotmuchDataSource: get_all_emails called")
        return []

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        print("NotmuchDataSource: get_emails_by_category called")
        return []

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        print("NotmuchDataSource: search_emails called")
        return []

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        print("NotmuchDataSource: update_email called")
        return None

    async def shutdown(self) -> None:
        print("NotmuchDataSource: shutdown called")
        pass
