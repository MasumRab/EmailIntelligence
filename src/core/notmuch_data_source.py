"""
Enhanced Notmuch Data Source with AI Analysis and Tagging Support

This module provides a comprehensive data source that integrates Notmuch database access
with AI analysis, smart filtering, and tagging functionality.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime, timezone
import email

if TYPE_CHECKING:
    from .database import DatabaseManager

# Import notmuch only when needed to allow import in environments without it
try:
    import notmuch
    NOTMUCH_AVAILABLE = True
except ImportError:
    notmuch = None
    NOTMUCH_AVAILABLE = False

from .data_source import DataSource
# Import DatabaseManager locally to avoid circular imports
# from .database import DatabaseManager
from .smart_filter_manager import SmartFilterManager
from .ai_engine import ModernAIEngine
from .performance_monitor import log_performance
from .enhanced_error_reporting import (
    log_error, 
    ErrorSeverity, 
    ErrorCategory, 
    create_error_context
)
from .security import PathValidator, validate_path_safety

logger = logging.getLogger(__name__)


class NotmuchDataSource(DataSource):
    """
    Enhanced data source for Notmuch with AI analysis and tagging support.
    
    This implementation provides both read and write capabilities for Notmuch,
    along with AI-powered analysis and smart filtering.
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        db_manager: Optional["DatabaseManager"] = None,
    ):
        # Validate the database path for security if provided
        if db_path is not None:
            try:
                # Use the PathValidator to validate and resolve the database path
                validated_path = PathValidator.validate_and_resolve_db_path(db_path)
                self.db_path = str(validated_path)
            except ValueError as e:
                logger.error(f"Invalid database path provided: {e}")
                self.db_path = None
        else:
            self.db_path = None
            
        self.notmuch_db = None
        self._initialized = False
        self.db = db_manager
        self.ai_engine = None
        self.filter_manager = None
        self._initialized = False
        
        # Initialize Notmuch database if the notmuch module is available
        if NOTMUCH_AVAILABLE:
            try:
                self.notmuch_db = notmuch.Database(self.db_path) if self.db_path else notmuch.Database()
            except Exception as e:
                logger.error(f"Error initializing notmuch database: {e}")
                self.notmuch_db = None
        else:
            logger.warning("Notmuch module not available. NotmuchDataSource will operate in limited mode.")

    async def _ensure_initialized(self):
        """Ensure the Notmuch database connection is available."""
        if self._initialized:
            return

        if self.notmuch_db is None:
            try:
                # Validate the database path before opening
                if self.db_path is not None:
                    validated_path = PathValidator.validate_and_resolve_db_path(self.db_path)
                    self.notmuch_db = notmuch.Database(str(validated_path))
                else:
                    self.notmuch_db = notmuch.Database()
            except ValueError as e:
                logger.error(f"Invalid database path: {e}")
                self.notmuch_db = None
            except Exception as e:
                logger.error(f"Error opening notmuch database: {e}")
                self.notmuch_db = None

        # Initialize database manager if it was provided
        if self.db:
            try:
                await self.db._ensure_initialized()
            except Exception as e:
                logger.warning(
                    f"Could not initialize injected DatabaseManager, proceeding without: {e}"
                )
                self.db = None  # Allow operation without database manager

        # Initialize AI engine if needed for analysis
        if self.ai_engine is None:
            try:
                self.ai_engine = ModernAIEngine()
                self.ai_engine.initialize()
            except Exception as e:
                logger.warning(f"Could not initialize AI engine: {e}")
                self.ai_engine = None

        # Initialize smart filter manager if needed for categorization
        if self.filter_manager is None:
            try:
                self.filter_manager = SmartFilterManager()
            except Exception as e:
                logger.warning(f"Could not initialize SmartFilterManager: {e}")
                self.filter_manager = None

        self._initialized = True
        logger.info("NotmuchDataSource initialized")

    @log_performance(operation="search_emails")
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches emails using a notmuch query string."""
        await self._ensure_initialized()
        
        if not self.notmuch_db:
            return []

        try:
            query = self.notmuch_db.create_query(search_term)
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
            logger.error(f"Error searching emails in notmuch: {e}")
            return []

    @log_performance(operation="get_email_by_message_id")
    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its notmuch message ID with improved content extraction."""
        await self._ensure_initialized()
        
        if not self.notmuch_db:
            return None

        query = self.db.create_query(f"id:{message_id}")
        messages = query.search_messages()

            if not messages:
                return None

            message = messages[0]
            
            # Load the full message from the file to extract content parts
            filename = message.get_filename()
            
            try:
                # Parse email content from file
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
                            elif part.get_content_type() == "text/html":
                                # If no plain text, use HTML content as fallback
                                if not content:
                                    payload = part.get_payload(decode=True)
                                    if payload:
                                        content = payload.decode('utf-8', errors='ignore')
                    else:
                        payload = email_message.get_payload(decode=True)
                        if payload:
                            content = payload.decode('utf-8', errors='ignore')
                    
                    email_data["body"] = content
                    
                return email_data
            except Exception as e:
                logger.error(f"Error processing email {message_id}: {e}")
                return {
                    "id": message.get_message_id(),
                    "message_id": message.get_message_id(),
                    "subject": message.get_header("subject"),
                    "sender": message.get_header("from"),
                    "date": message.get_date(),
                    "tags": list(message.get_tags()),
                    "body": f"Error decoding content: {e}"
                }

        except Exception as e:
            logger.error(f"Error retrieving email by message ID {message_id}: {e}")
            return None

    @log_performance(operation="get_emails")
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
        await self._ensure_initialized()
        
        query_parts = []
        if is_unread:
            query_parts.append("tag:unread")

        search_term = " ".join(query_parts) if query_parts else "*"

        if not self.notmuch_db:
            return []

        try:
            query = self.notmuch_db.create_query(search_term)
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
            logger.error(f"Error getting emails from notmuch: {e}")
            return []

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination."""
        return await self.get_emails(limit=limit, offset=offset)

    @log_performance(operation="get_all_categories")
    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """In notmuch, categories are tags."""
        await self._ensure_initialized()
        
        if not self.notmuch_db:
            return []
        
        try:
            tags = self.notmuch_db.get_all_tags()
            return [{"name": tag, "id": tag} for tag in tags]
        except Exception as e:
            logger.error(f"Error retrieving notmuch tags: {e}")
            return []

    @log_performance(operation="create_email")
    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email entry with AI analysis."""
        await self._ensure_initialized()
        
        logger.info(f"Creating email with subject: {email_data.get('subject', 'No subject')}")
        
        # This is a read-only implementation
        return None

    async def _analyze_and_tag_email_background(self, message_id: str, email_data: Dict[str, Any]):
        """Perform background AI analysis and tagging for a new email."""
        try:
            # Get the full email content for analysis
            subject = email_data.get("subject", "")
            content = email_data.get("body", "")
            full_text = f"{subject} {content}"

            analysis_results = {}

            # Sentiment analysis
            try:
                if self.ai_engine:
                    sentiment = self.ai_engine.analyze_sentiment(full_text)
                    if sentiment:
                        analysis_results["sentiment"] = sentiment
            except Exception as e:
                logger.warning(f"Sentiment analysis failed for email {message_id}: {e}")

            # Topic classification
            try:
                if self.ai_engine:
                    topics = self.ai_engine.classify_topic(full_text)
                    if topics:
                        analysis_results["topics"] = topics
            except Exception as e:
                logger.warning(f"Topic classification failed for email {message_id}: {e}")

            # Apply smart filters for categorization
            try:
                if self.filter_manager:
                    filter_results = await self.filter_manager.apply_filters_to_email({
                        "id": message_id,
                        "subject": subject,
                        "content": content,
                        "analysis": analysis_results
                    })

                    if filter_results:
                        analysis_results["smart_filters"] = filter_results

                        # Apply suggested tags based on filters
                        suggested_tags = filter_results.get("categories", [])
                        if suggested_tags:
                            # Add suggested tags
                            new_tags = suggested_tags
                            # Update tags in notmuch
                            await self.update_tags_for_message(message_id, new_tags)

            except Exception as e:
                logger.warning(f"Smart filtering failed for email {message_id}: {e}")

            logger.info(f"Completed background AI analysis and tagging for email {message_id}")
        except Exception as e:
            logger.error(f"Critical error in background email analysis and tagging for {message_id}: {e}")

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by ID - Notmuch uses string message IDs, not integer IDs."""
        # This is a compatibility method for the DataSource interface
        # In a real implementation, this would map internal IDs to message IDs
        logger.warning("get_email_by_id called but Notmuch uses string message IDs")
        return None

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category - Notmuch uses tags, not categories."""
        # This is a compatibility method for the DataSource interface
        # In Notmuch, categories are tags, so this would create a tag
        logger.warning("create_category called but Notmuch uses tags")
        return None

    @log_performance(operation="update_email_by_message_id")
    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an email by its message ID."""
        await self._ensure_initialized()
        
        logger.info(f"Updating email {message_id} with data: {update_data}")
        
        # This is a read-only implementation
        return None

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category - Notmuch uses string tags, not integer category IDs."""
        # This is a compatibility method for the DataSource interface
        # In Notmuch, categories are tags, so this would search by tag
        logger.warning("get_emails_by_category called but Notmuch uses string tags")
        return []

    @log_performance(operation="update_email")
    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an email by its internal ID."""
        await self._ensure_initialized()
        
        logger.info(f"Updating email ID {email_id} with data: {update_data}")
        
        # This is a read-only implementation
        return None

    async def delete_email(self, email_id: int) -> bool:
        """Delete an email by its internal ID."""
        await self._ensure_initialized()
        
        logger.info(f"Deleting email ID {email_id}")
        
        # This is a read-only implementation
        return False

    @log_performance(operation="get_dashboard_aggregates")
    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics for efficient server-side calculations."""
        await self._ensure_initialized()
        
        if not self.notmuch_db:
            return {
                "total_emails": 0,
                "auto_labeled": 0,
                "categories_count": 0,
                "unread_count": 0,
                "weekly_growth": {"emails": 0, "percentage": 0.0}
            }

        try:
            # Get total emails
            query = self.notmuch_db.create_query("*")
            total_emails = query.count_messages()

            # Get unread count
            unread_query = self.notmuch_db.create_query("tag:unread")
            unread_count = unread_query.count_messages()

            # For auto_labeled, we'll use a placeholder tag like "auto-labeled"
            auto_labeled_query = self.notmuch_db.create_query("tag:auto-labeled")
            auto_labeled = auto_labeled_query.count_messages()

            # For categories, we'll count distinct tags (excluding system tags)
            all_tags = self.notmuch_db.get_all_tags()
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
            logger.error(f"Error getting dashboard aggregates from notmuch: {e}")
            # Return default values on error
            return {
                "total_emails": 0,
                "auto_labeled": 0,
                "categories_count": 0,
                "unread_count": 0,
                "weekly_growth": {"emails": 0, "percentage": 0.0}
            }

    @log_performance(operation="get_category_breakdown")
    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit.
        
        In Notmuch, categories are mapped to tags. This implementation counts emails per tag
        and excludes common system tags to focus on user-defined categories.
        """
        await self._ensure_initialized()
        
        if not self.notmuch_db:
            return {}

        try:
            # Get all tags and their counts
            tag_counts = {}
            
            # Exclude common system tags
            system_tags = {"inbox", "unread", "sent", "draft", "deleted", "spam", "flagged", "replied", "forwarded"}
            
            # Get all tags from the database
            all_tags = list(self.notmuch_db.get_all_tags())
            
            # For each tag (that's not a system tag), count messages
            for tag in all_tags:
                if tag.lower() not in system_tags:
                    query = self.notmuch_db.create_query(f"tag:{tag}")
                    count = query.count_messages()
                    if count > 0:  # Only include tags with emails
                        tag_counts[tag] = count
            
            # Sort by count descending and apply limit
            sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_tags[:limit])
        except Exception as e:
            logger.error(f"Error getting category breakdown from notmuch: {e}")
            # Return empty dict on error
            return {}

    @log_performance(operation="update_tags_for_message")
    async def update_tags_for_message(self, message_id: str, tags: List[str]) -> bool:
        """
        Updates the tags for a given message ID in notmuch.
        """
        await self._ensure_initialized()
        
        if not self.notmuch_db:
            error_context = create_error_context(
                component="NotmuchDataSource",
                operation="update_tags_for_message",
                additional_context={"message_id": message_id}
            )
            error_id = log_error(
                "Notmuch database not available.",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.INTEGRATION,
                context=error_context
            )
            logger.error("Notmuch database not available. Error ID: {error_id}")
            return False

        try:
            # Find the message in notmuch
            query = self.notmuch_db.create_query(f"id:{message_id}")
            messages = list(query.search_messages())
            if not messages:
                error_context = create_error_context(
                    component="NotmuchDataSource",
                    operation="update_tags_for_message",
                    additional_context={"message_id": message_id}
                )
                error_id = log_error(
                    f"Message with ID {message_id} not found in notmuch.",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.DATA,
                    context=error_context
                )
                logger.error(f"Message with ID {message_id} not found in notmuch. Error ID: {error_id}")
                return False

            message = messages[0]

            # Update tags in notmuch
            message.freeze()
            message.remove_all_tags()
            for tag in tags:
                message.add_tag(tag)
            message.thaw()

            logger.info(f"Updated tags for message {message_id} in notmuch.")
            
            # Trigger re-analysis if AI engine is available
            if self.ai_engine:
                try:
                    asyncio.create_task(self._reanalyze_email(message_id))
                except Exception as e:
                    logger.warning(f"Failed to schedule re-analysis for email {message_id}: {e}")
            
            return True

        except Exception as e:
            error_context = create_error_context(
                component="NotmuchDataSource",
                operation="update_tags_for_message",
                additional_context={"message_id": message_id}
            )
            error_id = log_error(
                e,
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.INTEGRATION,
                context=error_context,
                details={"error_type": type(e).__name__}
            )
            logger.error(f"Error updating tags for message {message_id}: {e}. Error ID: {error_id}")
            return False

    async def _reanalyze_email(self, message_id: str):
        """Re-analyze an email after tags have been updated."""
        try:
            logger.info(f"Re-analyzing email {message_id} after tag update")
            
            # Get email content
            email_data = await self.get_email_by_message_id(message_id, include_content=True)
            if not email_data:
                logger.error(f"Could not retrieve email data for re-analysis {message_id}")
                return

            # Perform AI analysis
            subject = email_data.get("subject", "")
            content = email_data.get("body", "")
            full_text = f"{subject} {content}"

            analysis_results = {}

            # Sentiment analysis
            try:
                if self.ai_engine:
                    sentiment = self.ai_engine.analyze_sentiment(full_text)
                    if sentiment:
                        analysis_results["sentiment"] = sentiment
            except Exception as e:
                logger.warning(f"Sentiment analysis failed for email {message_id}: {e}")

            # Topic classification
            try:
                if self.ai_engine:
                    topics = self.ai_engine.classify_topic(full_text)
                    if topics:
                        analysis_results["topics"] = topics
            except Exception as e:
                logger.warning(f"Topic classification failed for email {message_id}: {e}")

            logger.info(f"Completed re-analysis for email {message_id}")
        except Exception as e:
            logger.error(f"Critical error in email re-analysis for {message_id}: {e}")

    async def analyze_and_tag_email(self, message_id: str) -> bool:
        """
        Performs comprehensive AI analysis on an email and applies intelligent tagging.
        """
        await self._ensure_initialized()
        
        if not self.ai_engine or not self.filter_manager:
            logger.warning("AI engine or filter manager not available for analysis")
            return False

        try:
            # Get email content
            email_data = await self.get_email_by_message_id(message_id, include_content=True)
            if not email_data:
                logger.error(f"Could not retrieve email data for {message_id}")
                return False

            # Perform AI analysis
            subject = email_data.get("subject", "")
            content = email_data.get("body", "")
            full_text = f"{subject} {content}"

            analysis_results = {}

            # Sentiment analysis
            try:
                if self.ai_engine:
                    sentiment = self.ai_engine.analyze_sentiment(full_text)
                    if sentiment:
                        analysis_results["sentiment"] = sentiment
            except Exception as e:
                logger.warning(f"Sentiment analysis failed for email {message_id}: {e}")

            # Topic classification
            try:
                if self.ai_engine:
                    topics = self.ai_engine.classify_topic(full_text)
                    if topics:
                        analysis_results["topics"] = topics
            except Exception as e:
                logger.warning(f"Topic classification failed for email {message_id}: {e}")

            # Apply smart filters for categorization
            try:
                if self.filter_manager:
                    filter_results = await self.filter_manager.apply_filters_to_email({
                        "id": message_id,
                        "subject": subject,
                        "content": content,
                        "analysis": analysis_results
                    })

                    if filter_results:
                        analysis_results["smart_filters"] = filter_results

                        # Apply suggested tags based on filters
                        suggested_tags = filter_results.get("categories", [])
                        if suggested_tags:
                            # Get current tags
                            current_tags = email_data.get("tags", [])
                            # Add suggested tags
                            new_tags = list(set(current_tags + suggested_tags))
                            # Update tags in notmuch
                            await self.update_tags_for_message(message_id, new_tags)

            except Exception as e:
                logger.warning(f"Smart filtering failed for email {message_id}: {e}")

            logger.info(f"Completed AI analysis and tagging for email {message_id}")
            return True

        except Exception as e:
            logger.error(f"Critical error in email analysis and tagging for {message_id}: {e}")
            return False

    async def shutdown(self) -> None:
        """Gracefully shutdown the data source and clean up resources."""
        if self.notmuch_db:
            self.notmuch_db.close()
            self.notmuch_db = None
        logger.info("NotmuchDataSource shutdown complete")
