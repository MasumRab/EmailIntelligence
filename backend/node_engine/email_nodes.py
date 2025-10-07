"""
Node implementations for the Email Intelligence Platform.

This module contains specific node implementations for email processing
functionality, following the node-based architecture.
"""
from backend.node_engine.workflow_engine import workflow_engine
import asyncio
from typing import Any, Dict, List
from datetime import datetime

from backend.node_engine.node_base import (
    BaseNode, NodePort, DataType, ExecutionContext
)
# Temporarily using a simplified NLP engine to avoid merge conflicts in original file


class NLPEngine:
    """Simplified NLP Engine for testing purposes."""

    def analyze_email(self, subject: str, content: str) -> dict:
        """Simplified email analysis for testing."""
        # This is a basic implementation for testing
        text = f"{subject} {content}".lower()

        # Simple sentiment analysis
        sentiment = "positive" if any(
            w in text for w in [
                "good",
                "great",
                "excellent",
                "thank"]) else "negative" if any(
            w in text for w in [
                "bad",
                "terrible",
                "problem"]) else "neutral"

        # Simple topic analysis
        topic = "work_business" if any(w in text for w in ["meeting", "project", "work"]) else \
            "personal" if any(w in text for w in ["family", "friend", "personal"]) else \
            "general"

        # Return a basic analysis structure
        return {
            "topic": topic,
            "sentiment": sentiment,
            "intent": "informational",
            "urgency": "medium",
            "confidence": 0.7,
            "categories": [topic],
            "keywords": ["sample", "keywords"],
            "reasoning": f"Basic analysis of subject and content",
            "suggested_labels": [topic],
            "risk_flags": [],
            "validation": {
                "method": "basic",
                "score": 0.7,
                "reliable": True,
                "feedback": "Analysis completed"
            },
            "details": {
                "sentiment_analysis": {"sentiment": sentiment, "confidence": 0.7},
                "topic_analysis": {"topic": topic, "confidence": 0.7},
                "intent_analysis": {"intent": "informational", "confidence": 0.7},
                "urgency_analysis": {"urgency": "medium", "confidence": 0.7},
            }
        }
# Temporarily using simplified classes to avoid merge conflicts in original files


class AdvancedAIEngine:
    """Simplified AI Engine for testing purposes."""
    pass


class AIAnalysisResult:
    """Simplified AI Analysis Result for testing purposes."""
    pass


class GmailAIService:
    """Simplified Gmail Service for testing purposes."""
    pass


class EmailSourceNode(BaseNode):
    """
    Node that sources emails from various providers (Gmail, etc.).
    """

    def __init__(self, config: Dict[str, Any] = None, node_id: str = None, name: str = None):
        super().__init__(node_id, name or "Email Source", "Sources emails from email provider")
        self.config = config or {}
        self.input_ports = []
        self.output_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True,
                     description="List of retrieved emails"),
            NodePort("status", DataType.JSON, required=True,
                     description="Status information about the operation")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute the email source operation."""
        try:
            # For now, we'll simulate email retrieval
            # In a real implementation, this would connect to email APIs
            emails = await self._fetch_emails()

            result = {
                "emails": emails,
                "status": {
                    "success": True,
                    "count": len(emails),
                    "timestamp": datetime.now().isoformat()
                }
            }

            return result
        except Exception as e:
            context.add_error(self.node_id, f"Email source failed: {str(e)}")
            return {
                "emails": [],
                "status": {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }

    async def _fetch_emails(self) -> List[Dict[str, Any]]:
        """Fetch emails from the configured provider."""
        # This is a placeholder - in real implementation, it would use GmailAIService
        # or other email providers
        await asyncio.sleep(0.1)  # Simulate network delay

        # Return sample emails for demonstration
        return [
            {
                "id": "1",
                "subject": "Sample Email Subject",
                "content": "This is a sample email content for demonstration purposes.",
                "from": "sender@example.com",
                "to": ["recipient@example.com"],
                "timestamp": datetime.now().isoformat(),
                "labels": ["inbox"]
            }
        ]


class PreprocessingNode(BaseNode):
    """
    Node that preprocesses email data (cleaning, normalization, etc.).
    """

    def __init__(self, config: Dict[str, Any] = None, node_id: str = None, name: str = None):
        super().__init__(node_id, name or "Email Preprocessor", "Preprocesses email data")
        self.config = config or {}
        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True,
                     description="List of emails to preprocess")
        ]
        self.output_ports = [
            NodePort("processed_emails", DataType.EMAIL_LIST, required=True,
                     description="List of preprocessed emails"),
            NodePort("stats", DataType.JSON, required=True,
                     description="Statistics about preprocessing")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute the preprocessing operation."""
        try:
            input_emails = self.inputs.get("emails", [])

            if not input_emails:
                return {
                    "processed_emails": [],
                    "stats": {
                        "processed_count": 0,
                        "errors": 0,
                        "timestamp": datetime.now().isoformat()
                    }
                }

            processed_emails = []
            errors = 0

            for email in input_emails:
                try:
                    processed_email = await self._process_email(email)
                    processed_emails.append(processed_email)
                except Exception:
                    errors += 1
                    continue  # Skip the problematic email

            result = {
                "processed_emails": processed_emails,
                "stats": {
                    "processed_count": len(processed_emails),
                    "errors": errors,
                    "timestamp": datetime.now().isoformat()
                }
            }

            return result
        except Exception as e:
            context.add_error(self.node_id, f"Preprocessing failed: {str(e)}")
            return {
                "processed_emails": [],
                "stats": {
                    "processed_count": 0,
                    "errors": "Error during preprocessing",
                    "timestamp": datetime.now().isoformat()
                }
            }

    async def _process_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single email."""
        # Simulate some preprocessing steps
        processed_email = email.copy()

        # Clean content
        content = processed_email.get("content", "")
        if content:
            # Remove extra whitespace and normalize
            processed_email["content"] = " ".join(content.split())

        # Normalize subject
        subject = processed_email.get("subject", "")
        if subject:
            processed_email["subject"] = subject.strip()

        # Add processing timestamp
        processed_email["processed_at"] = datetime.now().isoformat()

        return processed_email


class AIAnalysisNode(BaseNode):
    """
    Node that performs AI analysis on emails (sentiment, topic, intent, etc.).
    """

    def __init__(self, config: Dict[str, Any] = None, node_id: str = None, name: str = None):
        super().__init__(node_id, name or "AI Analyzer", "Performs AI analysis on emails")
        self.config = config or {}
        self.nlp_engine = NLPEngine()
        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True,
                     description="List of emails to analyze")
        ]
        self.output_ports = [
            NodePort("analysis_results", DataType.JSON, required=True,
                     description="AI analysis results for each email"),
            NodePort("summary", DataType.JSON, required=True,
                     description="Summary of the analysis")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute the AI analysis operation."""
        try:
            input_emails = self.inputs.get("emails", [])

            if not input_emails:
                return {
                    "analysis_results": [],
                    "summary": {
                        "analyzed_count": 0,
                        "timestamp": datetime.now().isoformat()
                    }
                }

            results = []

            for email in input_emails:
                subject = email.get("subject", "")
                content = email.get("content", "")

                # Analyze the email using the NLP engine
                analysis = self.nlp_engine.analyze_email(subject, content)
                results.append({
                    "email_id": email.get("id"),
                    "analysis": analysis
                })

            summary = {
                "analyzed_count": len(results),
                "timestamp": datetime.now().isoformat()
            }

            return {
                "analysis_results": results,
                "summary": summary
            }
        except Exception as e:
            context.add_error(self.node_id, f"AI analysis failed: {str(e)}")
            return {
                "analysis_results": [],
                "summary": {
                    "analyzed_count": 0,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }


class FilterNode(BaseNode):
    """
    Node that applies filtering rules to emails.
    """

    def __init__(self, config: Dict[str, Any] = None, node_id: str = None, name: str = None):
        super().__init__(node_id, name or "Email Filter", "Filters emails based on criteria")
        self.config = config or {}
        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True,
                     description="List of emails to filter"),
            NodePort("criteria", DataType.JSON, required=False,
                     description="Filtering criteria (optional override)")
        ]
        self.output_ports = [
            NodePort("filtered_emails", DataType.EMAIL_LIST, required=True,
                     description="Filtered email list"),
            NodePort("discarded_emails", DataType.EMAIL_LIST, required=True,
                     description="Emails that didn't match criteria"),
            NodePort("stats", DataType.JSON, required=True,
                     description="Filtering statistics")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute the filtering operation."""
        try:
            input_emails = self.inputs.get("emails", [])
            criteria = self.inputs.get("criteria", self.config.get("criteria", {}))

            if not input_emails:
                return {
                    "filtered_emails": [],
                    "discarded_emails": [],
                    "stats": {
                        "filtered_count": 0,
                        "discarded_count": 0,
                        "timestamp": datetime.now().isoformat()
                    }
                }

            filtered_emails = []
            discarded_emails = []

            for email in input_emails:
                if self._matches_criteria(email, criteria):
                    filtered_emails.append(email)
                else:
                    discarded_emails.append(email)

            return {
                "filtered_emails": filtered_emails,
                "discarded_emails": discarded_emails,
                "stats": {
                    "filtered_count": len(filtered_emails),
                    "discarded_count": len(discarded_emails),
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            context.add_error(self.node_id, f"Filtering failed: {str(e)}")
            return {
                "filtered_emails": [],
                "discarded_emails": [],
                "stats": {
                    "filtered_count": 0,
                    "discarded_count": 0,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }

    def _matches_criteria(self, email: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if an email matches the filtering criteria."""
        # This is a basic implementation - in reality, this would be more sophisticated
        if not criteria:
            return True  # If no criteria, pass everything through

        subject = email.get("subject", "").lower()
        content = email.get("content", "").lower()
        sender = email.get("from", "").lower()

        # Check for required keywords in subject or content
        required_keywords = criteria.get("required_keywords", [])
        if required_keywords:
            text = f"{subject} {content}"
            if not any(keyword.lower() in text for keyword in required_keywords):
                return False

        # Check for excluded senders
        excluded_senders = criteria.get("excluded_senders", [])
        if sender in [s.lower() for s in excluded_senders]:
            return False

        # Check for priority senders
        priority_senders = criteria.get("priority_senders", [])
        if priority_senders and sender in [s.lower() for s in priority_senders]:
            return True  # Priority emails always pass

        # Default behavior
        return True


class ActionNode(BaseNode):
    """
    Node that executes actions on emails (move, label, forward, etc.).
    """

    def __init__(self, config: Dict[str, Any] = None, node_id: str = None, name: str = None):
        super().__init__(node_id, name or "Action Executor", "Executes actions on emails")
        self.config = config or {}
        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True,
                     description="List of emails to act upon"),
            NodePort("actions", DataType.JSON, required=True,
                     description="Actions to perform on emails")
        ]
        self.output_ports = [
            NodePort("results", DataType.JSON, required=True,
                     description="Results of the actions performed"),
            NodePort("status", DataType.JSON, required=True,
                     description="Status of action execution")
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute the action operation."""
        try:
            input_emails = self.inputs.get("emails", [])
            actions = self.inputs.get("actions", [])

            if not input_emails:
                return {
                    "results": [],
                    "status": {
                        "success": True,
                        "processed_count": 0,
                        "timestamp": datetime.now().isoformat()
                    }
                }

            results = []

            for email in input_emails:
                email_result = await self._execute_actions_on_email(email, actions)
                results.append(email_result)

            return {
                "results": results,
                "status": {
                    "success": True,
                    "processed_count": len(input_emails),
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            context.add_error(self.node_id, f"Action execution failed: {str(e)}")
            return {
                "results": [],
                "status": {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }

    async def _execute_actions_on_email(self, email: Dict[str, Any], actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute actions on a single email."""
        # Simulate action execution
        # In a real implementation, this would interact with email APIs
        await asyncio.sleep(0.05)  # Simulate processing time

        result = {
            "email_id": email.get("id"),
            "actions_performed": [],
            "success": True
        }

        for action in actions:
            action_type = action.get("type", "unknown")
            action_result = {
                "type": action_type,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }

            # Simulate different types of actions
            if action_type == "label":
                label = action.get("label", "no_label")
                action_result["details"] = f"Labeled as {label}"
            elif action_type == "move":
                folder = action.get("folder", "inbox")
                action_result["details"] = f"Moved to {folder}"
            elif action_type == "forward":
                to = action.get("to", "unknown")
                action_result["details"] = f"Forwarded to {to}"
            else:
                action_result["details"] = f"Executed {action_type} action"

            result["actions_performed"].append(action_result)

        return result


# Register the node types with the global workflow engine

workflow_engine.register_node_type(EmailSourceNode)
workflow_engine.register_node_type(PreprocessingNode)
workflow_engine.register_node_type(AIAnalysisNode)
workflow_engine.register_node_type(FilterNode)
workflow_engine.register_node_type(ActionNode)
