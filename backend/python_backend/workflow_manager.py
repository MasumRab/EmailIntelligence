"""
It will be removed in a future release.

Workflow Persistence System for Email Intelligence Platform

Implements a complete workflow persistence system allowing users to save
their node-based email processing workflows to JSON files and load them later.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Workflow:
    """Represents a node-based email processing workflow"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.version = "1.0"
        self.nodes: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, Any]] = []
        self.config: Dict[str, Any] = {}

    def add_node(self, node_type: str, node_id: str, x: float = 0, y: float = 0, **kwargs) -> None:
        """Add a node to the workflow"""
        node = {
            "id": node_id,
            "type": node_type,
            "position": {"x": x, "y": y},
            "parameters": kwargs,
        }
        self.nodes.append(node)
        self.updated_at = datetime.now().isoformat()

    def add_connection(
        self, source_node_id: str, source_output: str, target_node_id: str, target_input: str
    ) -> None:
        """Add a connection between nodes"""
        connection = {
            "source_node": source_node_id,
            "source_output": source_output,
            "target_node": target_node_id,
            "target_input": target_input,
        }
        self.connections.append(connection)
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "nodes": self.nodes,
            "connections": self.connections,
            "config": self.config,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        """Create workflow from dictionary"""
        workflow = cls(data["name"], data.get("description", ""))
        workflow.created_at = data.get("created_at", datetime.now().isoformat())
        workflow.updated_at = data.get("updated_at", datetime.now().isoformat())
        workflow.version = data.get("version", "1.0")
        workflow.nodes = data.get("nodes", [])
        workflow.connections = data.get("connections", [])
        workflow.config = data.get("config", {})
        return workflow


class WorkflowManager:
    """Manages saving, loading, and tracking workflows"""

    def __init__(self, workflows_dir: str = "workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows_dir.mkdir(exist_ok=True)
        self._workflow_history: Dict[str, List[str]] = {}  # workflow name to version history

    def save_workflow(self, workflow: Workflow, filename: Optional[str] = None) -> bool:
        """Save a workflow to a JSON file"""
        try:
            if filename is None:
                filename = f"{workflow.name.replace(' ', '_').lower()}_{int(datetime.now().timestamp())}.json"

            filepath = self.workflows_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(workflow.to_dict(), f, indent=2, ensure_ascii=False)

            logger.info(f"Workflow '{workflow.name}' saved to {filepath}")

            # Track history
            if workflow.name not in self._workflow_history:
                self._workflow_history[workflow.name] = []
            self._workflow_history[workflow.name].append(str(filepath))

            return True
        except Exception as e:
            logger.error(f"Failed to save workflow '{workflow.name}': {str(e)}")
            return False

    def load_workflow(self, filename: str) -> Optional[Workflow]:
        """Load a workflow from a JSON file"""
        try:
            filepath = self.workflows_dir / filename

            if not filepath.exists():
                logger.error(f"Workflow file does not exist: {filepath}")
                return None

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            workflow = Workflow.from_dict(data)
            logger.info(f"Workflow '{workflow.name}' loaded from {filepath}")
            return workflow
        except Exception as e:
            logger.error(f"Failed to load workflow from {filename}: {str(e)}")
            return None

    def list_workflows(self) -> List[str]:
        """List all available workflow files"""
        try:
            workflow_files = list(self.workflows_dir.glob("*.json"))
            return [f.name for f in workflow_files]
        except Exception as e:
            logger.error(f"Failed to list workflows: {str(e)}")
            return []

    def get_workflow_history(self, workflow_name: str) -> List[str]:
        """Get the history of saved versions for a workflow"""
        return self._workflow_history.get(workflow_name, [])


# Global workflow manager instance
workflow_manager = WorkflowManager()


def get_workflow_manager() -> WorkflowManager:
    """Get the global workflow manager instance"""
    import warnings

    warnings.warn(
        "get_workflow_manager from backend.python_backend.workflow_manager is deprecated. "
        "Use backend.node_engine.workflow_manager.workflow_manager instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return workflow_manager
