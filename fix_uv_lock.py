import re

with open('uv.lock', 'r') as f:
    content = f.read()

blocks = content.split('[[package]]\n')
new_blocks = [blocks[0]]

bandit_count = 0
for block in blocks[1:]:
    if block.startswith('name = "bandit"'):
        bandit_count += 1
        if bandit_count > 1:
            continue # skip duplicate
    new_blocks.append('[[package]]\n' + block)

with open('uv.lock', 'w') as f:
    f.write("".join(new_blocks))
