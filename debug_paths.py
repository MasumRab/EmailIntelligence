import os
import fnmatch
import re

def check():
    path = "src/main.py"
    abs_path = os.path.realpath(path)
    print(f"Original: {path}")
    print(f"Absolute: {abs_path}")

    patterns = ["src/*.py"]
    regex_parts = [fnmatch.translate(p) for p in patterns]
    print(f"Regex parts: {regex_parts}")

    combined = "|".join(regex_parts)
    print(f"Combined regex: {combined}")

    pattern = re.compile(combined)

    print(f"Match original: {pattern.match(path)}")
    print(f"Match absolute: {pattern.match(abs_path)}")
    print(f"Match basename: {pattern.match(os.path.basename(path))}")

if __name__ == "__main__":
    check()
