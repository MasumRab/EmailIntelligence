import json

with open('/tmp/merge_tree_state.json', 'r') as f:
    state = json.load(f)

for pr in state:
    if 'depends_on' in pr:
        pr['blocked_by'] = pr.pop('depends_on')
    elif 'blocked_by' not in pr:
        pr['blocked_by'] = []

with open('/tmp/merge_tree_state.json', 'w') as f:
    json.dump(state, f, indent=2)

print("Updated schema to use 'blocked_by'.")
