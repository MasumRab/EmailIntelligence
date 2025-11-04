"""
Workflow execution engine for the node-based system.

This module provides the core workflow execution functionality,
including node registration, workflow validation, and secure execution.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Type
from datetime import datetime
import uuid

from .node_base import BaseNode, Workflow, ExecutionContext, NodeExecutionError
from .security_manager import SecurityManager

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Central engine for managing and executing workflows.

    Provides node registration, workflow validation, and execution orchestration
    with integrated security controls.
    """

    def __init__(self):
        self.node_types: Dict[str, Type[BaseNode]] = {}
        self.security_manager = SecurityManager()
        self.active_executions: Dict[str, asyncio.Task] = {}

        # Register built-in node types
        self._register_builtin_nodes()

    def _register_builtin_nodes(self) -> None:
        """
        Register built-in node types.
        """
        from .email_nodes import EmailSourceNode, PreprocessingNode, AIAnalysisNode, FilterNode, ActionNode

        self.register_node_type(EmailSourceNode)
        self.register_node_type(PreprocessingNode)
        self.register_node_type(AIAnalysisNode)
        self.register_node_type(FilterNode)
        self.register_node_type(ActionNode)

    def register_node_type(self, node_class: Type[BaseNode]) -> None:
        """
        Register a node type for use in workflows.

        Args:
            node_class: Node class to register
        """
        type_name = node_class.__name__
        self.node_types[type_name] = node_class
        logger.info(f"Registered node type: {type_name}")

    def get_registered_node_types(self) -> List[str]:
        """
        Get list of registered node type names.

        Returns:
            List of node type names
        """
        return list(self.node_types.keys())

    def create_node(self, node_type: str, config: Optional[Dict[str, Any]] = None, **kwargs) -> BaseNode:
        """
        Create a node instance.

        Args:
            node_type: Type name of node to create
            config: Node configuration
            **kwargs: Additional node parameters

        Returns:
            Node instance

        Raises:
            ValueError: If node type is not registered
        """
        if node_type not in self.node_types:
            raise ValueError(f"Unknown node type: {node_type}")

        node_class = self.node_types[node_type]
        return node_class(config=config, **kwargs)

    async def execute_workflow(self, workflow: Workflow, user_id: str, execution_id: Optional[str] = None) -> ExecutionContext:
        """
        Execute a workflow with security controls.

        Args:
            workflow: Workflow to execute
            user_id: ID of user executing the workflow
            execution_id: Optional execution ID (generated if not provided)

        Returns:
            Execution context with results

        Raises:
            ValueError: If workflow is invalid
            RuntimeError: If execution fails
        """
        execution_id = execution_id or str(uuid.uuid4())

        context = ExecutionContext(
            workflow_id=workflow.workflow_id,
            user_id=user_id,
            execution_id=execution_id
        )

        logger.info(f"Starting workflow execution: {workflow.workflow_id} by user {user_id}")

        try:
            # Validate workflow
            validation_errors = workflow.validate()
            if validation_errors:
                raise ValueError(f"Workflow validation failed: {validation_errors}")

            # Get execution order
            execution_order = workflow.get_execution_order()

            # Execute nodes in order
            for node_id in execution_order:
                node = workflow.nodes[node_id]

                # Execute node with security controls
                result = await self.security_manager.execute_node_securely(node, context)

                # Store results in context for dependent nodes
                context.variables[f"node_{node_id}_output"] = result

                # Propagate outputs to connected nodes
                await self._propagate_outputs(workflow, node_id, result, context)

            logger.info(f"Workflow execution completed: {workflow.workflow_id}")

        except Exception as e:
            logger.error(f"Workflow execution failed: {workflow.workflow_id}, error: {str(e)}")
            context.variables["execution_error"] = str(e)
            raise RuntimeError(f"Workflow execution failed: {str(e)}")

        return context

    async def _propagate_outputs(self, workflow: Workflow, source_node_id: str, outputs: Dict[str, Any], context: ExecutionContext) -> None:
        """
        Propagate node outputs to connected input nodes.

        Args:
            workflow: Workflow instance
            source_node_id: ID of node that produced outputs
            outputs: Node output data
            context: Execution context
        """
        for connection in workflow.connections:
            if connection.source_node_id == source_node_id:
                target_node = workflow.nodes[connection.target_node_id]
                port_name = connection.target_port

                # Get output data for this port
                output_data = outputs.get(port_name)
                if output_data is not None:
                    target_node.inputs[port_name] = output_data

                    # If using signed tokens, create and store token
                    if hasattr(self.security_manager, 'token_manager'):
                        token = self.security_manager.token_manager.create_node_data_token(
                            source_node_id, connection.target_node_id, output_data
                        )
                        # Store token in context for verification
                        context.variables[f"token_{connection.id}"] = token

    async def cancel_execution(self, execution_id: str) -> bool:
        """
        Cancel a running workflow execution.

        Args:
            execution_id: Execution ID to cancel

        Returns:
            True if execution was cancelled
        """
        if execution_id in self.active_executions:
            task = self.active_executions[execution_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_executions[execution_id]
            logger.info(f"Cancelled workflow execution: {execution_id}")
            return True

        return False

    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a workflow execution.

        Args:
            execution_id: Execution ID

        Returns:
            Status information or None if not found
        """
        if execution_id in self.active_executions:
            task = self.active_executions[execution_id]
            return {
                "execution_id": execution_id,
                "status": "running" if not task.done() else "completed",
                "done": task.done()
            }

        return None

    async def execute_workflow_async(self, workflow: Workflow, user_id: str) -> str:
        """
        Execute a workflow asynchronously.

        Args:
            workflow: Workflow to execute
            user_id: User executing the workflow

        Returns:
            Execution ID for tracking
        """
        execution_id = str(uuid.uuid4())

        task = asyncio.create_task(self._execute_workflow_task(workflow, user_id, execution_id))
        self.active_executions[execution_id] = task

        # Clean up completed tasks
        self.active_executions = {eid: t for eid, t in self.active_executions.items() if not t.done()}

        return execution_id

    async def _execute_workflow_task(self, workflow: Workflow, user_id: str, execution_id: str) -> None:
        """
        Task wrapper for async workflow execution.

        Args:
            workflow: Workflow to execute
            user_id: User executing workflow
            execution_id: Execution identifier
        """
        try:
            await self.execute_workflow(workflow, user_id, execution_id)
        except Exception as e:
            logger.error(f"Async workflow execution failed: {execution_id}, error: {str(e)}")
        finally:
            # Clean up
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]


# Global workflow engine instance
workflow_engine = WorkflowEngine()


class WorkflowManager:
    """
    Manager for workflow persistence and management.
    """

    def __init__(self, storage_path: str = "./workflows"):
        self.storage_path = storage_path
        self.workflows: Dict[str, Workflow] = {}

    def save_workflow(self, workflow: Workflow) -> str:
        """
        Save workflow to storage.

        Args:
            workflow: Workflow to save

        Returns:
            File path where workflow was saved
        """
        import os
        import json

        os.makedirs(self.storage_path, exist_ok=True)

        file_path = os.path.join(self.storage_path, f"{workflow.workflow_id}.json")

        with open(file_path, 'w') as f:
            json.dump(workflow.to_dict(), f, indent=2)

        self.workflows[workflow.workflow_id] = workflow
        logger.info(f"Saved workflow: {workflow.workflow_id} to {file_path}")

        return file_path

    def load_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Load workflow from storage.

        Args:
            workflow_id: Workflow ID to load

        Returns:
            Workflow instance or None if not found
        """
        import os
        import json

        if workflow_id in self.workflows:
            return self.workflows[workflow_id]

        file_path = os.path.join(self.storage_path, f"{workflow_id}.json")

        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            workflow = Workflow.from_dict(data)
            self.workflows[workflow_id] = workflow

            logger.info(f"Loaded workflow: {workflow_id} from {file_path}")
            return workflow

        except Exception as e:
            logger.error(f"Failed to load workflow {workflow_id}: {str(e)}")
            return None

    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        List all saved workflows.

        Returns:
            List of workflow metadata
        """
        import os
        import json

        workflows = []

        if os.path.exists(self.storage_path):
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    workflow_id = filename[:-5]  # Remove .json
                    workflow = self.load_workflow(workflow_id)
                    if workflow:
                        workflows.append({
                            "workflow_id": workflow.workflow_id,
                            "name": workflow.name,
                            "description": workflow.description,
                            "node_count": len(workflow.nodes),
                            "connection_count": len(workflow.connections)
                        })

        return workflows

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: Workflow ID to delete

        Returns:
            True if deleted successfully
        """
        import os

        file_path = os.path.join(self.storage_path, f"{workflow_id}.json")

        if os.path.exists(file_path):
            os.remove(file_path)
            self.workflows.pop(workflow_id, None)
            logger.info(f"Deleted workflow: {workflow_id}")
            return True

        return False


# Global workflow manager instance
workflow_manager = WorkflowManager()