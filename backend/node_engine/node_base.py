"""
Base classes for the node-based workflow system.

This module defines the foundational classes for creating and managing
node-based workflows in the Email Intelligence Platform.
"""
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
import logging


class DataType(Enum):
    """Enum for supported data types in node connections."""
    EMAIL = "email"
    EMAIL_LIST = "email_list"
    TEXT = "text"
    JSON = "json"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
    OBJECT = "object"
    ANY = "any"  # For dynamic typing when specific type is not known


class NodePort:
    """Defines an input or output port for a node."""

    def __init__(
            self,
            name: str,
            data_type: DataType,
            required: bool = True,
            description: str = ""):
        self.name = name
        self.data_type = data_type
        self.required = required
        self.description = description

    def __repr__(self):
        return f"NodePort(name='{self.name}', data_type={self.data_type}, required={self.required})"


class Connection:
    """Represents a connection between two nodes."""

    def __init__(self, source_node_id: str, source_port: str,
                 target_node_id: str, target_port: str):
        self.source_node_id = source_node_id
        self.source_port = source_port
        self.target_node_id = target_node_id
        self.target_port = target_port

    def __repr__(self):
        return (f"Connection({self.source_node_id}.{self.source_port} -> "
                f"{self.target_node_id}.{self.target_port})")


class ExecutionContext:
    """Maintains execution context during workflow execution."""

    def __init__(self):
        self.node_outputs: Dict[str, Dict[str, Any]] = {}
        self.shared_state: Dict[str, Any] = {}
        self.execution_path: List[str] = []
        self.errors: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}

    def set_node_output(self, node_id: str, output: Dict[str, Any]):
        """Store the output of a node."""
        self.node_outputs[node_id] = output

    def get_node_output(self, node_id: str, port_name: str) -> Optional[Any]:
        """Get the output of a specific node's port."""
        node_output = self.node_outputs.get(node_id)
        if node_output:
            return node_output.get(port_name)
        return None

    def add_error(self, node_id: str, error: str, details: Dict[str, Any] = None):
        """Add an error to the execution context."""
        error_info = {
            "node_id": node_id,
            "error": error,
            "timestamp": str(self.metadata.get("start_time")),
            "details": details or {}
        }
        self.errors.append(error_info)


class BaseNode(ABC):
    """Abstract base class for all nodes in the workflow system."""

    def __init__(self, node_id: str = None, name: str = None, description: str = ""):
        self.node_id = node_id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self.description = description
        self.input_ports: List[NodePort] = []
        self.output_ports: List[NodePort] = []
        self.inputs: Dict[str, Any] = {}
        self.outputs: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._parent_workflow_id: Optional[str] = None

    @abstractmethod
    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute the node's primary function.

        Args:
            context: The execution context containing shared state and node outputs

        Returns:
            Dictionary containing the node's output values
        """
        pass

    def validate_inputs(self) -> Dict[str, List[str]]:
        """
        Validate that all required inputs are present and correct type.

        Returns:
            Dictionary with 'valid' flag and list of errors if any
        """
        errors = []

        # Check required inputs
        for port in self.input_ports:
            if port.required and port.name not in self.inputs:
                errors.append(f"Required input '{port.name}' is missing")

        # Type validation would go here if we implement it
        # For now, we rely on run-time type checking

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def set_input(self, port_name: str, value: Any):
        """Set an input value for the node."""
        self.inputs[port_name] = value

    def set_inputs(self, inputs: Dict[str, Any]):
        """Set multiple input values at once."""
        self.inputs.update(inputs)

    def get_node_info(self) -> Dict[str, Any]:
        """Get information about the node for UI display."""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__,
            "input_ports": [
                {
                    "name": port.name,
                    "type": port.data_type.value,
                    "required": port.required,
                    "description": port.description
                }
                for port in self.input_ports
            ],
            "output_ports": [
                {
                    "name": port.name,
                    "type": port.data_type.value,
                    "required": port.required,  # All outputs are required by definition
                    "description": port.description
                }
                for port in self.output_ports
            ]
        }

    def set_parent_workflow(self, workflow_id: str):
        """Set the parent workflow ID for this node."""
        self._parent_workflow_id = workflow_id

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.node_id})"


class Workflow:
    """Represents a complete workflow of connected nodes."""

    def __init__(self, workflow_id: str = None, name: str = "", description: str = ""):
        self.workflow_id = workflow_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.nodes: Dict[str, BaseNode] = {}
        self.connections: List[Connection] = []
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def add_node(self, node: BaseNode):
        """Add a node to the workflow."""
        node.set_parent_workflow(self.workflow_id)
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str):
        """Remove a node from the workflow."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            # Remove any connections to/from this node
            self.connections = [
                conn for conn in self.connections
                if conn.source_node_id != node_id and conn.target_node_id != node_id
            ]

    def add_connection(self, connection: Connection):
        """Add a connection between nodes."""
        # Validate that the nodes exist in the workflow
        if connection.source_node_id not in self.nodes:
            raise ValueError(f"Source node {connection.source_node_id} does not exist in workflow")
        if connection.target_node_id not in self.nodes:
            raise ValueError(f"Target node {connection.target_node_id} does not exist in workflow")

        # Validate the ports exist on the respective nodes
        source_node = self.nodes[connection.source_node_id]
        target_node = self.nodes[connection.target_node_id]

        source_port_exists = any(p.name == connection.source_port for p in source_node.output_ports)
        if not source_port_exists:
            raise ValueError(
                f"Source port {
                    connection.source_port} does not exist on node {
                    connection.source_node_id}")

        target_port_exists = any(p.name == connection.target_port for p in target_node.input_ports)
        if not target_port_exists:
            raise ValueError(
                f"Target port {
                    connection.target_port} does not exist on node {
                    connection.target_node_id}")

        self.connections.append(connection)

    def get_connections_for_node(self, node_id: str) -> List[Connection]:
        """Get all connections involving a specific node."""
        return [
            conn for conn in self.connections
            if conn.source_node_id == node_id or conn.target_node_id == node_id
        ]

    def get_upstream_nodes(self, node_id: str) -> List[str]:
        """Get all nodes that provide input to the specified node."""
        upstream = []
        for conn in self.connections:
            if conn.target_node_id == node_id:
                upstream.append(conn.source_node_id)
        return upstream

    def get_downstream_nodes(self, node_id: str) -> List[str]:
        """Get all nodes that receive input from the specified node."""
        downstream = []
        for conn in self.connections:
            if conn.source_node_id == node_id:
                downstream.append(conn.target_node_id)
        return downstream

    def get_execution_order(self) -> List[str]:
        """Calculate the execution order of nodes using topological sort."""
        # Build adjacency list of dependencies
        dependencies = {node_id: [] for node_id in self.nodes.keys()}

        for conn in self.connections:
            dependencies[conn.target_node_id].append(conn.source_node_id)

        # Topological sort using DFS
        result = []
        visited = set()
        temp_visited = set()

        def visit(node_id):
            if node_id in temp_visited:
                raise ValueError("Workflow has circular dependencies")
            if node_id not in visited:
                temp_visited.add(node_id)
                for dep in dependencies[node_id]:
                    visit(dep)
                temp_visited.remove(node_id)
                visited.add(node_id)
                result.append(node_id)

        for node_id in self.nodes.keys():
            if node_id not in visited:
                visit(node_id)

        return result

    def __repr__(self):
        return f"Workflow(name={self.name}, nodes={len(self.nodes)
                                                   }, connections={len(self.connections)})"
