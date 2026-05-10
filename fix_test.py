import re

with open("tests/conftest.py", "r") as f:
    content = f.read()

content = re.sub(r'<<<<<<<.*?\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>>.*?\n', '', content)

with open("tests/conftest.py", "w") as f:
    f.write(content)
