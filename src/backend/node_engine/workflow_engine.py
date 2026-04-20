"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Workflow Execution Engine for the Email Intelligence Platform.

This module manages the execution of node-based workflows, handling
dependencies, execution order, and error management.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.node_engine.node_base import (
    BaseNode,
    Connection,
    DataType,
    ExecutionContext,
    SecurityContext,
    Workflow,
)
from backend.node_engine.security_manager import (
    ExecutionSandbox,
    InputSanitizer,
    ResourceLimits,
    SecurityManager,
    audit_logger,
    resource_manager,
)


class WorkflowExecutionException(Exception):
    """Exception raised when workflow execution fails."""

    pass


class WorkflowEngine:
    """Manages execution of node-based workflows."""

    def __init__(self, security_manager: Optional[SecurityManager] = None):
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.active_executions: Dict[str, ExecutionContext] = {}
        self.node_registry: Dict[str, type] = {}
        # Initialize with a default SecurityManager if not provided, for flexibility
        self.security_manager = (
            security_manager if security_manager else SecurityManager(user_roles={})
        )

    def register_node_type(self, node_class: type):
        """Register a node type for workflow composition."""
        self.node_registry[node_class.__name__] = node_class
        self.logger.info(f"Registered node type: {node_class.__name__}")

    def get_registered_node_types(self) -> List[str]:
        """Get list of all registered node types."""
        return list(self.node_registry.keys())

    async def execute_workflow(
        self, workflow: Workflow, initial_inputs: Dict[str, Any] = None, user_id: str = None
    ) -> ExecutionContext:
        """
        Execute a workflow with the given initial inputs.

        Args:
            workflow: The workflow to execute
            initial_inputs: Initial input values for the workflow
            user_id: ID of the user requesting execution (for security/auditing)

        Returns:
            ExecutionContext containing the results and metadata
        """
        execution_id = workflow.workflow_id
        self.logger.info(f"Starting execution of workflow: {workflow.name} (ID: {execution_id})")

        # --- SECURITY CHECK: VERIFY USER PERMISSION TO EXECUTE WORKFLOW ---
        class MockUser:
            def __init__(self, user_id: str):
                self.id = user_id

        mock_user = (
            MockUser(user_id) if user_id else MockUser("anonymous")
        )  # Use 'anonymous' for unauthenticated

        if not self.security_manager.has_permission(mock_user, "execute", workflow):
            error_msg = f"User {user_id or 'anonymous'} does not have permission to execute workflow {workflow.name} (ID: {workflow.workflow_id})."
            self.logger.warning(error_msg)
            audit_logger.log_security_event(
                "WORKFLOW_EXECUTION_DENIED",
                {
                    "workflow_id": workflow.workflow_id,
                    "user_id": user_id,
                    "reason": "Insufficient permissions",
                },
            )
            raise WorkflowExecutionException(error_msg)
        # --- END SECURITY CHECK ---

        # Create security context
        security_context = SecurityContext(user_id=user_id)
        security_context.execution_start_time = datetime.now()

        # Audit log workflow start
        audit_logger.log_workflow_start(execution_id, workflow.name, user_id)

        # Sanitize initial inputs
        if initial_inputs:
            initial_inputs = InputSanitizer._sanitize_dict(initial_inputs or {})

        # Acquire resources for the workflow
        resources_acquired = await resource_manager.acquire_resources(
            execution_id, ResourceLimits()
        )
        if not resources_acquired:
            raise WorkflowExecutionException(
                f"Unable to acquire resources for workflow {execution_id}"
            )

        # Create execution context
        context = ExecutionContext()
        context.metadata["workflow_id"] = workflow.workflow_id
        context.metadata["workflow_name"] = workflow.name
        context.metadata["start_time"] = datetime.now()
        context.metadata["initial_inputs"] = initial_inputs or {}
        context.metadata["user_id"] = user_id
        context.metadata["performance"] = {
            "node_execution_times": {},
            "total_execution_time": 0,
            "nodes_executed": 0,
            "errors_count": 0,
        }

        # Store active execution
        self.active_executions[execution_id] = context

        try:
            # Set initial inputs to appropriate source nodes
            if initial_inputs:
                await self._set_initial_inputs(workflow, context, initial_inputs)

            # Get execution order
            execution_order = workflow.get_execution_order()
            self.logger.debug(f"Execution order: {execution_order}")

            # Execute nodes in order
            sandbox = ExecutionSandbox(self.security_manager)
            for node_id in execution_order:
                node = workflow.nodes[node_id]

                # Validate node execution based on security policies
                node_type = node.__class__.__name__
                if not self.security_manager.validate_node_execution(
                    node_type, getattr(node, "config", {})
                ):
                    error_msg = f"Security validation failed for node {node_id} ({node_type})"
                    context.add_error(node_id, error_msg)
                    audit_logger.log_security_event(
                        "NODE_EXECUTION_BLOCKED",
                        {
                            "node_id": node_id,
                            "node_type": node_type,
                            "workflow_id": workflow.workflow_id,
                        },
                    )
                    raise WorkflowExecutionException(error_msg)

                # Set inputs from connected nodes
                await self._set_node_inputs(node, workflow, context)

                # Validate inputs
                validation_result = node.validate_inputs()
                if not validation_result["valid"]:
                    error_msg = f"Node {node_id} input validation failed: {', '.join(validation_result['errors'])}"
                    context.add_error(node_id, error_msg)
                    raise WorkflowExecutionException(error_msg)

                # Execute the node with security sandbox
                self.logger.debug(f"Executing node {node_id} ({node.name})")
                try:
                    # Check API call limits
                    if not self.security_manager.check_api_call_limit(
                        workflow.workflow_id, node_id
                    ):
                        raise WorkflowExecutionException(
                            f"API call limit exceeded for node {node_id}"
                        )

                    start_time = datetime.now()
                    result = await sandbox.execute_with_timeout(
                        node.execute, 30, context  # 30 second timeout per node
                    )
                    execution_duration = (datetime.now() - start_time).total_seconds()

                    context.set_node_output(node_id, result)
                    context.execution_path.append(node_id)
                    self.logger.debug(f"Node {node_id} executed successfully")

                    # Update performance metrics
                    context.metadata["performance"]["node_execution_times"][
                        node_id
                    ] = execution_duration
                    context.metadata["performance"]["nodes_executed"] += 1

                    self.logger.debug(
                        f"Node {node_id} executed successfully in {execution_duration:.3f}s"
                    )

                    # Log node execution with enhanced performance data
                    audit_logger.log_node_execution(
                        workflow.workflow_id, node_id, node.name, "success", execution_duration
                    )
                except Exception as e:
                    error_msg = f"Node {node_id} execution failed: {str(e)}"
                    context.add_error(
                        node_id, error_msg, {"exception": str(e), "type": type(e).__name__}
                    )
                    self.logger.error(error_msg, exc_info=True)

                    # Log failed node execution
                    audit_logger.log_node_execution(
                        workflow.workflow_id, node_id, node.name, "failed", -1  # Indicate error
                    )

                    raise WorkflowExecutionException(error_msg) from e

            # Set completion metadata
            context.metadata["end_time"] = datetime.now()
            context.metadata["execution_duration"] = (
                context.metadata["end_time"] - context.metadata["start_time"]
            ).total_seconds()
            context.metadata["status"] = "completed"

            # Calculate total execution time
            total_execution_time = (
                context.metadata["end_time"] - context.metadata["start_time"]
            ).total_seconds()
            
            self.logger.info(
                f"Workflow {workflow.name} completed successfully in "
                f"{total_execution_time:.3f}s ({context.metadata['performance']['nodes_executed']} nodes)"
            )

        except Exception as e:
            # Set failure metadata
            end_time = datetime.now()
            context.metadata["end_time"] = end_time
            if "start_time" in context.metadata:
                context.metadata["execution_duration"] = (
                    end_time - context.metadata["start_time"]
                ).total_seconds()
            context.metadata["status"] = "failed"
            context.metadata["error"] = str(e)

            self.logger.error(f"Workflow {workflow.name} execution failed: {str(e)}", exc_info=True)

            # Re-raise the exception to indicate failure
            raise
        finally:
            # Clean up active execution
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]

            # Release resources
            resource_manager.release_resources(execution_id)

            # Audit log workflow end
            status = context.metadata.get("status", "unknown")
            duration = context.metadata.get("execution_duration", -1)
            audit_logger.log_workflow_end(execution_id, status, duration, user_id)

        return context

    async def _set_initial_inputs(
        self, workflow: Workflow, context: ExecutionContext, initial_inputs: Dict[str, Any]
    ):
        """Set initial input values to appropriate source nodes."""
        # For now, set all initial inputs as shared state
        # In the future, we might want to map initial inputs to specific nodes based on metadata
        context.shared_state.update(initial_inputs)

    async def _set_node_inputs(self, node: BaseNode, workflow: Workflow, context: ExecutionContext):
        """Set input values for a node based on connected node outputs with type validation."""
        connections = workflow.get_connections_for_node(node.node_id)

        # Find connections where this node is the target
        input_connections = [conn for conn in connections if conn.target_node_id == node.node_id]

        # Set inputs based on connected outputs with type validation
        for conn in input_connections:
            source_output = context.get_node_output(conn.source_node_id, conn.source_port)
            if source_output is not None:
                # Validate type compatibility between source output and target input
                target_port = next(
                    (p for p in node.input_ports if p.name == conn.target_port), None
                )
                if target_port:
                    # Get the source node to check output port type
                    source_node = workflow.nodes.get(conn.source_node_id)
                    if source_node:
                        source_port = next(
                            (p for p in source_node.output_ports if p.name == conn.source_port),
                            None,
                        )
                        if source_port:
                            # Validate type compatibility
                            if not self._validate_type_compatibility(
                                source_port.data_type, target_port.data_type
                            ):
                                error_msg = (
                                    f"Type mismatch in connection: {source_node.__class__.__name__}."
                                    f"{conn.source_port} ({source_port.data_type.value}) -> "
                                    f"{node.__class__.__name__}.{conn.target_port} ({target_port.data_type.value})"
                                )

                                context.add_error(node.node_id, error_msg)
                                raise WorkflowExecutionException(error_msg)

                node.set_input(conn.target_port, source_output)

    # TODO(P2, 2h): Enhance type validation to support more complex type relationships
    # Pseudo code for complex type relationships:
    # - Support union types (e.g., EMAIL | EMAIL_LIST)
    # - Handle inheritance relationships
    # - Support generic types with constraints
    # - Add type aliases and custom type definitions

    # TODO(P2, 3h): Add support for optional input ports with default values
    # Pseudo code for optional ports:
    # - Modify NodePort to include default_value parameter
    # - Update validate_inputs to skip validation for optional ports without values
    # - Modify set_inputs to use default values when not provided

    # TODO(P3, 4h): Implement input transformation pipeline for incompatible but convertible types
    # Pseudo code for transformation pipeline:
    # - Create TypeTransformer class with conversion methods
    # - Add transform_input method to BaseNode
    # - Support common conversions (string to json, list to single item, etc.)
    # - Add transformation cost/priority system

    def _validate_type_compatibility(
        self, source_type: "DataType", target_type: "DataType"
    ) -> bool:
        """Validate if source and target types are compatible."""
        if target_type == DataType.ANY:
            return True
        if source_type == target_type:
            return True

        # Check for compatible type relationships (e.g., EMAIL_LIST can go to EMAIL)
        if target_type == DataType.EMAIL and source_type == DataType.EMAIL_LIST:
            return True  # A list can be treated as a single item in some contexts
        if target_type == DataType.JSON and source_type in [
            DataType.STRING,
            DataType.NUMBER,
            DataType.BOOLEAN,
        ]:
            return True  # Primitive types can be serialized to JSON

        # Add more type compatibility rules as needed
        return False

    # TODO(P1, 4h): Expand type compatibility rules to support all defined DataType combinations
    # Pseudo code for expanded type compatibility:
    # - Add compatibility matrix for all DataType combinations
    # - Support OBJECT to JSON conversion
    # - Handle TEXT/STRING interchangeability
    # - Add NUMBER to STRING conversion for display purposes

    # TODO(P2, 3h): Add support for generic types and type parameters
    # Pseudo code for generic types:
    # - Create GenericType class with type parameters
    # - Support List[T], Dict[K,V] style generics
    # - Add type parameter validation and inference
    # - Handle generic type compatibility checking

    # TODO(P3, 2h): Implement type coercion for compatible but distinct types
    # Pseudo code for type coercion:
    # - Create TypeCoercer class with coercion methods
    # - Add safe coercion (no data loss) vs unsafe coercion
    # - Support string to number, number to string conversions
    # - Add coercion cost and safety ratings

    async def execute_workflow_async(
        self, workflow: Workflow, initial_inputs: Dict[str, Any] = None
    ) -> ExecutionContext:
        """
        Execute a workflow asynchronously without blocking.

        Args:
            workflow: The workflow to execute
            initial_inputs: Initial input values for the workflow

        Returns:
            ExecutionContext containing the results and metadata
        """
        return await self.execute_workflow(workflow, initial_inputs)

    async def cancel_execution(self, execution_id: str):
        """Cancel an in-progress execution (not fully implemented)."""
        if execution_id in self.active_executions:
            context = self.active_executions[execution_id]
            context.metadata["status"] = "cancelled"
            context.metadata["cancelled_at"] = datetime.now()
            # In a real implementation, we would need to implement actual cancellation
            # which requires cooperative cancellation in all nodes
            del self.active_executions[execution_id]
            self.logger.info(f"Execution {execution_id} cancelled")

    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get the status of an execution."""
        if execution_id in self.active_executions:
            context = self.active_executions[execution_id]
            return {
                "execution_id": execution_id,
                "status": "running",
                "execution_path": context.execution_path,
            }
        else:
            # In a real system, we would check completed executions
            return {
                "execution_id": execution_id,
                "status": "not_found_or_completed",
            }


# Global workflow engine instance
workflow_engine = WorkflowEngine(
    SecurityManager(user_roles={})
)  # Instantiate with a default SecurityManager
