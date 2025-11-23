"""
Email processing nodes for the workflow system.

This module contains specialized nodes for email processing workflows,
including data sources, preprocessing, AI analysis, filtering, and actions.
"""

import asyncio
import re
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from .node_base import BaseNode, NodePort, DataType, ExecutionContext, NodeExecutionError


class EmailSourceNode(BaseNode):
    """
    Node for sourcing emails from various providers.

    Supports Gmail, IMAP, and local file sources.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}

        self.input_ports = [
            NodePort("query", DataType.STRING, required=False, description="Search query for emails"),
            NodePort("limit", DataType.NUMBER, required=False, default_value=100, description="Maximum emails to retrieve")
        ]

        self.output_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True, description="List of retrieved emails"),
            NodePort("status", DataType.JSON, required=True, description="Operation status and metadata")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Retrieve emails based on configuration and inputs.

        Args:
            context: Execution context

        Returns:
            Dictionary with emails and status
        """
        try:
            query = self.get_input("query", "")
            limit = int(self.get_input("limit", 100))

            # Mock email retrieval - in real implementation, connect to email providers
            emails = self._mock_retrieve_emails(query, limit)

            status = {
                "success": True,
                "count": len(emails),
                "query": query,
                "limit": limit,
                "timestamp": datetime.now().isoformat()
            }

            return {
                "emails": emails,
                "status": status
            }

        except Exception as e:
            raise NodeExecutionError(self.node_id, f"Failed to retrieve emails: {str(e)}")

    def _mock_retrieve_emails(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """
        Mock email retrieval for demonstration.

        Args:
            query: Search query
            limit: Maximum number of emails

        Returns:
            List of mock email data
        """
        # Generate mock emails
        emails = []
        for i in range(min(limit, 10)):  # Mock up to 10 emails
            email = {
                "id": f"mock_email_{i}",
                "subject": f"Mock Email Subject {i}",
                "sender": f"user{i}@example.com",
                "recipients": ["recipient@example.com"],
                "date": (datetime.now() - timedelta(days=i)).isoformat(),
                "body": f"This is mock email body {i}. Query: {query}",
                "attachments": [],
                "labels": ["INBOX"],
                "read": i % 2 == 0
            }
            emails.append(email)

        return emails


class PreprocessingNode(BaseNode):
    """
    Node for cleaning and normalizing email data.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}

        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True, description="Raw emails to process")
        ]

        self.output_ports = [
            NodePort("processed_emails", DataType.EMAIL_LIST, required=True, description="Cleaned email data"),
            NodePort("stats", DataType.JSON, required=True, description="Processing statistics")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Clean and normalize email data.

        Args:
            context: Execution context

        Returns:
            Dictionary with processed emails and stats
        """
        try:
            emails = self.get_input("emails", [])

            processed_emails = []
            stats = {
                "total_emails": len(emails),
                "processed": 0,
                "errors": 0,
                "cleaned_fields": []
            }

            for email in emails:
                try:
                    processed_email = self._clean_email(email)
                    processed_emails.append(processed_email)
                    stats["processed"] += 1
                except Exception as e:
                    stats["errors"] += 1
                    # Log error but continue processing
                    context.variables.setdefault("errors", []).append({
                        "email_id": email.get("id"),
                        "error": str(e)
                    })

            stats["success_rate"] = stats["processed"] / stats["total_emails"] if stats["total_emails"] > 0 else 0

            return {
                "processed_emails": processed_emails,
                "stats": stats
            }

        except Exception as e:
            raise NodeExecutionError(self.node_id, f"Preprocessing failed: {str(e)}")

    def _clean_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean individual email data.

        Args:
            email: Raw email data

        Returns:
            Cleaned email data
        """
        cleaned = email.copy()

        # Normalize subject
        if "subject" in cleaned:
            cleaned["subject"] = self._clean_text(cleaned["subject"])

        # Normalize body
        if "body" in cleaned:
            cleaned["body"] = self._clean_text(cleaned["body"])

        # Normalize sender
        if "sender" in cleaned:
            cleaned["sender"] = cleaned["sender"].strip().lower()

        # Normalize recipients
        if "recipients" in cleaned and isinstance(cleaned["recipients"], list):
            cleaned["recipients"] = [r.strip().lower() for r in cleaned["recipients"]]

        # Ensure date is properly formatted
        if "date" in cleaned:
            try:
                # Try to parse and reformat date
                if isinstance(cleaned["date"], str):
                    # Assume ISO format, could add more parsing
                    datetime.fromisoformat(cleaned["date"].replace('Z', '+00:00'))
            except:
                cleaned["date"] = datetime.now().isoformat()

        return cleaned

    def _clean_text(self, text: str) -> str:
        """
        Clean text content.

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return str(text)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove null bytes
        text = text.replace('\x00', '')

        return text


class AIAnalysisNode(BaseNode):
    """
    Node for performing AI analysis on email data.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}

        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True, description="Emails to analyze")
        ]

        self.output_ports = [
            NodePort("analysis_results", DataType.JSON, required=True, description="AI analysis results"),
            NodePort("summary", DataType.JSON, required=True, description="Analysis summary")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Perform AI analysis on emails.

        Args:
            context: Execution context

        Returns:
            Dictionary with analysis results and summary
        """
        try:
            emails = self.get_input("emails", [])

            analysis_results = []
            summary = {
                "total_emails": len(emails),
                "analyzed": 0,
                "sentiment_distribution": {},
                "topic_categories": {},
                "average_confidence": 0.0
            }

            total_confidence = 0.0

            for email in emails:
                try:
                    analysis = await self._analyze_email(email)
                    analysis_results.append(analysis)

                    # Update summary stats
                    sentiment = analysis.get("sentiment", "neutral")
                    summary["sentiment_distribution"][sentiment] = summary["sentiment_distribution"].get(sentiment, 0) + 1

                    topics = analysis.get("topics", [])
                    for topic in topics:
                        summary["topic_categories"][topic] = summary["topic_categories"].get(topic, 0) + 1

                    confidence = analysis.get("confidence", 0.5)
                    total_confidence += confidence

                    summary["analyzed"] += 1

                except Exception as e:
                    # Log error but continue
                    context.variables.setdefault("analysis_errors", []).append({
                        "email_id": email.get("id"),
                        "error": str(e)
                    })

            if summary["analyzed"] > 0:
                summary["average_confidence"] = total_confidence / summary["analyzed"]

            return {
                "analysis_results": analysis_results,
                "summary": summary
            }

        except Exception as e:
            raise NodeExecutionError(self.node_id, f"AI analysis failed: {str(e)}")

    async def _analyze_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze individual email with AI.

        Args:
            email: Email data to analyze

        Returns:
            Analysis results
        """
        # Mock AI analysis - in real implementation, call AI services
        subject = email.get("subject", "")
        body = email.get("body", "")

        # Simple mock analysis based on keywords
        text = f"{subject} {body}".lower()

        # Sentiment analysis
        if any(word in text for word in ["great", "excellent", "amazing", "love"]):
            sentiment = "positive"
        elif any(word in text for word in ["bad", "terrible", "hate", "awful"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Topic categorization
        topics = []
        if any(word in text for word in ["meeting", "schedule", "appointment"]):
            topics.append("meetings")
        if any(word in text for word in ["project", "task", "deadline"]):
            topics.append("work")
        if any(word in text for word in ["invoice", "payment", "billing"]):
            topics.append("finance")

        return {
            "email_id": email.get("id"),
            "sentiment": sentiment,
            "topics": topics,
            "confidence": 0.85,  # Mock confidence score
            "key_phrases": ["important", "meeting"],  # Mock key phrases
            "analyzed_at": datetime.now().isoformat()
        }


class FilterNode(BaseNode):
    """
    Node for filtering emails based on configurable criteria.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}

        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True, description="Emails to filter"),
            NodePort("criteria", DataType.JSON, required=False, description="Filter criteria")
        ]

        self.output_ports = [
            NodePort("filtered_emails", DataType.EMAIL_LIST, required=True, description="Emails that match criteria"),
            NodePort("discarded_emails", DataType.EMAIL_LIST, required=True, description="Emails that don't match"),
            NodePort("stats", DataType.JSON, required=True, description="Filtering statistics")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Filter emails based on criteria.

        Args:
            context: Execution context

        Returns:
            Dictionary with filtered results and stats
        """
        try:
            emails = self.get_input("emails", [])
            criteria = self.get_input("criteria", self.config.get("default_criteria", {}))

            filtered_emails = []
            discarded_emails = []
            stats = {
                "total_emails": len(emails),
                "filtered": 0,
                "discarded": 0,
                "criteria_applied": criteria
            }

            for email in emails:
                if self._matches_criteria(email, criteria):
                    filtered_emails.append(email)
                    stats["filtered"] += 1
                else:
                    discarded_emails.append(email)
                    stats["discarded"] += 1

            return {
                "filtered_emails": filtered_emails,
                "discarded_emails": discarded_emails,
                "stats": stats
            }

        except Exception as e:
            raise NodeExecutionError(self.node_id, f"Filtering failed: {str(e)}")

    def _matches_criteria(self, email: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Check if email matches filter criteria.

        Args:
            email: Email data
            criteria: Filter criteria

        Returns:
            True if email matches criteria
        """
        # Check sender
        if "sender" in criteria:
            sender_pattern = criteria["sender"]
            if not re.search(sender_pattern, email.get("sender", ""), re.IGNORECASE):
                return False

        # Check subject
        if "subject" in criteria:
            subject_pattern = criteria["subject"]
            if not re.search(subject_pattern, email.get("subject", ""), re.IGNORECASE):
                return False

        # Check date range
        if "date_from" in criteria:
            try:
                email_date = datetime.fromisoformat(email.get("date", "").replace('Z', '+00:00'))
                from_date = datetime.fromisoformat(criteria["date_from"])
                if email_date < from_date:
                    return False
            except:
                pass  # Skip date filtering if parsing fails

        if "date_to" in criteria:
            try:
                email_date = datetime.fromisoformat(email.get("date", "").replace('Z', '+00:00'))
                to_date = datetime.fromisoformat(criteria["date_to"])
                if email_date > to_date:
                    return False
            except:
                pass

        # Check labels
        if "labels" in criteria:
            required_labels = set(criteria["labels"])
            email_labels = set(email.get("labels", []))
            if not required_labels.issubset(email_labels):
                return False

        # Check read status
        if "read" in criteria:
            if email.get("read") != criteria["read"]:
                return False

        return True


class ActionNode(BaseNode):
    """
    Node for executing actions on emails.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}

        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True, description="Emails to act upon"),
            NodePort("action", DataType.STRING, required=True, description="Action to perform"),
            NodePort("parameters", DataType.JSON, required=False, description="Action parameters")
        ]

        self.output_ports = [
            NodePort("results", DataType.JSON, required=True, description="Action execution results"),
            NodePort("status", DataType.JSON, required=True, description="Operation status")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute action on emails.

        Args:
            context: Execution context

        Returns:
            Dictionary with action results and status
        """
        try:
            emails = self.get_input("emails", [])
            action = self.get_input("action", "")
            parameters = self.get_input("parameters", {})

            results = []
            status = {
                "action": action,
                "total_emails": len(emails),
                "processed": 0,
                "successful": 0,
                "failed": 0,
                "errors": []
            }

            for email in emails:
                try:
                    result = await self._execute_action(email, action, parameters, context)
                    results.append(result)
                    status["processed"] += 1
                    if result.get("success", False):
                        status["successful"] += 1
                    else:
                        status["failed"] += 1
                except Exception as e:
                    status["failed"] += 1
                    status["errors"].append({
                        "email_id": email.get("id"),
                        "error": str(e)
                    })

            return {
                "results": results,
                "status": status
            }

        except Exception as e:
            raise NodeExecutionError(self.node_id, f"Action execution failed: {str(e)}")

    async def _execute_action(self, email: Dict[str, Any], action: str, parameters: Dict[str, Any], context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute specific action on email.

        Args:
            email: Email data
            action: Action to perform
            parameters: Action parameters
            context: Execution context

        Returns:
            Action result
        """
        email_id = email.get("id", "unknown")

        if action == "move":
            # Mock move action
            folder = parameters.get("folder", "INBOX")
            return {
                "email_id": email_id,
                "action": "move",
                "success": True,
                "new_folder": folder,
                "timestamp": datetime.now().isoformat()
            }

        elif action == "label":
            # Mock label action
            labels = parameters.get("labels", [])
            return {
                "email_id": email_id,
                "action": "label",
                "success": True,
                "added_labels": labels,
                "timestamp": datetime.now().isoformat()
            }

        elif action == "mark_read":
            # Mock mark as read
            return {
                "email_id": email_id,
                "action": "mark_read",
                "success": True,
                "timestamp": datetime.now().isoformat()
            }

        elif action == "delete":
            # Mock delete action
            return {
                "email_id": email_id,
                "action": "delete",
                "success": True,
                "timestamp": datetime.now().isoformat()
            }

        else:
            raise ValueError(f"Unsupported action: {action}")