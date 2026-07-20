import re

file_path = "tests/test_launcher.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("PYTHON_MAX_VERSION", "")
content = content.replace(", ,", ",")
content = content.replace("( ,", "(")
content = content.replace(", )", ")")

with open(file_path, "w") as f:
    f.write(content)
