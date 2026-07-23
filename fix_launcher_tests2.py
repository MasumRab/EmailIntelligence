import re

file_path = "tests/test_launcher.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from launch import (\n    \n    ,\n    verify_environment,\n    PYTHON_MIN_VERSION\n)", "from launch import (\n    verify_environment,\n    PYTHON_MIN_VERSION\n)")

with open(file_path, "w") as f:
    f.write(content)
