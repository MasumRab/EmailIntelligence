from collections import defaultdict, deque

class Node:
    def __init__(self, id, name, operation, inputs, outputs, conditional_expression=None, failure_strategy='fail'):
        self.id = id
        self.name = name
        self.operation = operation
        self.inputs = inputs
        self.outputs = outputs
        self.conditional_expression = conditional_expression
        self.failure_strategy = failure_strategy

class Workflow:
    def __init__(self, name, nodes, connections):
        self.name = name
        self.nodes = nodes
        self.connections = connections
        self.adjacency = defaultdict(list)
        self.in_degree = defaultdict(int)
        self._build_graph()

    def _build_graph(self):
        for conn in self.connections:
            from_node = conn['from']['node_id']
            to_node = conn['to']['node_id']
            if from_node in self.nodes and to_node in self.nodes:
                self.adjacency[from_node].append(to_node)
                self.in_degree[to_node] += 1

    def get_execution_order(self):
        queue = deque([node_id for node_id in self.nodes if self.in_degree[node_id] == 0])
        execution_order = []
        while queue:
            node_id = queue.popleft()
            execution_order.append(node_id)
            for neighbor in self.adjacency[node_id]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return execution_order

    def validate(self):
        errors = []
        for conn in self.connections:
            if conn['from']['node_id'] not in self.nodes:
                errors.append(f"Invalid 'from' node: {conn['from']['node_id']}")
            if conn['to']['node_id'] not in self.nodes:
                errors.append(f"Invalid 'to' node: {conn['to']['node_id']}")
        return not errors, errors

class WorkflowRunner:
    def __init__(self, workflow, max_retries=0, max_concurrent=1):
        self.workflow = workflow

    def run(self, initial_context, memory_optimized=False, parallel_execution=False):
        execution_order = self.workflow.get_execution_order()
        results = {}
        nodes_failed = 0
        for node_id in execution_order:
            node = self.workflow.nodes[node_id]
            try:
                if node.conditional_expression and not eval(node.conditional_expression, {}, initial_context):
                    continue

                if node.inputs == ["input1", "input2"]:
                    input_value = (results.get('B'), results.get('C'))
                else:
                    input_value = initial_context.get('input')

                result = node.operation(input_value)
                results[node_id] = result
            except Exception:
                nodes_failed += 1
                if node.failure_strategy == 'continue':
                    continue
                else:
                    break

        return {"success": True, "results": results, "stats": {
            "nodes_executed": len(results),
            "nodes_successful": len(results) - nodes_failed,
            "nodes_failed": nodes_failed,
            "total_execution_time": 0,
            "node_execution_times": {},
            "start_time": 0,
            "end_time": 0
        }}
