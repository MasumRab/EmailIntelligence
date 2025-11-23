"""
Base classes and types for the node-based workflow system.

This module defines the core abstractions for creating and managing workflow nodes,
including data types, ports, connections, and the base node class.
"""

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set
from enum import Enum


class DataType(Enum):
    """Enumeration of supported data types for node ports."""
    EMAIL_LIST = "email_list"
    EMAIL = "email"
    JSON = "json"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    FILE_PATH = "file_path"
    BINARY = "binary"


@dataclass
class NodePort:
    """Represents an input or output port on a node."""
    name: str
    data_type: DataType
    required: bool = True
    description: str = ""
    default_value: Any = None


@dataclass
class Connection:
    """Represents a connection between two node ports."""
    source_node_id: str
    source_port: str
    target_node_id: str
    target_port: str
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())


@dataclass
class ExecutionContext:
    """Context information for node execution."""
    workflow_id: str
    user_id: str
    execution_id: str
    variables: Dict[str, Any] = None
    security_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = {}
        if self.security_context is None:
            self.security_context = {}


class BaseNode(ABC):
    """
    Abstract base class for all workflow nodes.

    Nodes are the fundamental building blocks of workflows, processing data
    and performing specific operations on email data.
    """

    def __init__(self, node_id: Optional[str] = None, name: Optional[str] = None, description: str = ""):
        self.node_id = node_id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self.description = description
        self.input_ports: List[NodePort] = []
        self.output_ports: List[NodePort] = []
        self.inputs: Dict[str, Any] = {}
        self.outputs: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute the node's logic.

        Args:
            context: Execution context containing workflow and user information

        Returns:
            Dictionary of output data keyed by output port name

        Raises:
            NodeExecutionError: If execution fails
        """
        pass

    def validate_inputs(self) -> List[str]:
        """
        Validate that all required inputs are present and valid.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        for port in self.input_ports:
            if port.required and port.name not in self.inputs:
                if port.default_value is None:
                    errors.append(f"Required input '{port.name}' is missing")
                else:
                    self.inputs[port.name] = port.default_value

        return errors

    def validate_outputs(self) -> List[str]:
        """
        Validate that all required outputs are present.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        for port in self.output_ports:
            if port.required and port.name not in self.outputs:
                errors.append(f"Required output '{port.name}' is missing")

        return errors

    def get_input(self, port_name: str, default: Any = None) -> Any:
        """
        Get input data for a specific port.

        Args:
            port_name: Name of the input port
            default: Default value if port not found

        Returns:
            Input data or default value
        """
        return self.inputs.get(port_name, default)

    def set_output(self, port_name: str, data: Any) -> None:
        """
        Set output data for a specific port.

        Args:
            port_name: Name of the output port
            data: Output data
        """
        self.outputs[port_name] = data

    def reset(self) -> None:
        """
        Reset the node's state for reuse.
        """
        self.inputs = {}
        self.outputs = {}
        self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize node to dictionary for persistence.

        Returns:
            Dictionary representation of the node
        """
        return {
            'node_id': self.node_id,
            'name': self.name,
            'description': self.description,
            'type': self.__class__.__name__,
            'input_ports': [{'name': p.name, 'data_type': p.data_type.value, 'required': p.required}
                          for p in self.input_ports],
            'output_ports': [{'name': p.name, 'data_type': p.data_type.value, 'required': p.required}
                           for p in self.output_ports],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseNode':
        """
        Deserialize node from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            Node instance
        """
        node = cls(
            node_id=data.get('node_id'),
            name=data.get('name'),
            description=data.get('description', '')
        )
        node.metadata = data.get('metadata', {})
        return node


class Workflow:
    """
    Represents a complete workflow consisting of nodes and connections.
    """

    def __init__(self, workflow_id: Optional[str] = None, name: str = "", description: str = ""):
        self.workflow_id = workflow_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.nodes: Dict[str, BaseNode] = {}
        self.connections: List[Connection] = []
        self.metadata: Dict[str, Any] = {}

    def add_node(self, node: BaseNode) -> None:
        """
        Add a node to the workflow.

        Args:
            node: Node to add
        """
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str) -> None:
        """
        Remove a node from the workflow.

        Args:
            node_id: ID of node to remove
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            # Remove connections involving this node
            self.connections = [c for c in self.connections
                              if c.source_node_id != node_id and c.target_node_id != node_id]

    def add_connection(self, connection: Connection) -> None:
        """
        Add a connection between nodes.

        Args:
            connection: Connection to add

        Raises:
            ValueError: If connection is invalid
        """
        # Validate connection
        if connection.source_node_id not in self.nodes:
            raise ValueError(f"Source node {connection.source_node_id} not found")
        if connection.target_node_id not in self.nodes:
            raise ValueError(f"Target node {connection.target_node_id} not found")

        source_node = self.nodes[connection.source_node_id]
        target_node = self.nodes[connection.target_node_id]

        # Check if ports exist
        source_port = next((p for p in source_node.output_ports if p.name == connection.source_port), None)
        target_port = next((p for p in target_node.input_ports if p.name == connection.target_port), None)

        if not source_port:
            raise ValueError(f"Source port '{connection.source_port}' not found on node {connection.source_node_id}")
        if not target_port:
            raise ValueError(f"Target port '{connection.target_port}' not found on node {connection.target_node_id}")

        # Check data type compatibility
        if source_port.data_type != target_port.data_type:
            raise ValueError(f"Data type mismatch: {source_port.data_type} -> {target_port.data_type}")

        self.connections.append(connection)

    def validate(self) -> List[str]:
        """
        Validate the workflow structure.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check for cycles (simplified check)
        # In a real implementation, you'd use topological sort
        visited = set()
        for node in self.nodes.values():
            if self._has_cycle(node.node_id, visited, set()):
                errors.append("Workflow contains cycles")
                break

        # Check that all required inputs are connected
        for node in self.nodes.values():
            for port in node.input_ports:
                if port.required:
                    connected = any(c.target_node_id == node.node_id and c.target_port == port.name
                                  for c in self.connections)
                    if not connected and port.default_value is None:
                        errors.append(f"Required input '{port.name}' of node '{node.name}' is not connected")

        return errors

    def _has_cycle(self, node_id: str, visited: Set[str], rec_stack: Set[str]) -> bool:
        """
        Check for cycles using DFS.

        Args:
            node_id: Current node ID
            visited: Set of visited nodes
            rec_stack: Recursion stack

        Returns:
            True if cycle detected
        """
        visited.add(node_id)
        rec_stack.add(node_id)

        for conn in self.connections:
            if conn.source_node_id == node_id:
                neighbor = conn.target_node_id
                if neighbor not in visited:
                    if self._has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

        rec_stack.remove(node_id)
        return False

    def get_execution_order(self) -> List[str]:
        """
        Get the order in which nodes should be executed.

        Returns:
            List of node IDs in execution order

        Raises:
            ValueError: If workflow has cycles
        """
        if self.validate():
            raise ValueError("Cannot determine execution order for invalid workflow")

        # Simple topological sort
        result = []
        visited = set()
        temp_visited = set()

        def visit(node_id: str):
            if node_id in temp_visited:
                raise ValueError("Workflow contains cycles")
            if node_id in visited:
                return

            temp_visited.add(node_id)

            # Visit all dependencies first
            for conn in self.connections:
                if conn.target_node_id == node_id:
                    visit(conn.source_node_id)

            temp_visited.remove(node_id)
            visited.add(node_id)
            result.append(node_id)

        # Visit all nodes
        for node_id in self.nodes:
            if node_id not in visited:
                visit(node_id)

        return result

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize workflow to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            'workflow_id': self.workflow_id,
            'name': self.name,
            'description': self.description,
            'nodes': {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            'connections': [vars(c) for c in self.connections],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """
        Deserialize workflow from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            Workflow instance
        """
        workflow = cls(
            workflow_id=data.get('workflow_id'),
            name=data.get('name', ''),
            description=data.get('description', '')
        )
        workflow.metadata = data.get('metadata', {})

        # Note: Node deserialization would require a node registry
        # For now, just store the data
        workflow._serialized_nodes = data.get('nodes', {})
        workflow._serialized_connections = data.get('connections', [])

        return workflow


class NodeExecutionError(Exception):
    """
    Exception raised when a node execution fails.
    """

    def __init__(self, node_id: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.node_id = node_id
        self.details = details or {}