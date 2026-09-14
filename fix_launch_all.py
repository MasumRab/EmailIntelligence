filepath = "setup/launch.py"
with open(filepath, "r") as f:
    content = f.read()

import re

# Fix list arguments
content = re.sub(r'subprocess.run\(\[([^\]]+)\]', r'subprocess.run([str(x) for x in [\1]]', content)
content = re.sub(r'\[str\(x\) for x in \[str\(x\) for x in', r'[str(x) for x in', content)

with open(filepath, "w") as f:
    f.write(content)
