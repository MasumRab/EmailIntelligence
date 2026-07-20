import re

file_path = "tests/test_launcher.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from launch import (\n    ,\n    PYTHON_MIN_VERSION,", "from launch import (\n    PYTHON_MIN_VERSION,")

with open(file_path, "w") as f:
    f.write(content)
