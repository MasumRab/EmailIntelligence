"""
Workflow Execution Engine for the Email Intelligence Platform.

This module manages the execution of node-based workflows, handling
dependencies, execution order, and error management.
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from backend.node_engine.node_base import (
    BaseNode, Workflow, ExecutionContext, Connection
)
from backend.node_engine.security_manager import (
    security_manager, audit_logger, resource_manager, 
    ExecutionSandbox, InputSanitizer, ResourceLimits
)


class WorkflowExecutionException(Exception):
    """Exception raised when workflow execution fails."""
    pass


class WorkflowEngine:
    """Manages execution of node-based workflows."""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.active_executions: Dict[str, ExecutionContext] = {}
        self.node_registry: Dict[str, type] = {}
    
    def register_node_type(self, node_class: type):
        """Register a node type for workflow composition."""
        self.node_registry[node_class.__name__] = node_class
        self.logger.info(f"Registered node type: {node_class.__name__}")
    
    def get_registered_node_types(self) -> List[str]:
        """Get list of all registered node types."""
        return list(self.node_registry.keys())
    
    async def execute_workflow(self, workflow: Workflow, 
                              initial_inputs: Dict[str, Any] = None,
                              user_id: str = None) -> ExecutionContext:
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
        
        # Audit log workflow start
        audit_logger.log_workflow_start(execution_id, workflow.name, user_id)
        
        # Sanitize initial inputs
        if initial_inputs:
            initial_inputs = InputSanitizer._sanitize_dict(initial_inputs or {})
        
        # Acquire resources for the workflow
        resources_acquired = await resource_manager.acquire_resources(execution_id, ResourceLimits())
        if not resources_acquired:
            raise WorkflowExecutionException(f"Unable to acquire resources for workflow {execution_id}")
        
        # Create execution context
        context = ExecutionContext()
        context.metadata["workflow_id"] = workflow.workflow_id
        context.metadata["workflow_name"] = workflow.name
        context.metadata["start_time"] = datetime.now()
        context.metadata["initial_inputs"] = initial_inputs or {}
        context.metadata["user_id"] = user_id
        
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
            sandbox = ExecutionSandbox(security_manager)
            for node_id in execution_order:
                node = workflow.nodes[node_id]
                
                # Validate node execution based on security policies
                node_type = node.__class__.__name__
                if not security_manager.validate_node_execution(node_type, getattr(node, 'config', {})):
                    error_msg = f"Security validation failed for node {node_id} ({node_type})"
                    context.add_error(node_id, error_msg)
                    audit_logger.log_security_event("NODE_EXECUTION_BLOCKED", {
                        "node_id": node_id,
                        "node_type": node_type,
                        "workflow_id": workflow.workflow_id
                    })
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
                    if not security_manager.check_api_call_limit(workflow.workflow_id, node_id):
                        raise WorkflowExecutionException(f"API call limit exceeded for node {node_id}")
                    
                    start_time = datetime.now()
                    result = await sandbox.execute_with_timeout(
                        node.execute, 
                        30,  # 30 second timeout per node
                        context
                    )
                    execution_duration = (datetime.now() - start_time).total_seconds()
                    
                    context.set_node_output(node_id, result)
                    context.execution_path.append(node_id)
                    self.logger.debug(f"Node {node_id} executed successfully")
                    
                    # Log node execution
                    audit_logger.log_node_execution(
                        workflow.workflow_id, 
                        node_id, 
                        node.name, 
                        "success", 
                        execution_duration
                    )
                except Exception as e:
                    error_msg = f"Node {node_id} execution failed: {str(e)}"
                    context.add_error(node_id, error_msg, {"exception": str(e), "type": type(e).__name__})
                    self.logger.error(error_msg, exc_info=True)
                    
                    # Log failed node execution
                    audit_logger.log_node_execution(
                        workflow.workflow_id, 
                        node_id, 
                        node.name, 
                        "failed", 
                        -1  # Indicate error
                    )
                    
                    raise WorkflowExecutionException(error_msg) from e
            
            # Set completion metadata
            context.metadata["end_time"] = datetime.now()
            context.metadata["execution_duration"] = (
                context.metadata["end_time"] - context.metadata["start_time"]
            ).total_seconds()
            context.metadata["status"] = "completed"
            
            self.logger.info(f"Workflow {workflow.name} completed successfully in {context.metadata['execution_duration']:.2f}s")
            
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
    
    async def _set_initial_inputs(self, workflow: Workflow, 
                                 context: ExecutionContext, 
                                 initial_inputs: Dict[str, Any]):
        """Set initial input values to appropriate source nodes."""
        # For now, set all initial inputs as shared state
        # In the future, we might want to map initial inputs to specific nodes based on metadata
        context.shared_state.update(initial_inputs)
    
    async def _set_node_inputs(self, node: BaseNode, workflow: Workflow, 
                              context: ExecutionContext):
        """Set input values for a node based on connected node outputs."""
        connections = workflow.get_connections_for_node(node.node_id)
        
        # Find connections where this node is the target
        input_connections = [
            conn for conn in connections 
            if conn.target_node_id == node.node_id
        ]
        
        # Set inputs based on connected outputs
        for conn in input_connections:
            source_output = context.get_node_output(conn.source_node_id, conn.source_port)
            if source_output is not None:
                node.set_input(conn.target_port, source_output)
    
    async def execute_workflow_async(self, workflow: Workflow, 
                                   initial_inputs: Dict[str, Any] = None) -> ExecutionContext:
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
workflow_engine = WorkflowEngine()