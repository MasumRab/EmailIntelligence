import re

with open("tests/test_auth.py", "r") as f:
    content = f.read()

if "from src.main import app" not in content:
    content = content.replace("from src.main import create_app", "from src.main import app")

with open("tests/test_auth.py", "w") as f:
    f.write(content)
