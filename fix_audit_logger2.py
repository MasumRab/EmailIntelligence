import re

file_path = "src/core/audit_logger.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("except Exception:", "except queue.Empty:")

with open(file_path, "w") as f:
    f.write(content)
