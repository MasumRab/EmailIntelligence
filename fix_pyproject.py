import re

with open("pyproject.toml", "r") as f:
    content = f.read()

# Make sure all merge conflicts are resolved properly
content = re.sub(r'<<<<<<<.*?\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>>.*?\n', '', content)

with open("pyproject.toml", "w") as f:
    f.write(content)

with open("setup/pyproject.toml", "r") as f:
    content = f.read()

content = re.sub(r'<<<<<<<.*?\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>>.*?\n', '', content)

with open("setup/pyproject.toml", "w") as f:
    f.write(content)
