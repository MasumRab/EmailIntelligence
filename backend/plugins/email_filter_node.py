"""
It will be removed in a future release.

Sample Email Processing Node Plugin for Email Intelligence Platform

Implements a sample processing node for the node-based workflow system.
"""

from typing import Any, Dict, Type
from backend.plugins.base_plugin import ProcessingNode


class EmailFilterNode(ProcessingNode):
    """
    A sample processing node that filters emails based on specified criteria.
    """

    def __init__(self):
        self._initialized = False

    @property
    def name(self) -> str:
        return "email_filter"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def input_types(self) -> Dict[str, Type]:
        return {
            "emails": list,  # List of email objects
            "filter_criteria": dict,  # Criteria for filtering
        }

    @property
    def output_types(self) -> Dict[str, Type]:
        return {
            "filtered_emails": list,  # Filtered list of email objects
            "stats": dict,  # Statistics about filtering
        }

    def initialize(self) -> bool:
        """Initialize the plugin."""
        self._initialized = True
        return True

    def process(self, data: Any) -> Any:
        """Process the input data."""
        # For this sample, we'll just pass through the run method
        if isinstance(data, dict) and "emails" in data and "filter_criteria" in data:
            return self.run(emails=data["emails"], filter_criteria=data["filter_criteria"])
        return {"filtered_emails": [], "stats": {}}

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the node with the provided inputs.
        Returns a dictionary of outputs based on output_types.
        """
        emails = kwargs.get("emails", [])
        criteria = kwargs.get("filter_criteria", {})

        # Apply filtering based on criteria
        filtered_emails = []
        for email in emails:
            include = True

            # Example: filter by sender
            if "sender" in criteria:
                sender_filter = criteria["sender"]
                if sender_filter and email.get("sender", "").lower() != sender_filter.lower():
                    include = False

            # Example: filter by subject contains
            if include and "subject_contains" in criteria:
                subject_filter = criteria["subject_contains"]
                if (
                    subject_filter
                    and subject_filter.lower() not in email.get("subject", "").lower()
                ):
                    include = False

            # Example: filter by minimum sentiment
            if include and "min_sentiment" in criteria:
                min_sentiment = criteria["min_sentiment"]
                email_sentiment = email.get("sentiment", "neutral")
                if min_sentiment == "positive" and email_sentiment != "positive":
                    include = False
                elif min_sentiment == "negative" and email_sentiment != "negative":
                    include = False

            if include:
                filtered_emails.append(email)

        stats = {
            "total_input": len(emails),
            "total_output": len(filtered_emails),
            "filtered_count": len(emails) - len(filtered_emails),
        }

        return {"filtered_emails": filtered_emails, "stats": stats}
