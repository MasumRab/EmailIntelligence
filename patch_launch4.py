import re
with open("setup/launch.py", "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'\"\"\"Check for common setup issues and warn users\.\"\"\"', '    \"\"\"Check for common setup issues and warn users.\"\"\"', text)

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.write(text)
