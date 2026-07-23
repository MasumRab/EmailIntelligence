import re

file_path = "src/backend/python_nlp/nlp_engine.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from backend.python_nlp.text_utils", "from src.backend.python_nlp.text_utils")

with open(file_path, "w") as f:
    f.write(content)
