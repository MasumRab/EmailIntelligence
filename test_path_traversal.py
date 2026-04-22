import sys
from pathlib import Path

workflows_dir = Path("workflows")
workflows_dir.mkdir(exist_ok=True)

filename = "../test.json"
filepath = workflows_dir / filename

print(f"Filepath: {filepath}")
print(f"Resolved: {filepath.resolve()}")
