import re

file_path = "tests/test_launcher.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from launch import (", "from setup.launch import (")

with open(file_path, "w") as f:
    f.write(content)
