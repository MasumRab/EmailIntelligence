with open("src/core/workflow_engine.py", "r") as f:
    content = f.read()

import re

# Resolve remaining python file conflicts
content = re.sub(r'<<<<<<<.*?\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>>.*?\n', '', content)

with open("src/core/workflow_engine.py", "w") as f:
    f.write(content)

with open("src/main.py", "r") as f:
    content = f.read()

content = re.sub(r'<<<<<<<.*?\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>>.*?\n', '', content)

with open("src/main.py", "w") as f:
    f.write(content)
