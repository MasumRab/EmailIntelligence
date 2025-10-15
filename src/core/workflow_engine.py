import logging
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class Node:
    """
    Represents a single node in a processing workflow.

    Each node encapsulates a specific operation, such as fetching an email,
    analyzing its sentiment, or applying a category. Nodes define their
    required inputs and the outputs they produce.
    """

    def __init__(
        self, node_id: str, name: str, operation: Callable, inputs: List[str], outputs: List[str]
    ):
        self.node_id = node_id
        self.name = name
        self.operation = operation
        self.inputs = inputs
        self.outputs = outputs

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the node's operation using the provided context.
        """
        try:
            # Prepare the arguments for the operation from the context
            args = [context[key] for key in self.inputs]

            # Execute the operation
            result = self.operation(*args)

            # If the node produces multiple outputs, we expect the operation
            # to return a tuple. Otherwise, a single value.
            if len(self.outputs) == 1:
                return {self.outputs[0]: result}
            else:
                return {name: value for name, value in zip(self.outputs, result)}

        except Exception as e:
            logger.error(f"Error executing node '{self.name}' ({self.node_id}): {e}", exc_info=True)
            raise


class Workflow:
    """
    Represents a processing workflow as a directed acyclic graph (DAG) of nodes.
    """

    def __init__(self, name: str, nodes: Dict[str, Node], connections: Dict[str, str]):
        self.name = name
        self.nodes = nodes
        self.connections = connections  # Maps an input of a node to an output of another


class WorkflowRunner:
    """
    Executes a workflow by processing its nodes in the correct topological order.

    This is a placeholder for the full implementation. The actual runner will
    need to perform a topological sort of the nodes and manage the execution
    context, passing data between nodes as defined by the workflow's connections.
    """

    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.execution_context = {}

    def run(self, initial_context: Dict[str, Any]):
        """
        Executes the workflow.

        This is a simplified implementation. A real implementation would involve
        a topological sort of the nodes to determine the execution order.
        """
        logger.info(f"Running workflow: {self.workflow.name}")
        self.execution_context.update(initial_context)

        # This is a placeholder and does not represent the final implementation.
        # A real implementation would need to handle the graph traversal.
        for node_id, node in self.workflow.nodes.items():
            logger.info(f"Executing node: {node.name}")

            # This is a naive implementation that assumes the context is already populated.
            # A real implementation would use the `connections` to map outputs to inputs.
            try:
                results = node.execute(self.execution_context)
                self.execution_context.update(results)
            except Exception as e:
                logger.error(f"Workflow execution failed at node '{node.name}'.")
                return {"error": f"Failed at node {node.name}: {e}"}

        logger.info("Workflow execution completed.")
        return self.execution_context
