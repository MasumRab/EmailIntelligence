import re

with open('uv.lock', 'r') as f:
    content = f.read()

pattern = r'\[\[package\]\]\nname = "bandit".*?(?=\n\[\[package\]\]|\Z)'
blocks = re.finditer(pattern, content, re.DOTALL)

blocks = list(blocks)
if len(blocks) > 1:
    start_pos = blocks[1].start()
    end_pos = blocks[-1].end()

    new_content = content[:start_pos] + content[end_pos:]

    with open('uv.lock', 'w') as f:
        f.write(new_content)
