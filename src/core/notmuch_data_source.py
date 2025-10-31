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

    async def delete_email(self, email_id: int) -> bool:
        """Delete an email by its internal ID."""
        await self._ensure_initialized()

        try:
            # Get the email first to check if it exists and get message_id
            email = await self.db.get_email_by_id(email_id)
            if not email:
                logger.warning(f"Email with ID {email_id} not found for deletion")
                return False

            message_id = email.get("message_id")
            if message_id:
                # Remove from notmuch database
                try:
                    query = self.notmuch_db.create_query(f"id:{message_id}")
                    messages = query.search_messages()
                    for message in messages:
                        message.remove_all_tags()
                        message.add_tag("deleted")
                    self.notmuch_db.close()
                    self.notmuch_db = self.notmuch.open(self.db_path)
                except Exception as e:
                    logger.warning(f"Failed to mark message as deleted in notmuch: {e}")

            # Delete from our database
            return await self.db.delete_email(email_id)

        except Exception as e:
            logger.error(f"Error deleting email {email_id}: {e}")
            return False

    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics for efficient server-side calculations."""
        # For Notmuch, we need to query the database for counts
        # This is a simplified implementation - in production would use optimized queries

        try:
            # Get total emails
            query = notmuch.Query(self.db, "*")
            total_emails = query.count_messages()

            # Get unread count
            unread_query = notmuch.Query(self.db, "tag:unread")
            unread_count = unread_query.count_messages()

            # For auto_labeled and categories, Notmuch doesn't have built-in categories
            # This would need to be implemented based on tags or external category mapping
            auto_labeled = 0  # Placeholder
            categories_count = 0  # Placeholder

            # Weekly growth - simplified calculation
            weekly_growth = {
                "emails": total_emails,  # Placeholder
                "percentage": 0.0
            }

            return {
                "total_emails": total_emails,
                "auto_labeled": auto_labeled,
                "categories_count": categories_count,
                "unread_count": unread_count,
                "weekly_growth": weekly_growth
            }
        except Exception as e:
            # Return default values on error
            return {
                "total_emails": 0,
                "auto_labeled": 0,
                "categories_count": 0,
                "unread_count": 0,
                "weekly_growth": {"emails": 0, "percentage": 0.0}
            }

    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit."""
        # For Notmuch, categories would need to be mapped from tags or external metadata
        # This is a simplified implementation that returns empty results
        # In a full implementation, this would query Notmuch tags and map them to categories

        try:
            # Placeholder implementation - Notmuch doesn't have built-in categories
            # This would need to be implemented based on tag-to-category mapping
            return {}  # Return empty dict as Notmuch doesn't have category concept
        except Exception as e:
            # Return empty dict on error
            return {}

    async def shutdown(self) -> None:
        if self.db:
            self.db.close()
            self.db = None
