
import time
from src.core.workflow_engine import Workflow, WorkflowRunner, Node

def create_dummy_node(id):
    return Node(
        node_id=id,
        name=f"Node {id}",
        operation=lambda x: x,
        inputs=[],
        outputs=["out"]
    )

def benchmark_cleanup_schedule(num_nodes=100):
    nodes = {}
    connections = []

    # Create a long chain: 0 -> 1 -> 2 ... -> N
    # This is a worst case for "check all subsequent nodes" if not careful,
    # but actually the current N^3 algo might be okayish for chain because "needed" is found quickly?
    # Let's try a dense graph or just a long chain.
    # In a chain: 0 is needed by 1. 1 is subsequent to 0.
    # When processing 1: 0 is needed by 1.
    # When processing 2: 0 is NOT needed by 2...N. So 0 cleaned up at 2?
    # Wait, current algo:
    # At node i:
    #   For prev in 0..i-1:
    #     For sub in i+1..N:
    #        check if prev connected to sub.

    # For a chain 0->1->2...
    # At i=50. prev=0. sub=51..100.
    # Is 0 connected to 51? No. 52? No.
    # It iterates all sub for all prev.
    # So it really is N^3.

    for i in range(num_nodes):
        node_id = f"node_{i}"
        nodes[node_id] = create_dummy_node(node_id)
        if i > 0:
            prev_id = f"node_{i-1}"
            connections.append({
                "from": {"node_id": prev_id, "output": "out"},
                "to": {"node_id": node_id, "input": "in"}
            })

    workflow = Workflow("Benchmark", nodes, connections)
    runner = WorkflowRunner(workflow)

    execution_order = [f"node_{i}" for i in range(num_nodes)]

    start = time.time()
    schedule = runner._calculate_cleanup_schedule(execution_order)
    end = time.time()

    print(f"Nodes: {num_nodes}, Time: {end - start:.4f}s")
    return end - start

if __name__ == "__main__":
    print("Benchmarking _calculate_cleanup_schedule...")
    benchmark_cleanup_schedule(100)
    benchmark_cleanup_schedule(200)
    benchmark_cleanup_schedule(300)
