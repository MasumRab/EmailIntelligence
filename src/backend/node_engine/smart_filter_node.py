"""
Smart Filter Node for the Email Intelligence Platform.

This module provides a node that integrates with the smart filtering system
to apply intelligent email filtering within node-based workflows.
"""

from typing import Any, Dict, List

from src.backend.node_engine.node_base import BaseNode, DataType, ExecutionContext, NodePort
from src.backend.python_nlp.smart_filters import SmartFilterManager


class SmartFilterNode(BaseNode):
    """
    A node that applies smart filtering to emails using the SmartFilterManager.
    
    This node takes a list of emails and applies intelligent filtering based on
    learned patterns and user preferences.
    """

    def __init__(self, node_id: str = None, name: str = None, description: str = ""):
        super().__init__(
            node_id,
            name or "Smart Filter Node",
            description or "Applies intelligent filtering to emails using learned patterns",
        )

        # Define input ports
        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, True, "List of emails to filter"),
            NodePort(
                "filter_criteria",
                DataType.JSON,
                False,
                "Optional filter criteria to customize filtering behavior",
            ),
        ]

        # Define output ports
        self.output_ports = [
            NodePort("filtered_emails", DataType.EMAIL_LIST, True, "Filtered emails"),
            NodePort("filter_stats", DataType.JSON, True, "Statistics about the filtering process"),
            NodePort("matched_filters", DataType.JSON, True, "Filters that matched the emails"),
        ]

        # Initialize the smart filter manager
        self.filter_manager = SmartFilterManager()

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Executes the smart filtering operation.

        Args:
            context: The execution context containing input values

        Returns:
            Dictionary containing filtered emails and filtering statistics
        """
        # Get input values
        emails = context.get_input("emails")
        filter_criteria = context.get_input("filter_criteria", {})

        # Apply smart filtering
        filtered_results = self._apply_smart_filters(emails, filter_criteria)

        # Prepare output
        output = {
            "filtered_emails": filtered_results["filtered_emails"],
            "filter_stats": filtered_results["stats"],
            "matched_filters": filtered_results["matched_filters"],
        }

        return output

    def _apply_smart_filters(self, emails: List[Dict[str, Any]], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies smart filtering to the provided emails.

        Args:
            emails: List of email dictionaries to filter
            criteria: Optional criteria to customize filtering

        Returns:
            Dictionary containing filtered emails and statistics
        """
        # Use the smart filter manager to apply filters
        filtered_emails = []
        matched_filters = []
        stats = {"total_emails": len(emails), "filtered_emails": 0, "matched_filters_count": 0}

        for email in emails:
            # Apply filters to the email
            filter_result = self.filter_manager.apply_filters_to_email_data(email)
            
            # If the email matches any filters, add it to the filtered list
            if filter_result["filters_matched"]:
                filtered_emails.append(email)
                matched_filters.extend(filter_result["filters_matched"])
        
        stats["filtered_emails"] = len(filtered_emails)
        stats["matched_filters_count"] = len(set(matched_filters))  # Count unique matched filters

        return {
            "filtered_emails": filtered_emails,
            "stats": stats,
            "matched_filters": list(set(matched_filters))  # Unique matched filters
        }


# Register the node type in the node library
def register_node_type(node_library):
    """
    Registers the SmartFilterNode with the provided node library.

    Args:
        node_library: The NodeLibrary instance to register the node with
    """
    node_library.register_node_type(
        "SmartFilterNode",
        {
            "class": SmartFilterNode,
            "name": "Smart Filter",
            "category": "Filtering",
            "description": "Applies intelligent filtering to emails using learned patterns",
            "input_ports": [
                {
                    "name": "emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of emails to filter",
                },
                {
                    "name": "filter_criteria",
                    "type": "JSON",
                    "required": False,
                    "description": "Optional filter criteria to customize filtering behavior",
                },
            ],
            "output_ports": [
                {
                    "name": "filtered_emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "Filtered emails",
                },
                {
                    "name": "filter_stats",
                    "type": "JSON",
                    "required": True,
                    "description": "Statistics about the filtering process",
                },
                {
                    "name": "matched_filters",
                    "type": True,
                    "description": "Filters that matched the emails",
                },
            ],
        }
    )