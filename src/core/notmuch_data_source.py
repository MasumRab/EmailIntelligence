from typing import Any, Dict, List, Optional

import notmuch

from .data_source import DataSource


class NotmuchDataSource(DataSource):
    """
    A data source for Notmuch, implementing the DataSource interface.
    This implementation is read-only for the initial phase.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.db = None
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Initializing NotmuchDataSource with db_path: {db_path}")
            self.db = notmuch.Database(db_path)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error opening notmuch database: {e}")
            self.db = None

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails using a notmuch query string."""
        if not self.db:
            return []

        try:
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
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error searching emails in notmuch: {e}")
            return []

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its notmuch message ID."""
        if not self.db:
            return None

        query = self.db.create_query(f"id:{message_id}")
        messages = list(query.search_messages())

        if not messages:
            return None

        message = messages[0]
        
        # Load the full message from the file to extract content parts
        filename = message.get_filename()
        
        try:
            # Parse email content from file
            import email
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                email_message = email.message_from_file(f)
            
            email_data = {
                "id": message.get_message_id(),
                "message_id": message.get_message_id(),
                "subject": message.get_header("subject") or email_message.get("Subject", ""),
                "sender": message.get_header("from") or email_message.get("From", ""),
                "recipients": message.get_header("to") or email_message.get("To", ""),
                "date": message.get_date(),
                "tags": list(message.get_tags()),
            }

            if include_content:
                content = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True)
                            if payload:
                                content = payload.decode('utf-8', errors='ignore')
                                break
                else:
                    payload = email_message.get_payload(decode=True)
                    if payload:
                        content = payload.decode('utf-8', errors='ignore')
                
                email_data["body"] = content
                
            return email_data
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error processing email {message_id}: {e}")
            return {
                "id": message.get_message_id(),
                "message_id": message.get_message_id(),
                "subject": message.get_header("subject"),
                "sender": message.get_header("from"),
                "recipients": message.get_header("to"),
                "date": message.get_date(),
                "tags": list(message.get_tags()),
                "body": f"Error decoding content: {e}"
            }

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

        try:
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
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting emails from notmuch: {e}")
            return []

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
        """Delete an email by its internal ID - Not implemented for Notmuch data source."""
        # Notmuch is a read-only index, so we can't actually delete emails
        # In a real implementation, this would need to remove tags or mark as deleted
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"NotmuchDataSource: delete_email called for ID {email_id} but not implemented")
        return False

    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics for efficient server-side calculations."""
        if not self.db:
            return {
                "total_emails": 0,
                "auto_labeled": 0,
                "categories_count": 0,
                "unread_count": 0,
                "weekly_growth": {"emails": 0, "percentage": 0.0}
            }

        try:
            # Get total emails
            query = self.db.create_query("*")
            total_emails = query.count_messages()

            # Get unread count
            unread_query = self.db.create_query("tag:unread")
            unread_count = unread_query.count_messages()

            # For auto_labeled, we'll use a placeholder tag like "auto-labeled"
            auto_labeled_query = self.db.create_query("tag:auto-labeled")
            auto_labeled = auto_labeled_query.count_messages()

            # For categories, we'll count distinct tags (excluding system tags)
            all_tags = self.db.get_all_tags()
            # Filter out common system tags to get user-defined categories
            system_tags = {"inbox", "unread", "sent", "draft", "deleted", "spam", "flagged", "replied", "forwarded"}
            category_tags = [tag for tag in all_tags if tag.lower() not in system_tags]
            categories_count = len(category_tags)

            # Weekly growth - simplified calculation
            # In a production implementation, this would query for emails from the last week
            weekly_growth = {
                "emails": total_emails,  # Placeholder - would be new emails in last week
                "percentage": 0.0  # Placeholder - would be week-over-week growth percentage
            }

            return {
                "total_emails": total_emails,
                "auto_labeled": auto_labeled,
                "categories_count": categories_count,
                "unread_count": unread_count,
                "weekly_growth": weekly_growth
            }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting dashboard aggregates from notmuch: {e}")
            # Return default values on error
            return {
                "total_emails": 0,
                "auto_labeled": 0,
                "categories_count": 0,
                "unread_count": 0,
                "weekly_growth": {"emails": 0, "percentage": 0.0}
            }

    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit.
        
        In Notmuch, categories are mapped to tags. This implementation counts emails per tag
        and excludes common system tags to focus on user-defined categories.
        """
        if not self.db:
            return {}

        try:
            # Get all tags and their counts
            tag_counts = {}
            
            # Exclude common system tags
            system_tags = {"inbox", "unread", "sent", "draft", "deleted", "spam", "flagged", "replied", "forwarded"}
            
            # Get all tags from the database
            all_tags = list(self.db.get_all_tags())
            
            # For each tag (that's not a system tag), count messages
            for tag in all_tags:
                if tag.lower() not in system_tags:
                    query = self.db.create_query(f"tag:{tag}")
                    count = query.count_messages()
                    if count > 0:  # Only include tags with emails
                        tag_counts[tag] = count
            
            # Sort by count descending and apply limit
            sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_tags[:limit])
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting category breakdown from notmuch: {e}")
            # Return empty dict on error
            return {}

    async def shutdown(self) -> None:
        if self.db:
            self.db.close()
            self.db = None
