with open("src/core/workflow_engine.py", "r") as f:
    content = f.read()

import re

old_code = """        # For each node in the execution order, determine which previous nodes' results
        # are no longer needed after this node executes
        for i, node_id in enumerate(execution_order):
            # Check all previous nodes to see if their results are still needed
            for prev_node_id in execution_order[:i]:
                # Check if any subsequent nodes need the result from prev_node_id
                still_needed = False

                subsequent_nodes = set(execution_order[i + 1 :])

                # If there's an intersection between subsequent nodes and the target nodes
                # of the previous node, it means the result is still needed
                if node_targets.get(prev_node_id, set()).intersection(subsequent_nodes):
                    still_needed = True

                # If not still needed by any subsequent nodes, it can be cleaned up
                if not still_needed:
                    cleanup_schedule[node_id].append(prev_node_id)"""

new_code = """        # For each node in the execution order, determine which previous nodes' results
        # are no longer needed after this node executes
        for i, node_id in enumerate(execution_order):
            subsequent_nodes = set(execution_order[i + 1 :])
            # Check all previous nodes to see if their results are still needed
            for prev_node_id in execution_order[:i]:
                # Check if any subsequent nodes need the result from prev_node_id
                still_needed = False

                # If there's an intersection between subsequent nodes and the target nodes
                # of the previous node, it means the result is still needed
                if node_targets.get(prev_node_id, set()).intersection(subsequent_nodes):
                    still_needed = True

                # If not still needed by any subsequent nodes, it can be cleaned up
                if not still_needed:
                    cleanup_schedule[node_id].append(prev_node_id)"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("src/core/workflow_engine.py", "w") as f:
        f.write(content)
    print("Patch applied successfully")
else:
    print("Old code not found")
