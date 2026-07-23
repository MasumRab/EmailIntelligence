import re

file_path = "src/core/factory.py"
with open(file_path, "r") as f:
    content = f.read()

content += """
def get_ai_engine(*args, **kwargs): pass
"""

with open(file_path, "w") as f:
    f.write(content)
