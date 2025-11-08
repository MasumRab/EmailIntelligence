"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Workflow Manager for the Email Intelligence Platform.

This module provides functionality for managing, storing, and retrieving
node-based workflows.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.node_engine.email_nodes import (
    ActionNode,
    AIAnalysisNode,
    EmailSourceNode,
    FilterNode,
    PreprocessingNode,
)
from backend.node_engine.node_base import Connection, Workflow


class WorkflowManager:
    """Manages storage and retrieval of workflows."""

    def __init__(self, workflows_dir: str = "data/workflows"):
        self.workflows_dir = workflows_dir
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

        # Create workflows directory if it doesn't exist
        os.makedirs(workflows_dir, exist_ok=True)

    def save_workflow(self, workflow: Workflow) -> str:
        """
        Save a workflow to a JSON file.

        Args:
            workflow: The workflow to save

        Returns:
            Path to the saved workflow file
        """
        workflow_data = self._workflow_to_dict(workflow)
        filename = f"{workflow.workflow_id}.json"
        raw_filepath = os.path.join(self.workflows_dir, filename)
        filepath = os.path.normpath(raw_filepath)
        # Validate that the workflow file resides within self.workflows_dir
        if not filepath.startswith(os.path.abspath(self.workflows_dir) + os.sep):
            raise ValueError("Invalid workflow_id resulting in unsafe file path")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(workflow_data, f, indent=2, default=str)

        self.logger.info(f"Workflow {workflow.name} saved to {filepath}")
        return filepath

    def load_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Load a workflow from a JSON file.

        Args:
            workflow_id: ID of the workflow to load

        Returns:
            The loaded workflow or None if not found
        """
        filename = f"{workflow_id}.json"
        raw_filepath = os.path.join(self.workflows_dir, filename)
        filepath = os.path.normpath(raw_filepath)
        if not filepath.startswith(os.path.abspath(self.workflows_dir) + os.sep):
            self.logger.warning(f"Attempted file access outside workflows_dir: {filepath}")
            return None

        if not os.path.exists(filepath):
            self.logger.warning(f"Workflow file not found: {filepath}")
            return None

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                workflow_data = json.load(f)

            workflow = self._dict_to_workflow(workflow_data)
            self.logger.info(f"Workflow {workflow.name} loaded from {filepath}")
            return workflow
        except Exception as e:
            self.logger.error(f"Error loading workflow {workflow_id}: {str(e)}")
            return None

    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        List all available workflows.

        Returns:
            List of workflow metadata
        """
        workflows = []

        for filename in os.listdir(self.workflows_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.workflows_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        workflow_data = json.load(f)

                    workflows.append(
                        {
                            "id": workflow_data.get("workflow_id"),
                            "name": workflow_data.get("name", "Unnamed"),
                            "description": workflow_data.get("description", ""),
                            "created_at": workflow_data.get("metadata", {}).get("created_at"),
                            "modified_at": workflow_data.get("metadata", {}).get("modified_at"),
                            "node_count": len(workflow_data.get("nodes", [])),
                            "connection_count": len(workflow_data.get("connections", [])),
                        }
                    )
                except Exception as e:
                    self.logger.error(f"Error reading workflow {filename}: {str(e)}")

        return workflows

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: ID of the workflow to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        filename = f"{workflow_id}.json"
        raw_filepath = os.path.join(self.workflows_dir, filename)
        filepath = os.path.normpath(raw_filepath)
        if not filepath.startswith(os.path.abspath(self.workflows_dir) + os.sep):
            self.logger.warning(f"Attempted deletion of file outside workflows_dir: {filepath}")
            return False

        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                self.logger.info(f"Workflow {workflow_id} deleted")
                return True
            except Exception as e:
                self.logger.error(f"Error deleting workflow {workflow_id}: {str(e)}")
                return False
        else:
            self.logger.warning(f"Workflow file not found for deletion: {filepath}")
            return False

    def _workflow_to_dict(self, workflow: Workflow) -> Dict[str, Any]:
        """Convert a Workflow object to a dictionary for serialization."""
        return {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "description": workflow.description,
            "nodes": [
                {
                    "node_id": node.node_id,
                    "type": node.__class__.__name__,
                    "name": node.name,
                    "description": node.description,
                    "config": getattr(node, "config", {}),
                }
                for node in workflow.nodes.values()
            ],
            "connections": [
                {
                    "source_node_id": conn.source_node_id,
                    "source_port": conn.source_port,
                    "target_node_id": conn.target_node_id,
                    "target_port": conn.target_port,
                }
                for conn in workflow.connections
            ],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "modified_at": datetime.now().isoformat(),
                "version": "1.0",
            },
        }

    def _dict_to_workflow(self, workflow_data: Dict[str, Any]) -> Workflow:
        """Convert a dictionary to a Workflow object."""
        workflow = Workflow(
            workflow_id=workflow_data["workflow_id"],
            name=workflow_data.get("name", "Unnamed"),
            description=workflow_data.get("description", ""),
        )

        # Create node instances from the data
        node_configs = {node_data["node_id"]: node_data for node_data in workflow_data["nodes"]}

        for node_data in workflow_data["nodes"]:
            node_id = node_data["node_id"]
            node_type = node_data["type"]
            node_config = node_data.get("config", {})

            # Create node instance based on type
            node = self._create_node_from_type(
                node_type, node_config, node_id, node_data.get("name")
            )
            workflow.add_node(node)

        # Create connections
        for conn_data in workflow_data["connections"]:
            connection = Connection(
                source_node_id=conn_data["source_node_id"],
                source_port=conn_data["source_port"],
                target_node_id=conn_data["target_node_id"],
                target_port=conn_data["target_port"],
            )
            workflow.add_connection(connection)

        return workflow

    def _create_node_from_type(
        self, node_type: str, config: Dict[str, Any], node_id: str, name: str = None
    ):
        """Create a node instance from its type string."""
        node_classes = {
            "EmailSourceNode": EmailSourceNode,
            "PreprocessingNode": PreprocessingNode,
            "AIAnalysisNode": AIAnalysisNode,
            "FilterNode": FilterNode,
            "ActionNode": ActionNode,
        }

        if node_type not in node_classes:
            raise ValueError(f"Unknown node type: {node_type}")

        node_class = node_classes[node_type]
        return node_class(config=config, node_id=node_id, name=name)

    def create_sample_workflow(self) -> Workflow:
        """
        Create a sample workflow for demonstration purposes.

        Returns:
            A sample workflow with common email processing nodes
        """
        workflow = Workflow(
            name="Email Processing Pipeline",
            description="A sample workflow that processes emails through multiple stages",
        )

        # Create nodes
        source_node = EmailSourceNode(name="Email Source", config={"provider": "gmail"})
        preprocessing_node = PreprocessingNode(name="Email Preprocessor")
        analysis_node = AIAnalysisNode(name="AI Analyzer")
        filter_node = FilterNode(
            name="Email Filter",
            config={
                "criteria": {
                    "required_keywords": ["important", "urgent"],
                    "excluded_senders": ["noreply@spam.com"],
                }
            },
        )
        action_node = ActionNode(name="Action Executor")

        # Add nodes to workflow
        workflow.add_node(source_node)
        workflow.add_node(preprocessing_node)
        workflow.add_node(analysis_node)
        workflow.add_node(filter_node)
        workflow.add_node(action_node)

        # Create connections
        workflow.add_connection(
            Connection(
                source_node_id=source_node.node_id,
                source_port="emails",
                target_node_id=preprocessing_node.node_id,
                target_port="emails",
            )
        )

        workflow.add_connection(
            Connection(
                source_node_id=preprocessing_node.node_id,
                source_port="processed_emails",
                target_node_id=analysis_node.node_id,
                target_port="emails",
            )
        )

        workflow.add_connection(
            Connection(
                source_node_id=analysis_node.node_id,
                source_port="analysis_results",
                target_node_id=filter_node.node_id,
                target_port="emails",
            )
        )

        workflow.add_connection(
            Connection(
                source_node_id=filter_node.node_id,
                source_port="filtered_emails",
                target_node_id=action_node.node_id,
                target_port="emails",
            )
        )

        # Also connect actions input separately (this is just for demo)
        # In a real workflow, actions would come from another source
        workflow.add_connection(
            Connection(
                source_node_id=analysis_node.node_id,
                source_port="summary",
                target_node_id=action_node.node_id,
                target_port="actions",
            )
        )

        return workflow


# Global workflow manager instance
workflow_manager = WorkflowManager()
