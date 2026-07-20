import re

file_path = "src/core/auth.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from typing import Optional",
"""import logging
from typing import Optional""")

with open(file_path, "w") as f:
    f.write(content)
