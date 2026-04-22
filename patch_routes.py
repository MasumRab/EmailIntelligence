import re

with open("src/backend/python_backend/__init__.py", "r") as f:
    content = f.read()
content = re.sub(r'^(from \.models import \()', r'\1  # noqa: E402', content, flags=re.MULTILINE)
with open("src/backend/python_backend/__init__.py", "w") as f:
    f.write(content)

with open("src/core/auth.py", "r") as f:
    content = f.read()
content = content.replace("from enum import Enum", "from enum import Enum  # noqa: E402")
with open("src/core/auth.py", "w") as f:
    f.write(content)
