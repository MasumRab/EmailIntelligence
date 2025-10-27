"""
Advanced Node-Based Workflow Engine for Email Intelligence Platform

Implements a sophisticated, extensible workflow system inspired by ComfyUI, automatic1111,
and Stability-AI frameworks with enterprise-grade security and scalability.

This module provides:
- Node-based processing architecture with dependency management
- Plugin extensibility system
- Performance monitoring
- Workflow persistence and sharing
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import networkx as nx

logger = logging.getLogger(__name__)

# Import security features if available
try:
    from .security import DataSanitizer, Permission, SecurityContext, SecurityLevel, SecurityManager

    security_available = True
except ImportError:
    SecurityContext = None
    security_available = False
    print("Security module not available, proceeding without advanced security features")


class NodeExecutionStatus(Enum):
    """Status of node execution"""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class NodeMetadata:
    """Metadata for a node"""

    name: str
    description: str
    version: str
    input_types: Dict[str, type]
    output_types: Dict[str, type]


class BaseNode(ABC):
    """
    Abstract base class for all processing nodes in the workflow system.

    This follows patterns similar to ComfyUI's node architecture with additional
    enterprise features like security contexts and performance monitoring.
    """

    def __init__(self, node_id: str, name: str, workflow_id: str):
        self.node_id = node_id
        self.name = name
        self.workflow_id = workflow_id
        self._execution_context: Dict[str, Any] = {}
        self._security_context: Optional[SecurityContext] = None
        self._status: NodeExecutionStatus = NodeExecutionStatus.PENDING
        self._last_executed: Optional[float] = None

    @abstractmethod
    def get_metadata(self) -> NodeMetadata:
        """Return metadata about the node"""
        pass

    @abstractmethod
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return outputs"""
        pass

    def set_security_context(self, context: Optional[SecurityContext]):
        """Set the security context for this node"""
        self._security_context = context

    def get_security_context(self) -> Optional[SecurityContext]:
        """Get the security context for this node"""
        return self._security_context

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the node with security and performance monitoring.

        This method provides a standardized execution wrapper that handles:
        - Security context validation (when security is available)
        - Performance monitoring
        - Error handling
        - Status tracking
        """
        logger.info(f"Executing node {self.name} ({self.node_id}) in workflow {self.workflow_id}")

        start_time = time.time()
        self._status = NodeExecutionStatus.RUNNING

        # If security is available, validate and sanitize inputs
        if security_available and self._security_context:
            from .security import security_manager

            # Validate access and sanitize inputs
            sanitized_inputs = DataSanitizer.sanitize_input(inputs)
        else:
            sanitized_inputs = inputs

        try:
            # Execute the node's processing logic
            output = await self.process(sanitized_inputs)

            execution_time = time.time() - start_time

            # If security is available, sanitize outputs
            if security_available and self._security_context:
                final_output = DataSanitizer.sanitize_output(output)
            else:
                final_output = output

            self._status = NodeExecutionStatus.SUCCESS
            self._last_executed = time.time()

            logger.info(f"Node {self.name} executed successfully in {execution_time:.2f}s")
            return final_output

        except Exception as e:
            execution_time = time.time() - start_time
            self._status = NodeExecutionStatus.FAILED
            logger.error(f"Node {self.name} failed: {str(e)}", exc_info=True)
            raise

    def get_status(self) -> NodeExecutionStatus:
        """Get current execution status"""
        return self._status


class Connection:
    """Represents a connection between two nodes"""

    def __init__(
        self,
        source_node_id: str,
        source_output: str,
        target_node_id: str,
        target_input: str,
        connection_id: Optional[str] = None,
    ):
        self.connection_id = connection_id or str(uuid4())
        self.source_node_id = source_node_id
        self.source_output = source_output
        self.target_node_id = target_node_id
        self.target_input = target_input

    def to_dict(self) -> Dict[str, str]:
        """Convert connection to dictionary for serialization"""
        return {
            "connection_id": self.connection_id,
            "source_node_id": self.source_node_id,
            "source_output": self.source_output,
            "target_node_id": self.target_node_id,
            "target_input": self.target_input,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Connection":
        """Create connection from dictionary"""
        return cls(
            connection_id=data.get("connection_id"),
            source_node_id=data["source_node_id"],
            source_output=data["source_output"],
            target_node_id=data["target_node_id"],
            target_input=data["target_input"],
        )


class Workflow:
    """Represents a complete node-based workflow"""

    def __init__(self, name: str, description: str = ""):
        self.workflow_id = str(uuid4())
        self.name = name
        self.description = description
        self.version = "1.0.0"
        self.nodes: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, str]] = []
        self.config: Dict[str, Any] = {}
        self.created_at = time.time()
        self.updated_at = time.time()
        self.metadata: Dict[str, Any] = {}

    def add_node(
        self,
        node_type: str,
        node_id: Optional[str] = None,
        x: float = 0.0,
        y: float = 0.0,
        **kwargs,
    ) -> str:
        """Add a node to the workflow"""
        node_id = node_id or f"{node_type}_{len(self.nodes)}"

        node_data = {
            "id": node_id,
            "type": node_type,
            "position": {"x": x, "y": y},
            "parameters": kwargs,
        }

        self.nodes.append(node_data)
        self.updated_at = time.time()
        return node_id

    def add_connection(
        self, source_node_id: str, source_output: str, target_node_id: str, target_input: str
    ):
        """Add a connection between nodes"""
        connection = {
            "source_node_id": source_node_id,
            "source_output": source_output,
            "target_node_id": target_node_id,
            "target_input": target_input,
        }

        self.connections.append(connection)
        self.updated_at = time.time()

    def to_graph(self) -> nx.DiGraph:
        """Convert workflow to a NetworkX directed graph for topological analysis"""
        graph = nx.DiGraph()

        # Add nodes
        for node in self.nodes:
            graph.add_node(node["id"], **node)

        # Add edges based on connections
        for conn in self.connections:
            graph.add_edge(
                conn["source_node_id"],
                conn["target_node_id"],
                source_output=conn["source_output"],
                target_input=conn["target_input"],
            )

        return graph

    def get_execution_order(self) -> List[str]:
        """Get the execution order of nodes based on dependencies"""
        graph = self.to_graph()

        try:
            # Use topological sort to determine execution order
            execution_order = list(nx.topological_sort(graph))
            return execution_order
        except nx.NetworkXUnfeasible:
            # If there's a cycle, raise an error
            raise ValueError("Workflow contains cycles, which are not allowed")

    def get_node_inputs(self, node_id: str) -> Dict[str, Any]:
        """Get input connections for a specific node"""
        inputs = {}
        for conn in self.connections:
            if conn["target_node_id"] == node_id:
                inputs[conn["target_input"]] = {
                    "source_node_id": conn["source_node_id"],
                    "source_output": conn["source_output"],
                }
        return inputs

    def get_node_outputs(self, node_id: str) -> Dict[str, Any]:
        """Get output connections for a specific node"""
        outputs = {}
        for conn in self.connections:
            if conn["source_node_id"] == node_id:
                output_key = conn["source_output"]
                if output_key not in outputs:
                    outputs[output_key] = []
                outputs[output_key].append(
                    {"target_node_id": conn["target_node_id"], "target_input": conn["target_input"]}
                )
        return outputs

    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary for serialization"""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "nodes": self.nodes,
            "connections": self.connections,
            "config": self.config,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        """Create workflow from dictionary"""
        workflow = cls(
            name=data.get("name", "Unnamed Workflow"), description=data.get("description", "")
        )
        workflow.workflow_id = data.get("workflow_id", str(uuid4()))
        workflow.version = data.get("version", "1.0.0")
        workflow.nodes = data.get("nodes", [])
        workflow.connections = data.get("connections", [])
        workflow.config = data.get("config", {})
        workflow.created_at = data.get("created_at", time.time())
        workflow.updated_at = data.get("updated_at", time.time())
        workflow.metadata = data.get("metadata", {})

        return workflow


class WorkflowExecutionResult:
    """Result of workflow execution"""

    def __init__(
        self,
        workflow_id: str,
        status: str,
        execution_time: float,
        node_results: Dict[str, Any],
        error: Optional[str] = None,
    ):
        self.workflow_id = workflow_id
        self.status = status
        self.execution_time = execution_time
        self.node_results = node_results
        self.error = error


class WorkflowRunner:
    """
    Executes workflows with performance monitoring and error handling.

    This runner handles the complex task of executing node-based workflows,
    managing dependencies, and ensuring secure execution.
    """

    def __init__(
        self,
        node_registry: Dict[str, type],
        max_concurrent_nodes: int = 5,
        security_context: Optional[SecurityContext] = None,
    ):
        self.node_registry = node_registry
        self.max_concurrent_nodes = max_concurrent_nodes
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent_nodes)
        self._running_workflows = set()
        self.security_context = security_context

    async def run_workflow(
        self,
        workflow: Workflow,
        initial_inputs: Optional[Dict[str, Any]] = None,
        workflow_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecutionResult:
        """
        Execute a workflow with all security and performance features.

        This method implements the core execution logic with:
        - Topological sorting of nodes
        - Dependency resolution
        - Performance monitoring
        - Error handling and recovery
        """
        logger.info(f"Starting execution of workflow: {workflow.name} ({workflow.workflow_id})")
        start_time = time.time()

        workflow_id = workflow.workflow_id
        self._running_workflows.add(workflow_id)

        try:
            # Initialize execution context
            context = {
                "__initial_inputs": initial_inputs or {},
                "__workflow_context": workflow_context or {},
                "__node_outputs": {},
                "__execution_start_time": start_time,
            }

            # Get execution order
            execution_order = workflow.get_execution_order()
            logger.info(f"Execution order: {execution_order}")

            # Execute nodes in topological order
            for node_id in execution_order:
                # Check if workflow execution should be cancelled
                if workflow_id not in self._running_workflows:
                    break

                node_data = self._find_node_by_id(workflow, node_id)
                if not node_data:
                    continue

                # Build inputs for this node
                node_inputs = self._build_node_inputs(workflow, node_id, context)

                # Execute the node
                result = await self._execute_node(
                    workflow=workflow, node_data=node_data, inputs=node_inputs, context=context
                )

                # Store the result
                context["__node_outputs"][node_id] = result

            execution_time = time.time() - start_time

            logger.info(f"Workflow {workflow.name} completed successfully in {execution_time:.2f}s")

            return WorkflowExecutionResult(
                workflow_id=workflow_id,
                status="success",
                execution_time=execution_time,
                node_results=context["__node_outputs"],
            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Workflow {workflow.name} failed: {str(e)}", exc_info=True)

            return WorkflowExecutionResult(
                workflow_id=workflow_id,
                status="failed",
                execution_time=execution_time,
                node_results={},
                error=str(e),
            )
        finally:
            self._running_workflows.discard(workflow_id)

    async def _execute_node(
        self,
        workflow: Workflow,
        node_data: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a single node in the workflow"""
        node_type = node_data["type"]

        # Get the node class from registry
        node_class = self.node_registry.get(node_type)
        if not node_class:
            raise ValueError(f"Unknown node type: {node_type}")

        # Create node instance
        node = node_class(
            node_id=node_data["id"],
            name=node_data.get("name", node_type),
            workflow_id=workflow.workflow_id,
        )

        # Set security context if available
        if security_available and self.security_context:
            node.set_security_context(self.security_context)

        # Execute the node
        result = await node.execute(inputs)
        return result

    def _build_node_inputs(
        self, workflow: Workflow, node_id: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build inputs for a node based on connections and initial inputs"""
        inputs = {}

        # Get direct inputs to this node
        node_inputs = workflow.get_node_inputs(node_id)

        for input_name, source_info in node_inputs.items():
            source_node_id = source_info["source_node_id"]
            source_output = source_info["source_output"]

            # Get the output from the source node
            if source_node_id in context["__node_outputs"]:
                source_outputs = context["__node_outputs"][source_node_id]
                if source_output in source_outputs:
                    inputs[input_name] = source_outputs[source_output]
                else:
                    raise ValueError(
                        f"Source node {source_node_id} did not produce output {source_output}"
                    )
            else:
                # This shouldn't happen in a properly connected workflow
                raise ValueError(f"Source node {source_node_id} has not been executed")

        # Also include any direct workflow-level inputs
        for input_name, value in context["__initial_inputs"].items():
            if input_name not in inputs:  # Don't override connected inputs
                inputs[input_name] = value

        return inputs

    def _find_node_by_id(self, workflow: Workflow, node_id: str) -> Optional[Dict[str, Any]]:
        """Find a node in the workflow by its ID"""
        for node in workflow.nodes:
            if node["id"] == node_id:
                return node
        return None

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        if workflow_id in self._running_workflows:
            self._running_workflows.discard(workflow_id)
            logger.info(f"Cancelled workflow execution: {workflow_id}")
            return True
        return False

    def get_running_workflows(self) -> List[str]:
        """Get list of currently running workflow IDs"""
        return list(self._running_workflows)


class WorkflowManager:
    """
    Manages workflow persistence, execution, and sharing with enterprise-grade features.
    """

    def __init__(self, workflows_dir: str = "data/workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows_dir.mkdir(exist_ok=True, parents=True)
        self._workflows: Dict[str, Workflow] = {}
        self._workflow_runners: Dict[str, WorkflowRunner] = {}
        self._node_registry: Dict[str, type] = {}

    def register_node_type(self, node_type: str, node_class: type):
        """Register a new node type"""
        self._node_registry[node_type] = node_class

    def get_registered_node_types(self) -> List[str]:
        """Get list of registered node types"""
        return list(self._node_registry.keys())

    def create_workflow(self, name: str, description: str = "") -> Workflow:
        """Create a new workflow"""
        workflow = Workflow(name=name, description=description)
        self._workflows[workflow.workflow_id] = workflow
        return workflow

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID"""
        return self._workflows.get(workflow_id)

    def save_workflow(self, workflow: Workflow, filename: Optional[str] = None) -> bool:
        """Save a workflow to file"""
        try:
            if filename is None:
                safe_name = workflow.name.replace(" ", "_").replace("/", "_")
                filename = f"{safe_name}_{workflow.workflow_id[:8]}.json"

            filepath = self.workflows_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(workflow.to_dict(), f, indent=2, ensure_ascii=False)

            logger.info(f"Workflow saved to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save workflow: {str(e)}")
            return False

    def load_workflow(self, workflow_filename: Union[str, Path]) -> Optional[Workflow]:
        """Load a workflow from file"""
        try:
            # Always join the user-provided filename with the workflows_dir, then normalize & check it's inside
            candidate_path = self.workflows_dir / workflow_filename
            fullpath = candidate_path.resolve()
            workflows_dir_resolved = self.workflows_dir.resolve()
            try:
                # This will raise ValueError if fullpath is not inside workflows_dir_resolved
                fullpath.relative_to(workflows_dir_resolved)
            except ValueError:
                logger.error(f"Access to file outside workflow directory is not allowed: {fullpath}")
                return None

            if not fullpath.is_file():
                logger.error(f"Workflow file does not exist: {fullpath}")
                return None

            with open(fullpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            workflow = Workflow.from_dict(data)
            self._workflows[workflow.workflow_id] = workflow
            logger.info(f"Workflow loaded from {fullpath}")
            return workflow

        except Exception as e:
            logger.error(f"Failed to load workflow from {workflow_filename}: {str(e)}")
            return None

    def list_workflows(self) -> List[str]:
        """List saved workflow files"""
        return [f.name for f in self.workflows_dir.glob("*.json")]

    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow from memory and storage"""
        if workflow_id in self._workflows:
            del self._workflows[workflow_id]

        # Also try to delete the file if it exists
        for file in self.workflows_dir.glob(f"*{workflow_id[:8]}*.json"):
            try:
                file.unlink()
            except Exception:
                logger.warning(f"Could not delete workflow file: {file}")

        return True

    async def execute_workflow(
        self,
        workflow_id: str,
        initial_inputs: Optional[Dict[str, Any]] = None,
        security_context: Optional[SecurityContext] = None,
    ) -> WorkflowExecutionResult:
        """Execute a workflow asynchronously"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        # Create a runner for this execution
        runner = WorkflowRunner(self._node_registry, security_context=security_context)

        # Execute the workflow
        result = await runner.run_workflow(workflow, initial_inputs)
        return result

    def get_workflow_by_name(self, name: str) -> Optional[Workflow]:
        """Get a workflow by name (not ID)"""
        for workflow in self._workflows.values():
            if workflow.name == name:
                return workflow
        return None


# Example node implementations that demonstrate the advanced workflow system
class EmailInputNode(BaseNode):
    """Node that represents an email input"""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Email Input",
            description="Provides email data as input to the workflow",
            version="1.0.0",
            input_types={},
            output_types={"email": dict, "subject": str, "content": str, "sender": str},
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # For now, we'll use the inputs directly as the email data
        # In a real implementation, this would fetch from an API, database, etc.
        email_data = inputs.get("email_data", {})

        return {
            "email": email_data,
            "subject": email_data.get("subject", ""),
            "content": email_data.get("content", ""),
            "sender": email_data.get("sender", ""),
        }


class NLPProcessorNode(BaseNode):
    """Node that processes email content with NLP analysis"""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="NLP Processor",
            description="Performs NLP analysis on email content",
            version="1.0.0",
            input_types={"content": str, "subject": str},
            output_types={"analysis": dict, "sentiment": str, "topic": str, "keywords": list},
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Mock NLP processing - in real implementation, this would call the AI engine
        content = inputs.get("content", "")
        subject = inputs.get("subject", "")

        # Mock analysis results
        analysis = {
            "sentiment": (
                "positive" if "good" in content.lower() or "great" in content.lower() else "neutral"
            ),
            "topic": (
                "business"
                if "meeting" in content.lower() or "work" in content.lower()
                else "personal"
            ),
            "keywords": ["email", "content", "analysis"],  # Extract keywords from content
        }

        return {
            "analysis": analysis,
            "sentiment": analysis["sentiment"],
            "topic": analysis["topic"],
            "keywords": analysis["keywords"],
        }


class EmailOutputNode(BaseNode):
    """Node that outputs processed email data"""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Email Output",
            description="Outputs the final processed email data",
            version="1.0.0",
            input_types={"email": dict, "analysis": dict},
            output_types={"processed_email": dict, "status": str},
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Combine email and analysis data
        email = inputs.get("email", {})
        analysis = inputs.get("analysis", {})

        processed_email = {
            **email,
            "nlp_analysis": analysis,
            "processed_timestamp": time.time(),
            "workflow_id": self.workflow_id,
        }

        return {"processed_email": processed_email, "status": "completed"}


# Default workflow manager instance
workflow_manager: Optional[WorkflowManager] = None


def initialize_workflow_system() -> WorkflowManager:
    """Initialize the workflow system with default nodes"""
    global workflow_manager
    workflow_manager = WorkflowManager()

    # Register default node types
    workflow_manager.register_node_type("email_input", EmailInputNode)
    workflow_manager.register_node_type("nlp_processor", NLPProcessorNode)
    workflow_manager.register_node_type("email_output", EmailOutputNode)

    return workflow_manager


def get_workflow_manager() -> WorkflowManager:
    """Get the global workflow manager instance"""
    import warnings

    warnings.warn(
        "get_workflow_manager from src.core.advanced_workflow_engine is deprecated. "
        "Use backend.node_engine.workflow_manager.workflow_manager instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    if not workflow_manager:
        # Initialize with default configuration
        return initialize_workflow_system()
    return workflow_manager
