"""
Enhanced Notmuch Data Source with AI Integration

This module provides a powerful data source that integrates with all existing
EmailIntelligence features including AI analysis, smart filtering, workflows,
and performance monitoring.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone

import notmuch

from .data_source import DataSource
from .database import DatabaseManager
from backend.python_nlp.smart_filters import SmartFilterManager
from backend.python_backend.performance_monitor import log_performance

logger = logging.getLogger(__name__)


class NotmuchDataSource(DataSource):
    """
    Enhanced data source that integrates AI analysis, smart filtering,
    and workflow processing for comprehensive email intelligence.
    This implementation combines Notmuch database access with AI capabilities.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.notmuch_db = None
        self.db = None
        self.ai_engine = None
        self.filter_manager = None
        self._initialized = False
        
        # Initialize Notmuch database
        try:
            self.notmuch_db = notmuch.Database(db_path)
        except Exception as e:
            logger.error(f"Error opening notmuch database: {e}")
            self.notmuch_db = None

    async def _ensure_initialized(self):
        """Ensure all components are properly initialized."""
        if self._initialized:
            return

        # Initialize database connection
        if self.db is None:
            self.db = DatabaseManager()
            await self.db._ensure_initialized()

        # Initialize AI engine
        if self.ai_engine is None:
            # For NotmuchDataSource, we create the engine directly
            # since we're not in a FastAPI dependency injection context
            from .ai_engine import ModernAIEngine
            self.ai_engine = ModernAIEngine()
            self.ai_engine.initialize()

        # Initialize smart filter manager
        if self.filter_manager is None:
            self.filter_manager = SmartFilterManager()

        self._initialized = True
        logger.info("NotmuchDataSource fully initialized with AI and smart filtering integration")

    @log_performance(operation="create_email_ai")
    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email with automatic AI analysis and processing."""
        await self._ensure_initialized()

        try:
            # Create the email in database
            created_email = await self.db.create_email(email_data)
            if not created_email:
                return None

            email_id = created_email.get("id")
            content = email_data.get("content", "")
            subject = email_data.get("subject", "")

            # Perform AI analysis asynchronously
            asyncio.create_task(self._analyze_email_async(email_id, subject, content))

            logger.info(f"Created email {email_id} with AI analysis queued")
            return created_email

        except Exception as e:
            logger.error(f"Error creating email: {e}")
            return None

    async def _analyze_email_async(self, email_id: int, subject: str, content: str):
        """Perform comprehensive AI analysis on an email asynchronously."""
        try:
            full_text = f"{subject} {content}"

            # Perform AI analysis
            analysis_results = {}

            # Sentiment analysis
            try:
                sentiment = self.ai_engine.analyze_sentiment(full_text)
                if sentiment:
                    analysis_results["sentiment"] = sentiment
            except Exception as e:
                logger.warning(f"Sentiment analysis failed for email {email_id}: {e}")

            # Topic classification
            try:
                topics = self.ai_engine.classify_topic(full_text)
                if topics:
                    analysis_results["topics"] = topics
            except Exception as e:
                logger.warning(f"Topic classification failed for email {email_id}: {e}")

            # Intent recognition
            try:
                intent = self.ai_engine.recognize_intent(full_text)
                if intent:
                    analysis_results["intent"] = intent
            except Exception as e:
                logger.warning(f"Intent recognition failed for email {email_id}: {e}")

            # Urgency detection
            try:
                urgency = self.ai_engine.detect_urgency(full_text)
                if urgency:
                    analysis_results["urgency"] = urgency
            except Exception as e:
                logger.warning(f"Urgency detection failed for email {email_id}: {e}")

            # Apply smart filters for categorization
            try:
                filter_results = await self.filter_manager.apply_filters_to_email({
                    "id": email_id,
                    "subject": subject,
                    "content": content,
                    "analysis": analysis_results
                })

                if filter_results:
                    analysis_results["smart_filters"] = filter_results

                    # Auto-categorize based on filters
                    suggested_category = self._determine_category_from_filters(filter_results)
                    if suggested_category:
                        analysis_results["suggested_category"] = suggested_category

            except Exception as e:
                logger.warning(f"Smart filtering failed for email {email_id}: {e}")

            # Update email with analysis results
            update_data = {
                "analysis_metadata": analysis_results,
                "analyzed_at": datetime.now(timezone.utc).isoformat()
            }

            await self.db.update_email_by_id(email_id, update_data)

            logger.info(f"Completed AI analysis for email {email_id}")

        except Exception as e:
            logger.error(f"Critical error in email analysis for {email_id}: {e}")

    def _determine_category_from_filters(self, filter_results: Dict[str, Any]) -> Optional[str]:
        """Determine suggested category based on filter results."""
        # This is a simple implementation - could be enhanced with ML
        categories = filter_results.get("categories", [])

        if not categories:
            return None

        # Return the highest confidence category
        if isinstance(categories, list) and categories:
            return categories[0]  # Could implement scoring logic here

        return None

    @log_performance(operation="get_email")
    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieve an email by ID with full analysis data."""
        await self._ensure_initialized()

        try:
            email = await self.db.get_email_by_id(email_id, include_content)
            if email and email.get("analysis_metadata"):
                # Enhance with additional processing if needed
                pass
            return email
        except Exception as e:
            logger.error(f"Error retrieving email {email_id}: {e}")
            return None

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieves an email by its notmuch message ID."""
        if not self.notmuch_db:
            return None

        try:
            query = self.notmuch_db.create_query(f"id:{message_id}")
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
        except Exception as e:
            logger.error(f"Error retrieving email by message ID {message_id}: {e}")
            return None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with usage statistics."""
        await self._ensure_initialized()

        try:
            # First try to get categories from our database
            categories = await self.db.get_all_categories()

            # Enhance with email counts
            for category in categories:
                category_id = category.get("id")
                if category_id:
                    # Get email count for this category
                    emails_in_category = await self.db.get_emails_by_category_id(category_id)
                    category["email_count"] = len(emails_in_category)

            return categories
        except Exception as e:
            logger.error(f"Error retrieving categories: {e}")
            # Fallback to notmuch tags
            if self.notmuch_db:
                try:
                    tags = self.notmuch_db.get_all_tags()
                    return [{"name": tag, "id": tag} for tag in tags]
                except Exception as e2:
                    logger.error(f"Error retrieving notmuch tags: {e2}")
            return []

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category."""
        await self._ensure_initialized()

        try:
            return await self.db.create_category(category_data)
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            return None

    @log_performance(operation="get_emails_filtered")
    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Get emails with intelligent filtering and sorting."""
        await self._ensure_initialized()

        try:
            emails = await self.db.get_emails(limit, offset, category_id, is_unread)

            # Enhance emails with analysis insights
            for email in emails:
                analysis = email.get("analysis_metadata", {})
                if analysis:
                    # Add analysis summary for quick access
                    email["analysis_summary"] = {
                        "sentiment": analysis.get("sentiment", {}).get("label"),
                        "urgency": analysis.get("urgency", {}).get("level"),
                        "has_filters": bool(analysis.get("smart_filters"))
                    }

            return emails
        except Exception as e:
            logger.error(f"Error retrieving emails: {e}")
            return []

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an email by message ID."""
        await self._ensure_initialized()

        try:
            return await self.db.update_email_by_message_id(message_id, update_data)
        except Exception as e:
            logger.error(f"Error updating email {message_id}: {e}")
            return None

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with AI-enhanced metadata."""
        return await self.get_emails(limit, offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category ID with smart filtering."""
        return await self.get_emails(limit, offset, category_id)

    @log_performance(operation="search_emails_ai")
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Perform intelligent search across emails and analysis data."""
        await self._ensure_initialized()

        try:
            # Basic text search
            basic_results = await self.db.search_emails(search_term, limit * 2)  # Get more for ranking

            # Enhance with AI-powered ranking
            scored_results = []
            for email in basic_results:
                score = self._calculate_search_relevance(email, search_term)
                scored_results.append((email, score))

            # Sort by relevance score
            scored_results.sort(key=lambda x: x[1], reverse=True)

            # Return top results
            results = [email for email, score in scored_results[:limit]]

            # Add search metadata
            for email in results:
                email["search_metadata"] = {
                    "search_term": search_term,
                    "relevance_score": next(score for e, score in scored_results if e["id"] == email["id"])
                }

            return results

        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            # Fallback to basic search
            return await self.db.search_emails(search_term, limit)

    def _calculate_search_relevance(self, email: Dict[str, Any], search_term: str) -> float:
        """Calculate search relevance score using analysis data."""
        score = 0.0
        search_lower = search_term.lower()

        # Basic text matching (subject and content)
        subject = email.get("subject", "").lower()
        content = email.get("content", "").lower()

        if search_lower in subject:
            score += 2.0  # Subject matches are highly relevant
        if search_lower in content:
            score += 1.0  # Content matches are relevant

        # AI analysis boost
        analysis = email.get("analysis_metadata", {})

        # Sentiment-based relevance
        sentiment = analysis.get("sentiment", {})
        if search_term.lower() in ["positive", "negative", "neutral"]:
            if sentiment.get("label", "").lower() == search_term.lower():
                score += 1.5

        # Topic-based relevance
        topics = analysis.get("topics", [])
        if any(search_lower in topic.lower() for topic in topics):
            score += 1.2

        # Intent-based relevance
        intent = analysis.get("intent", {})
        if search_lower in intent.get("type", "").lower():
            score += 1.1

        return score

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an email with smart processing."""
        await self._ensure_initialized()

        try:
            # If content is being updated, re-run analysis
            if "content" in update_data or "subject" in update_data:
                email = await self.db.get_email_by_id(email_id)
                if email:
                    subject = update_data.get("subject", email.get("subject", ""))
                    content = update_data.get("content", email.get("content", ""))

                    # Queue re-analysis
                    asyncio.create_task(self._analyze_email_async(email_id, subject, content))

            return await self.db.update_email_by_id(email_id, update_data)

        except Exception as e:
            logger.error(f"Error updating email {email_id}: {e}")
            return None

<<<<<<< HEAD
=======
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

>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2
    async def shutdown(self) -> None:
        """Gracefully shutdown the data source and clean up resources."""
        logger.info("Shutting down NotmuchDataSource")

        try:
            if self.notmuch_db:
                self.notmuch_db.close()
                self.notmuch_db = None
            if self.db:
                await self.db.close()
            if self.filter_manager:
                await self.filter_manager.cleanup()

        except Exception as e:
            logger.error(f"Error during NotmuchDataSource shutdown: {e}")

        logger.info("NotmuchDataSource shutdown complete")

    # Additional AI-enhanced methods

    async def get_emails_by_sentiment(self, sentiment: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get emails filtered by sentiment analysis."""
        await self._ensure_initialized()

        try:
            all_emails = await self.db.get_all_emails(limit * 5)  # Get more to filter
            filtered_emails = []

            for email in all_emails:
                analysis = email.get("analysis_metadata", {})
                email_sentiment = analysis.get("sentiment", {}).get("label", "").lower()
                if email_sentiment == sentiment.lower():
                    filtered_emails.append(email)
                    if len(filtered_emails) >= limit:
                        break

            return filtered_emails

        except Exception as e:
            logger.error(f"Error filtering emails by sentiment: {e}")
            return []

    async def get_emails_by_urgency(self, urgency_level: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get emails filtered by urgency level."""
        await self._ensure_initialized()

        try:
            all_emails = await self.db.get_all_emails(limit * 5)
            filtered_emails = []

            for email in all_emails:
                analysis = email.get("analysis_metadata", {})
                urgency = analysis.get("urgency", {}).get("level", "").lower()
                if urgency == urgency_level.lower():
                    filtered_emails.append(email)
                    if len(filtered_emails) >= limit:
                        break

            return filtered_emails

        except Exception as e:
            logger.error(f"Error filtering emails by urgency: {e}")
            return []

    async def get_smart_filter_suggestions(self, email_id: int) -> Dict[str, Any]:
        """Get smart filter suggestions for an email."""
        await self._ensure_initialized()

        try:
            email = await self.db.get_email_by_id(email_id)
            if not email:
                return {}

            # Apply smart filters
            filter_results = await self.filter_manager.apply_filters_to_email(email)

            return {
                "email_id": email_id,
                "suggested_filters": filter_results,
                "confidence_scores": self._calculate_filter_confidence(filter_results)
            }

        except Exception as e:
            logger.error(f"Error getting smart filter suggestions for email {email_id}: {e}")
            return {}

    def _calculate_filter_confidence(self, filter_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for filter suggestions."""
        # Simple implementation - could be enhanced with ML
        confidence = {}

        if "categories" in filter_results:
            confidence["category"] = min(1.0, len(filter_results["categories"]) * 0.3)

        if "priority" in filter_results:
            confidence["priority"] = 0.8  # High confidence for priority detection

        if "spam_likelihood" in filter_results:
            confidence["spam"] = filter_results["spam_likelihood"]

        return confidence