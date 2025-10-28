from typing import Any, Dict, List, Optional

import notmuch

from .data_source import DataSource


class NotmuchDataSource(DataSource):
    """
    A data source for Notmuch, implementing the DataSource interface.
    This implementation is read-only for the initial phase.
    """

    def __init__(self, db_path: Optional[str] = None):
        try:
            self.db = notmuch.Database(db_path)
        except Exception as e:
            print(f"Error opening notmuch database: {e}")
            self.db = None

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails using a notmuch query string."""
        if not self.db:
            return []

        query = self.db.create_query(search_term)
        messages = query.search_messages()

        results = []
        for message in list(messages)[:limit]:
            results.append(
                {
                    "id": message.get_message_id(),
                    "message_id": message.get_message_id(),
                    "subject": message.get_header("subject"),
                    "sender": message.get_header("from"),
                    "date": message.get_date(),
                    "tags": list(message.get_tags()),
                }
            )
        return results

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its notmuch message ID."""
        if not self.db:
            return None

        query = self.db.create_query(f"id:{message_id}")
        messages = query.search_messages()

        message_list = list(messages)
        if not message_list:
            return None

        message = message_list[0]
        email_data = {
            "id": message.get_message_id(),
            "message_id": message.get_message_id(),
            "subject": message.get_header("subject"),
            "sender": message.get_header("from"),
            "recipients": message.get_header("to"),
            "date": message.get_date(),
            "tags": list(message.get_tags()),
        }

        if include_content:
            try:
                content = ""
                for part in message.get_message_parts():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
                if not content:  # fallback to first part if no text/plain
                    content = message.get_message_parts()[0].get_payload(decode=True).decode(
                        "utf-8", errors="ignore"
                    )
                email_data["body"] = content
            except Exception as e:
                email_data["body"] = f"Error decoding content: {e}"

        return email_data

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves emails. This is a basic implementation that maps parameters to a notmuch query.
        """
        query_parts = []
        if is_unread:
            query_parts.append("tag:unread")

        search_term = " ".join(query_parts) if query_parts else "*"

        if not self.db:
            return []

        query = self.db.create_query(search_term)
        messages = query.search_messages()

        results = []
        for message in list(messages)[offset : offset + limit]:
            results.append(
                {
                    "id": message.get_message_id(),
                    "message_id": message.get_message_id(),
                    "subject": message.get_header("subject"),
                    "sender": message.get_header("from"),
                    "date": message.get_date(),
                    "tags": list(message.get_tags()),
                }
            )
        return results

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        return await self.get_emails(limit=limit, offset=offset)

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """In notmuch, categories are tags."""
        if not self.db:
            return []
        tags = self.db.get_all_tags()
        return [{"name": tag, "id": tag} for tag in tags]

    # Mock implementations for write operations and methods with type mismatches

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Not implemented for read-only data source."""
        return None

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Not implemented. Notmuch uses string message IDs, not integer IDs."""
        return None

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Not implemented for read-only data source."""
        return None

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Not implemented for read-only data source."""
        return None

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Not implemented. Notmuch uses string tags, not integer category IDs."""
        return []

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Not implemented for read-only data source."""
        return None

    async def shutdown(self) -> None:
        if self.db:
            self.db.close()
            self.db = None
