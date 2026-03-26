import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from src.core.workflow_engine import Node, Workflow, WorkflowRunner

# Create a large workflow to test performance of _calculate_cleanup_schedule
nodes = {}
connections = []
N = 200

for i in range(N):
    nodes[f"N{i}"] = Node(f"N{i}", f"Node {i}", lambda x: x, ["input"], ["output"])
    if i < N - 1:
        connections.append({"from": {"node_id": f"N{i}", "output": "output"}, "to": {"node_id": f"N{i+1}", "input": "input"}})

workflow = Workflow("perf_test", nodes, connections)
runner = WorkflowRunner(workflow)

execution_order = [f"N{i}" for i in range(N)]

start_time = time.time()
runner._calculate_cleanup_schedule(execution_order)
end_time = time.time()

print(f"Time taken (N={N}): {end_time - start_time:.4f} seconds")
