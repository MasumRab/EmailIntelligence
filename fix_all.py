import os
import glob
import re

def fix_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "<<<<<<< HEAD" in content or "=======" in content:
            content = re.sub(r'<<<<<<<.*?\n', '', content)
            content = re.sub(r'=======\n', '', content)
            content = re.sub(r'>>>>>>>.*?\n', '', content)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed {filepath}")
    except Exception as e:
        pass

for root, dirs, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            fix_file(os.path.join(root, file))

for root, dirs, files in os.walk("tests"):
    for file in files:
        if file.endswith(".py"):
            fix_file(os.path.join(root, file))
