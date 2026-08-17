with open("uv.lock", "r") as f:
    text = f.read()

import re

# Let's count actual package definitions of bandit
parts = text.split('[[package]]\n')
new_parts = [parts[0]]

bandit_count = 0
for part in parts[1:]:
    if part.startswith('name = "bandit"'):
        bandit_count += 1
        if bandit_count > 1:
            print("Skipping duplicate bandit package")
            continue
    new_parts.append(part)

with open("uv.lock", "w") as f:
    f.write('[[package]]\n'.join(new_parts))
