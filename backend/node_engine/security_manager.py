"""
Security manager for the node-based workflow system.

This module implements security controls for node execution in the Email Intelligence Platform.
"""

import logging
from typing import Any, Dict

from .node_base import BaseNode, ExecutionContext

logger = logging.getLogger(__name__)


class NodeExecutionError(Exception):
    """Exception raised for errors during node execution."""

    def __init__(self, message: str, node_id: str = None):
        super().__init__(message)
        self.node_id = node_id
        self.message = message


class SecurityManager:
    """
    Security manager for node-based workflow execution.

    Provides security controls for node execution, input validation,
    and secure data handling.
    """

    def __init__(self):
        self.security_enabled = True

    def validate_node_input(self, node: BaseNode, context: ExecutionContext) -> bool:
        """
        Validate node input against security policies.

        Args:
            node: Node to validate input for
            context: Execution context containing input data

        Returns:
            True if input is valid and secure
        """
        # In a real implementation, this would validate inputs against security policies
        # For now, we'll just return True to allow normal execution
        return True

    def validate_node_output(self, node: BaseNode, output: Dict[str, Any]) -> bool:
        """
        Validate node output against security policies.

        Args:
            node: Node that produced output
            output: Output data to validate

        Returns:
            True if output is valid and secure
        """
        # In a real implementation, this would validate outputs against security policies
        # For now, we'll just return True
        return True

    async def execute_node_securely(self, node: BaseNode, context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute a node with security controls.

        Args:
            node: Node to execute
            context: Execution context

        Returns:
            Node execution result

        Raises:
            NodeExecutionError: If security validation fails or execution encounters an error
        """
        try:
            # Validate inputs before execution
            if not self.validate_node_input(node, context):
                raise NodeExecutionError(f"Security validation failed for inputs on node {node.node_id}")

            # Execute the node
            output = await node.execute(context)

            # Validate outputs after execution
            if not self.validate_node_output(node, output):
                raise NodeExecutionError(f"Security validation failed for outputs on node {node.node_id}")

            return output

        except NodeExecutionError:
            # Re-raise security-related errors directly
            raise
        except Exception as e:
            # Wrap other exceptions in NodeExecutionError
            logger.error(f"Error executing node {node.node_id}: {str(e)}")
            raise NodeExecutionError(f"Node execution failed: {str(e)}", node_id=node.node_id)