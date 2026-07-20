import os
import glob

def fix_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    content = content.replace("from backend.python_backend", "from src.backend.python_backend")
    content = content.replace("from backend.python_nlp", "from src.backend.python_nlp")

    with open(file_path, "w") as f:
        f.write(content)

for py_file in glob.glob("tests/**/*.py", recursive=True):
    fix_file(py_file)
