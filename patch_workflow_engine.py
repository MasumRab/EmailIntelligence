filepath = "src/core/workflow_engine.py"
with open(filepath, "r") as f:
    content = f.read()

# Fix _build_node_context to handle dict connections if they aren't parsed into objects
method = """
    def _build_node_context(self, node_id: str) -> Dict[str, Any]:
        \"\"\"Helper method to build execution context for a node by mapping upstream outputs to inputs.\"\"\"
        context = {}
        # First add initial inputs for the workflow if this node takes them
        node = self.workflow.nodes[node_id]
        if self.execution_context:
            for input_name in node.inputs:
                if input_name in self.execution_context:
                    context[input_name] = self.execution_context[input_name]

        # Then map outputs from completed upstream nodes
        for conn in self.workflow.connections:
            # Handle both dict and object connection representations
            if isinstance(conn, dict):
                to_node = conn.get("to", {}).get("node_id")
                from_node = conn.get("from", {}).get("node_id")
                to_input = conn.get("to", {}).get("input")
                from_output = conn.get("from", {}).get("output")
            else:
                to_node = getattr(conn, "to_node", None)
                from_node = getattr(conn, "from_node", None)
                to_input = getattr(conn, "to_input", None)
                from_output = getattr(conn, "from_output", None)

            if to_node == node_id and from_node in self.node_results:
                context[to_input] = self.node_results[from_node].get(from_output)

        return context
"""
import re
content = re.sub(r'    def _run_sequential\(self, execution_order, cleanup_schedule\):', method[1:] + '\n    def _run_sequential(self, execution_order, cleanup_schedule):', content, count=1)

with open(filepath, "w") as f:
    f.write(content)
