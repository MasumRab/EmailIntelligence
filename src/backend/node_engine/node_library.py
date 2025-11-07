"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Node Library for the Email Intelligence Platform.

This module provides a library of available nodes that can be consumed
by the Gradio UI to allow users to build node-based workflows.
"""

from typing import Any, Dict, List

from src.backend.node_engine.email_nodes import (
    ActionNode,
    AIAnalysisNode,
    EmailSourceNode,
    FilterNode,
    PreprocessingNode,
)
from src.backend.node_engine.node_base import DataType, NodePort


class NodeLibrary:
    """Library of available nodes for the workflow builder UI."""

    def __init__(self):
        self._nodes = {}
        self._register_default_nodes()

    def _register_default_nodes(self):
        """Register the default email processing nodes."""
        # Register EmailSourceNode
        self._nodes["EmailSourceNode"] = {
            "class": EmailSourceNode,
            "name": "Email Source",
            "category": "Input",
            "description": "Sources emails from various providers (Gmail, etc.)",
            "input_ports": [],
            "output_ports": [
                {
                    "name": "emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of retrieved emails",
                },
                {
                    "name": "status",
                    "type": "JSON",
                    "required": True,
                    "description": "Status information about the operation",
                },
            ],
        }

        # Register PreprocessingNode
        self._nodes["PreprocessingNode"] = {
            "class": PreprocessingNode,
            "name": "Email Preprocessor",
            "category": "Processing",
            "description": "Preprocesses email data (cleaning, normalization, etc.)",
            "input_ports": [
                {
                    "name": "emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of emails to preprocess",
                }
            ],
            "output_ports": [
                {
                    "name": "processed_emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of preprocessed emails",
                },
                {
                    "name": "stats",
                    "type": "JSON",
                    "required": True,
                    "description": "Statistics about preprocessing",
                },
            ],
        }

        # Register AIAnalysisNode
        self._nodes["AIAnalysisNode"] = {
            "class": AIAnalysisNode,
            "name": "AI Analyzer",
            "category": "AI/ML",
            "description": "Performs AI analysis on emails (sentiment, topic, intent, etc.)",
            "input_ports": [
                {
                    "name": "emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of emails to analyze",
                }
            ],
            "output_ports": [
                {
                    "name": "analysis_results",
                    "type": "JSON",
                    "required": True,
                    "description": "AI analysis results for each email",
                },
                {
                    "name": "summary",
                    "type": "JSON",
                    "required": True,
                    "description": "Summary of the analysis",
                },
            ],
        }

        # Register FilterNode
        self._nodes["FilterNode"] = {
            "class": FilterNode,
            "name": "Email Filter",
            "category": "Processing",
            "description": "Filters emails based on criteria",
            "input_ports": [
                {
                    "name": "emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of emails to filter",
                },
                {
                    "name": "criteria",
                    "type": "JSON",
                    "required": False,
                    "description": "Filtering criteria (optional override)",
                },
            ],
            "output_ports": [
                {
                    "name": "filtered_emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "Filtered email list",
                },
                {
                    "name": "discarded_emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "Emails that didn't match criteria",
                },
                {
                    "name": "stats",
                    "type": "JSON",
                    "required": True,
                    "description": "Filtering statistics",
                },
            ],
        }

        # Register ActionNode
        self._nodes["ActionNode"] = {
            "class": ActionNode,
            "name": "Action Executor",
            "category": "Output",
            "description": "Executes actions on emails (move, label, forward, etc.)",
            "input_ports": [
                {
                    "name": "emails",
                    "type": "EMAIL_LIST",
                    "required": True,
                    "description": "List of emails to act upon",
                },
                {
                    "name": "actions",
                    "type": "JSON",
                    "required": True,
                    "description": "Actions to perform on emails",
                },
            ],
            "output_ports": [
                {
                    "name": "results",
                    "type": "JSON",
                    "required": True,
                    "description": "Results of the actions performed",
                },
                {
                    "name": "status",
                    "type": "JSON",
                    "required": True,
                    "description": "Status of action execution",
                },
            ],
        }

    def get_node_types(self) -> List[str]:
        """Get a list of all available node types."""
        return list(self._nodes.keys())

    def get_node_info(self, node_type: str) -> Dict[str, Any]:
        """Get detailed information about a specific node type."""
        if node_type not in self._nodes:
            raise ValueError(f"Node type '{node_type}' not found")

        return self._nodes[node_type]

    def get_nodes_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all nodes grouped by category."""
        categories = {}
        for node_type, node_info in self._nodes.items():
            category = node_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(
                {
                    "type": node_type,
                    "name": node_info["name"],
                    "description": node_info["description"],
                }
            )

        return categories

    def get_all_node_info(self) -> List[Dict[str, Any]]:
        """Get information about all available nodes."""
        result = []
        for node_type, node_info in self._nodes.items():
            result.append(
                {
                    "type": node_type,
                    "name": node_info["name"],
                    "description": node_info["description"],
                    "category": node_info["category"],
                    "input_ports": node_info["input_ports"],
                    "output_ports": node_info["output_ports"],
                }
            )

        return result

    def create_node(
        self, node_type: str, config: Dict[str, Any] = None, node_id: str = None, name: str = None
    ):
        """Create an instance of a node."""
        if node_type not in self._nodes:
            raise ValueError(f"Node type '{node_type}' not found")

        node_class = self._nodes[node_type]["class"]
        return node_class(config=config, node_id=node_id, name=name)


# Global node library instance
node_library = NodeLibrary()


# Convenience functions for UI consumption
def get_available_node_types() -> List[str]:
    """Get a list of all available node types."""
    return node_library.get_node_types()


def get_node_info(node_type: str) -> Dict[str, Any]:
    """Get detailed information about a specific node type."""
    return node_library.get_node_info(node_type)


def get_nodes_by_category() -> Dict[str, List[Dict[str, Any]]]:
    """Get all nodes grouped by category."""
    return node_library.get_nodes_by_category()


def get_all_node_info() -> List[Dict[str, Any]]:
    """Get information about all available nodes."""
    return node_library.get_all_node_info()
