#!/usr/bin/env python3
import sys
import subprocess
try:
    files = subprocess.check_output(["git", "diff", "--cached", "--name-only"]).decode().splitlines()
    for file in files:
        if "check_deprecated" in file or not file:
            continue
        content = subprocess.check_output(["git", "show", f":{file}"]).decode().lower()
        if "deprecated" in content:
            print(f"ERROR: The term deprecated was found in {file}.")
            print("Please use Legacy Component - Maintained for Backward Compatibility instead.")
            sys.exit(1)
except subprocess.CalledProcessError:
    pass
sys.exit(0)
