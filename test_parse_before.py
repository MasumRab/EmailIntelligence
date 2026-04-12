import ast
import os
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r") as f:
                    ast.parse(f.read())
            except Exception as e:
                print(f"Error parsing {path}: {e}")
