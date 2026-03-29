<<<<<<< HEAD
import logging
import time
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import networkx as nx
import psutil  # For memory monitoring

logger = logging.getLogger(__name__)


class NodeExecutionStatus(Enum):
    """Status of node execution"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class Node:
    """
    Represents a single node in a processing workflow.

    Each node encapsulates a specific operation, such as fetching an email,
    analyzing its sentiment, or applying a category. Nodes define their
    required inputs and the outputs they produce.
    """

    def __init__(
        self, node_id: str, name: str, operation: Callable, inputs: List[str], outputs: List[str],
        failure_strategy: str = "stop", conditional_expression: Optional[str] = None
    ):
        self.node_id = node_id
        self.name = name
        self.operation = operation
        self.inputs = inputs
        self.outputs = outputs
        self.failure_strategy = failure_strategy  # "stop", "continue", or "retry"
        self.conditional_expression = conditional_expression  # Optional conditional for execution
        self.status = NodeExecutionStatus.PENDING

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the node's operation using the provided context.
        """
        self.status = NodeExecutionStatus.RUNNING

        try:
            # Prepare the arguments for the operation from the context
            args = [context[key] for key in self.inputs]

            # Execute the operation
            result = self.operation(*args)

            # If the node produces multiple outputs, we expect the operation
            # to return a tuple. Otherwise, a single value.
            if len(self.outputs) == 1:
                node_result = {self.outputs[0]: result}
            else:
                node_result = {name: value for name, value in zip(self.outputs, result)}

            self.status = NodeExecutionStatus.SUCCESS
            return node_result

        except Exception as e:
            self.status = NodeExecutionStatus.FAILED
            logger.error(f"Error executing node '{self.name}' ({self.node_id}): {e}", exc_info=True)
            raise


class Workflow:
    """
    Represents a processing workflow as a directed acyclic graph (DAG) of nodes.
    """

    def __init__(self, name: str, nodes: Dict[str, Node], connections: List[Dict[str, str]]):
        self.name = name
        self.nodes = nodes
        self.connections = connections  # List of connections in the format {"from": {"node_id": str, "output": str}, "to": {"node_id": str, "input": str}}

    def to_graph(self) -> nx.DiGraph:
        """
        Convert workflow to a NetworkX directed graph for topological analysis.
        """
        graph = nx.DiGraph()

        # Add nodes to the graph
        for node_id in self.nodes:
            graph.add_node(node_id)

        # Add edges based on connections
        for conn in self.connections:
            source_node_id = conn["from"]["node_id"]
            target_node_id = conn["to"]["node_id"]
            graph.add_edge(source_node_id, target_node_id)

        return graph

    def get_execution_order(self) -> List[str]:
        """
        Get the execution order of nodes based on dependencies using topological sort.
        """
        graph = self.to_graph()

        try:
            # Use topological sort to determine execution order
            execution_order = list(nx.topological_sort(graph))
            return execution_order
        except nx.NetworkXUnfeasible:
            # If there's a cycle, raise an error
            raise ValueError("Workflow contains cycles, which are not allowed")

    def validate(self) -> (bool, List[str]):
        """
        Validate the workflow before execution.
        Returns a tuple of (is_valid, list_of_errors).
        """
        errors = []

        # Check that all nodes have unique IDs
        node_ids = list(self.nodes.keys())
        if len(node_ids) != len(set(node_ids)):
            errors.append("Duplicate node IDs found in workflow")

        # Check that all connections reference valid nodes
        for i, conn in enumerate(self.connections):
            from_node_id = conn["from"]["node_id"]
            to_node_id = conn["to"]["node_id"]

            if from_node_id not in self.nodes:
                errors.append(f"Connection {i}: Source node '{from_node_id}' does not exist")
            if to_node_id not in self.nodes:
                errors.append(f"Connection {i}: Target node '{to_node_id}' does not exist")

        # Check for cycles using the topological sort
        try:
            self.get_execution_order()
        except ValueError as e:
            errors.append(str(e))

        # Check that inputs and outputs are properly connected
        for conn in self.connections:
            from_node_id = conn["from"]["node_id"]
            to_node_id = conn["to"]["node_id"]
            expected_output = conn["from"]["output"]
            expected_input = conn["to"]["input"]

            # Check if the output exists in the source node
            if from_node_id in self.nodes:
                source_node = self.nodes[from_node_id]
                if expected_output not in source_node.outputs:
<<<<<<< HEAD
                    errors.append(f"Connection from {from_node_id} to {to_node_id}: Output '{expected_output}' does not exist in source node")
=======
                    errors.append(
                        f"Connection from {from_node_id} to {to_node_id}: "
                        f"Output '{expected_output}' does not exist in source node"
                    )
>>>>>>> scientific

            # Check if the input exists in the target node
            if to_node_id in self.nodes:
                target_node = self.nodes[to_node_id]
                if expected_input not in target_node.inputs:
<<<<<<< HEAD
                    errors.append(f"Connection from {from_node_id} to {to_node_id}: Input '{expected_input}' does not exist in target node")
=======
                    errors.append(
                        f"Connection from {from_node_id} to {to_node_id}: "
                        f"Input '{expected_input}' does not exist in target node"
                    )
>>>>>>> scientific

        return len(errors) == 0, errors


import asyncio
from concurrent.futures import ThreadPoolExecutor

class WorkflowRunner:
    """
    Executes a workflow by processing its nodes in the correct topological order.

    Enhanced with:
    - Proper topological sorting
    - Error handling and recovery
    - Conditional execution
    - Memory optimization
    - Parallel execution
    - Monitoring and metrics
    """

    def __init__(self, workflow: Workflow, fail_on_error: bool = False, max_retries: int = 1, max_concurrent: int = 5):
        self.workflow = workflow
        self.fail_on_error = fail_on_error
        self.max_retries = max_retries
        self.max_concurrent = max_concurrent  # Maximum number of nodes to execute in parallel
        self.execution_context = {}
        self.node_results = {}
        self.execution_stats = {
            "nodes_executed": 0,
            "nodes_total": len(workflow.nodes),
            "nodes_successful": 0,
            "nodes_failed": 0,
            "nodes_skipped": 0,
            "total_execution_time": 0,
            "start_time": time.time(),
            "end_time": None,
            "errors": [],
            "retries_performed": 0,
            "node_execution_times": {},  # Track execution time per node
            "memory_usage_peak": 0,  # Track peak memory usage
            "parallelism_utilization": 0,  # Track parallelism utilization
        }

    def run(self, initial_context: Dict[str, Any], memory_optimized: bool = False, parallel_execution: bool = False):
        """
        Executes the workflow with proper topological sorting of nodes to determine execution order.
        Enhanced with comprehensive error handling and recovery, memory optimization, and optional parallel execution.
        """
        import time
        start_time = time.time()

        logger.info(f"Running workflow: {self.workflow.name}")
        self.execution_context.update(initial_context)

        # Validate the workflow before execution
        is_valid, validation_errors = self.workflow.validate()
        if not is_valid:
            validation_error_msg = f"Workflow validation failed: {', '.join(validation_errors)}"
            logger.error(validation_error_msg)
            return {
                "success": False,
                "error": validation_error_msg,
                "results": {},
                "stats": {"nodes_executed": 0, "total_execution_time": 0, "errors": validation_errors}
            }

        try:
            # Get current memory usage
            current_process = psutil.Process()
            initial_memory = current_process.memory_info().rss / 1024 / 1024  # MB

            # Get execution order using topological sort
            execution_order = self.workflow.get_execution_order()
            logger.info(f"Execution order: {execution_order}")

            # If memory optimization is enabled, pre-calculate which nodes' results can be cleaned up
            cleanup_schedule = {}
            if memory_optimized:
                cleanup_schedule = self._calculate_cleanup_schedule(execution_order)

            if parallel_execution:
                # Execute with parallel execution for independent nodes
                result = asyncio.run(self._run_parallel(execution_order, cleanup_schedule))
            else:
                # Execute nodes in topological order sequentially
                result = self._run_sequential(execution_order, cleanup_schedule)

            execution_time = time.time() - start_time
            self.execution_stats["total_execution_time"] = execution_time

            # Track final memory usage
            current_process = psutil.Process()
            final_memory = current_process.memory_info().rss / 1024 / 1024  # MB
            memory_used = final_memory - initial_memory
            self.execution_stats["memory_usage_peak"] = max(self.execution_stats["memory_usage_peak"], final_memory)

            logger.info(f"Workflow execution completed in {execution_time:.2f}s.")
            logger.info(f"Memory used: {memory_used:.2f} MB")

            # Update the end_time
            self.execution_stats["end_time"] = time.time()

            return {
                "success": True,
                "results": self.node_results,
                "context": self.execution_context,
                "stats": self.execution_stats
            }

        except Exception as e:
            execution_time = time.time() - start_time
            self.execution_stats["total_execution_time"] = execution_time
            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)

            return {
                "success": False,
                "error": str(e),
                "results": self.node_results,
                "stats": self.execution_stats
            }

    def _run_sequential(self, execution_order, cleanup_schedule):
        """Execute workflow nodes sequentially"""
        for node_id in execution_order:
            logger.info(f"Executing node: {node_id}")

            node = self.workflow.nodes.get(node_id)
            if not node:
                error_msg = f"Node {node_id} not found in workflow"
                logger.error(error_msg)
                self.execution_stats["errors"].append(error_msg)
                if self.fail_on_error:
                    raise ValueError(error_msg)
                continue

            # Check if node should be executed based on condition
            if node.conditional_expression and not self._evaluate_condition(node.conditional_expression):
                node.status = NodeExecutionStatus.SKIPPED
                logger.info(f"Condition not met for node {node_id}, skipping execution")
                self.execution_stats["nodes_skipped"] += 1
                continue

            # Update execution stats
            self.execution_stats["nodes_executed"] += 1

            # Track execution start time for this node
            node_start_time = time.time()

            # Build context for this specific node based on connections
            node_context = self._build_node_context(node_id)

            # Try to execute the node with retries if specified
            success = False
            retry_count = 0

            while not success and retry_count <= self.max_retries:
                try:
                    # Execute the node
                    results = node.execute(node_context)

                    # Store the results for this node
                    self.node_results[node_id] = results

                    # Update the main execution context with results
                    self.execution_context.update(results)

                    success = True
                    self.execution_stats["nodes_successful"] += 1

                except Exception as e:
                    retry_count += 1
                    self.execution_stats["retries_performed"] += 1

                    if retry_count <= self.max_retries:
<<<<<<< HEAD
                        logger.warning(f"Node {node.name} failed, retrying ({retry_count}/{self.max_retries}): {str(e)}")
=======
                        logger.warning(
                            f"Node {node.name} failed, retrying "
                            f"({retry_count}/{self.max_retries}): {str(e)}"
                        )
>>>>>>> scientific
                    else:
                        error_msg = f"Node {node.name} ({node_id}) failed after {self.max_retries} retries: {str(e)}"
                        logger.error(error_msg, exc_info=True)
                        self.execution_stats["errors"].append(error_msg)
                        self.execution_stats["nodes_failed"] += 1

                        # Handle failure based on strategy
                        if node.failure_strategy == "stop":
                            raise
                        elif node.failure_strategy == "continue":
                            # Continue with execution
                            continue
                        elif node.failure_strategy == "retry" and retry_count > self.max_retries:
                            # Already retried max times, continue to next node
                            continue

            # Record execution time for this node
            node_end_time = time.time()
            node_execution_time = node_end_time - node_start_time
            self.execution_stats["node_execution_times"][node_id] = node_execution_time

            # If memory optimization is enabled, clean up results that are no longer needed
            if node_id in cleanup_schedule:
                for node_to_cleanup in cleanup_schedule[node_id]:
                    if node_to_cleanup in self.node_results:
                        del self.node_results[node_to_cleanup]
<<<<<<< HEAD
                        logger.debug(f"Cleaned up results for node {node_to_cleanup} to optimize memory")
=======
                        logger.debug(
                            f"Cleaned up results for node " f"{node_to_cleanup} to optimize memory"
                        )
>>>>>>> scientific

    async def _run_parallel(self, execution_order, cleanup_schedule):
        """Execute workflow nodes in parallel where possible"""
        # Create a queue of nodes that are ready to execute
        ready_nodes = []
        completed_nodes = set()
        node_dependencies = self._calculate_node_dependencies()

        # Initially, all nodes without dependencies are ready
        for node_id in execution_order:
            if not node_dependencies[node_id]:  # No dependencies
                ready_nodes.append(node_id)

        # Track running tasks
        running_tasks = {}

        # Process nodes
        while ready_nodes or running_tasks:
            # Start new tasks up to the concurrency limit
            while ready_nodes and len(running_tasks) < self.max_concurrent:
                node_id = ready_nodes.pop(0)

                # Create an async task to execute the node
                task = asyncio.create_task(self._execute_single_node_with_timing(node_id))
                running_tasks[node_id] = task

            if running_tasks:
                # Wait for at least one task to complete
                done, pending = await asyncio.wait(
                    list(running_tasks.values()),
                    return_when=asyncio.FIRST_COMPLETED
                )

                # Process completed tasks
                for task in done:
                    node_id = None
                    for nid, t in running_tasks.items():
                        if t == task:
                            node_id = nid
                            break

                    if node_id:
                        try:
                            result = await task
                            # Update results
                            self.node_results[node_id] = result
                            # Update the main execution context with results
                            self.execution_context.update(result)
                            completed_nodes.add(node_id)

                            # Update execution stats
                            self.execution_stats["nodes_executed"] += 1
                            self.execution_stats["nodes_successful"] += 1

                            # Add newly ready nodes to the ready queue
                            for candidate_id in execution_order:
                                if candidate_id not in completed_nodes and candidate_id not in running_tasks:
                                    # Check if all dependencies for candidate are met
                                    dependencies_met = all(
                                        dep in completed_nodes for dep in node_dependencies[candidate_id]
                                    )
                                    if dependencies_met:
                                        ready_nodes.append(candidate_id)
                        except Exception as e:
                            # Handle errors in parallel execution
                            node = self.workflow.nodes[node_id]
                            error_msg = f"Node {node.name} ({node_id}) failed: {str(e)}"
                            logger.error(error_msg, exc_info=True)
                            self.execution_stats["errors"].append(error_msg)
                            self.execution_stats["nodes_failed"] += 1

                            # Handle failure based on strategy
                            if node.failure_strategy == "stop":
                                raise
                            else:
                                # If failure strategy is continue, mark as completed anyway
                                completed_nodes.add(node_id)

                        # Remove completed task from running tasks
                        del running_tasks[node_id]

                # If memory optimization is enabled, clean up results that are no longer needed
                for node_id in completed_nodes.copy():  # Use copy to avoid mutation during iteration
                    if node_id in cleanup_schedule:
                        for node_to_cleanup in cleanup_schedule[node_id]:
<<<<<<< HEAD
                            if (node_to_cleanup in self.node_results and
                                node_to_cleanup not in running_tasks and
                                node_to_cleanup not in ready_nodes):
                                del self.node_results[node_to_cleanup]
                                logger.debug(f"Cleaned up results for node {node_to_cleanup} to optimize memory")
=======
                            if (
                                node_to_cleanup in self.node_results
                                and node_to_cleanup not in running_tasks
                                and node_to_cleanup not in ready_nodes
                            ):
                                del self.node_results[node_to_cleanup]
                                logger.debug(
                                    f"Cleaned up results for node "
                                    f"{node_to_cleanup} to optimize memory"
                                )
>>>>>>> scientific

    async def _execute_single_node(self, node_id: str):
        """Execute a single node asynchronously"""
        node = self.workflow.nodes[node_id]

        # Check if node should be executed based on condition
        if node.conditional_expression and not self._evaluate_condition(node.conditional_expression):
            node.status = NodeExecutionStatus.SKIPPED
            logger.info(f"Condition not met for node {node_id}, skipping execution")
            # Update execution stats for skipped nodes
            self.execution_stats["nodes_skipped"] += 1
            return {}

        # Build context for this specific node based on connections
        node_context = self._build_node_context(node_id)

        # Try to execute the node with retries if specified
        success = False
        retry_count = 0

        while not success and retry_count <= self.max_retries:
            try:
                # Execute the node
                result = node.execute(node_context)
                success = True
                return result
            except Exception as e:
                retry_count += 1
                self.execution_stats["retries_performed"] += 1

                if retry_count <= self.max_retries:
<<<<<<< HEAD
                    logger.warning(f"Node {node.name} failed, retrying ({retry_count}/{self.max_retries}): {str(e)}")
=======
                    logger.warning(
                        f"Node {node.name} failed, retrying "
                        f"({retry_count}/{self.max_retries}): {str(e)}"
                    )
>>>>>>> scientific
                else:
                    raise e  # Re-raise the exception after max retries

    async def _execute_single_node_with_timing(self, node_id: str):
        """Execute a single node asynchronously and track execution time"""
        start_time = time.time()
        try:
            result = await self._execute_single_node(node_id)
            end_time = time.time()
            execution_time = end_time - start_time

            # Record execution time for this node
            self.execution_stats["node_execution_times"][node_id] = execution_time

            return result
        except Exception:
            # Even if execution fails, record the time it took
            end_time = time.time()
            execution_time = end_time - start_time
            self.execution_stats["node_execution_times"][node_id] = execution_time
            raise

    def _calculate_node_dependencies(self) -> Dict[str, List[str]]:
        """Calculate which nodes each node depends on"""
        dependencies = {node_id: [] for node_id in self.workflow.nodes}

        for conn in self.workflow.connections:
            target_node = conn["to"]["node_id"]
            source_node = conn["from"]["node_id"]

            if target_node in dependencies and source_node not in dependencies[target_node]:
                dependencies[target_node].append(source_node)

        return dependencies

    def _calculate_cleanup_schedule(self, execution_order: List[str]) -> Dict[str, List[str]]:
        """
        Calculate which node results can be cleaned up after each node executes.
        This helps optimize memory usage by removing results that are no longer needed.
        """
        cleanup_schedule = {}

        # For each node in the execution order, determine which previous nodes' results
        # are no longer needed after this node executes
        for i, node_id in enumerate(execution_order):
            cleanup_schedule[node_id] = []

            # Check all previous nodes to see if their results are still needed
            for prev_node_id in execution_order[:i]:
                # Check if any subsequent nodes need the result from prev_node_id
                still_needed = False

                for subsequent_node_id in execution_order[i+1:]:
                    # Check if there's a connection from prev_node to subsequent_node
                    for conn in self.workflow.connections:
                        if (conn["from"]["node_id"] == prev_node_id and
                            conn["to"]["node_id"] == subsequent_node_id):
                            still_needed = True
                            break
                    if still_needed:
                        break

                # If not still needed by any subsequent nodes, it can be cleaned up
                if not still_needed:
                    cleanup_schedule[node_id].append(prev_node_id)

        return cleanup_schedule

    def _build_node_context(self, node_id: str) -> Dict[str, Any]:
        """
        Build the context for a specific node based on connections and available data.
        """
        # Start with the main execution context
        node_context = self.execution_context.copy()

        # Find all incoming connections to this node
        for conn in self.workflow.connections:
            if conn["to"]["node_id"] == node_id:
                source_node_id = conn["from"]["node_id"]
                source_output = conn["from"]["output"]
                target_input = conn["to"]["input"]

                # If we have results from the source node, add them to the context
                if source_node_id in self.node_results:
                    source_results = self.node_results[source_node_id]
                    if source_output in source_results:
                        node_context[target_input] = source_results[source_output]

        return node_context

    def _evaluate_condition(self, condition: str) -> bool:
        """
        Evaluate a condition expression for conditional node execution.
        Uses a safe evaluation approach to check conditions against the execution context.
        """
        try:
            # This is a simplified implementation - in production, you'd want a more robust
            # and secure expression evaluation system
            # For now, we'll support basic comparison expressions like "variable == value"

            # If condition contains variables from context, evaluate accordingly
            # This is a basic implementation that checks for simple patterns
            if "==" in condition:
                left, right = condition.split("==")
                left = left.strip()
                right = right.strip()

                # Remove quotes from right side if present
                if (right.startswith('"') and right.endswith('"')) or (right.startswith("'") and right.endswith("'")):
                    right = right[1:-1]

                # Check if variable exists in context
                if left in self.execution_context:
                    context_value = self.execution_context[left]
                    # For simplicity, assuming right side is a literal
                    try:
                        # Try to convert right to same type as context value
                        if isinstance(context_value, int):
                            right = int(right)
                        elif isinstance(context_value, float):
                            right = float(right)
                        elif isinstance(context_value, bool):
                            right = right.lower() == 'true'
                        # For other types, keep as string
                    except ValueError:
                        pass  # Keep as string if conversion fails

                    return context_value == right
                else:
                    # If variable doesn't exist in context, condition fails
                    return False
            elif ">" in condition:
                left, right = condition.split(">")
                left = left.strip()
                right = right.strip()

                if left in self.execution_context:
                    context_value = self.execution_context[left]
                    try:
                        right = float(right)
                        return float(context_value) > right
                    except (ValueError, TypeError):
                        return False
            elif "<" in condition:
                left, right = condition.split("<")
                left = left.strip()
                right = right.strip()

                if left in self.execution_context:
                    context_value = self.execution_context[left]
                    try:
                        right = float(right)
                        return float(context_value) < right
                    except (ValueError, TypeError):
                        return False
            # More complex conditions can be added as needed

            # For unsupported conditions, default to True to not block execution
            return True

        except Exception:
            logger.warning(f"Condition evaluation failed for: {condition}")
            return False
=======
>>>>>>> origin/main
