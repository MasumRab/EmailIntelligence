from typing import Any, Dict, List
from .node_base import BaseNode, ExecutionContext

class Workflow:
    def __init__(self, name: str, nodes: List[BaseNode], connections: List[Dict[str, Any]]):
        self.name = name
        self.nodes = {node.node_id: node for node in nodes}
        self.connections = connections

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # A simple implementation to deserialize a workflow from a dict
        # This will need to be more robust in a real application
        from .email_nodes import EmailSourceNode, FilterNode  # Import here to avoid circular dependency

        nodes = []
        for node_data in data.get("nodes", []):
            node_type = node_data.get("node_type")
            if node_type == "EmailSourceNode":
                nodes.append(EmailSourceNode(node_id=node_data.get("node_id"), config=node_data.get("config")))
            elif node_type == "FilterNode":
                nodes.append(FilterNode(node_id=node_data.get("node_id"), config=node_data.get("config")))

        return cls(data.get("name", "Untitled Workflow"), nodes, data.get("connections", []))

class WorkflowEngine:
    def __init__(self):
        self.node_types = {}

    def register_node_type(self, node_class):
        self.node_types[node_class.__name__] = node_class

    async def execute_workflow(self, workflow: Workflow, initial_inputs: Dict[str, Any], context: ExecutionContext) -> Dict[str, Any]:
        results = {}
        # This is a simplified execution model that assumes a linear workflow
        # A real implementation would need to handle complex graphs

        # Sort nodes by their connections to create a simple execution order
        # This is a naive approach and will not work for complex graphs
        sorted_nodes = []
        node_ids = list(workflow.nodes.keys())

        while len(sorted_nodes) < len(node_ids):
            for node_id in node_ids:
                if node_id in [n.node_id for n in sorted_nodes]:
                    continue

                is_ready = True
                for conn in workflow.connections:
                    if conn['target_node_id'] == node_id:
                        if conn['source_node_id'] not in [n.node_id for n in sorted_nodes]:
                            is_ready = False
                            break

                if is_ready:
                    sorted_nodes.append(workflow.nodes[node_id])

        for node in sorted_nodes:
            inputs = {}
            for conn in workflow.connections:
                if conn['target_node_id'] == node.node_id:
                    source_node_id = conn['source_node_id']
                    source_port = conn['source_port']
                    target_port = conn['target_port']
                    if source_node_id in results:
                        inputs[target_port] = results[source_node_id].get(source_port)

            node.inputs = inputs
            result = await node.execute(context)
            results[node.node_id] = result

        return results

workflow_engine = WorkflowEngine()
