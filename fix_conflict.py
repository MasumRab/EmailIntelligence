import re

files_to_fix = [
    "src/core/performance_monitor.py"
]

for file_path in files_to_fix:
    with open(file_path, "r") as f:
        content = f.read()

    # Just a quick hack to remove the merge conflicts for tests to run
    content = re.sub(r'<<<<<<< HEAD.*?=======(.*?)>>>>>>>.*?\n', r'\1', content, flags=re.DOTALL)

    with open(file_path, "w") as f:
        f.write(content)
import glob

files_to_fix = [
    "src/core/data/__init__.py",
    "src/core/data/data_source.py",
    "src/core/auth.py",
    "src/core/settings.py",
    "src/core/models.py",
    "src/core/security.py"
]

for file_path in files_to_fix:
    try:
        with open(file_path, "r") as f:
            content = f.read()

        content = re.sub(r'<<<<<<< HEAD.*?=======(.*?)>>>>>>>.*?\n', r'\1', content, flags=re.DOTALL)

        with open(file_path, "w") as f:
            f.write(content)
    except:
        pass
