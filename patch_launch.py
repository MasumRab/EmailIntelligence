import re

with open("setup/launch.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the broken docstring
content = content.replace('This script provides a unified entry point', '"""\nThis script provides a unified entry point')

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.write(content)
