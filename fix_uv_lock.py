import re

with open('uv.lock', 'r') as f:
    content = f.read()

# Find all package blocks
blocks = re.split(r'\n(?=\[\[package\]\])', content)

new_blocks = []
bandit_count = 0

for block in blocks:
    if 'name = "bandit"' in block and 'version =' in block:
        if bandit_count == 0:
            new_blocks.append(block)
        bandit_count += 1
    else:
        new_blocks.append(block)

with open('uv.lock', 'w') as f:
    f.write('\n'.join(new_blocks))
