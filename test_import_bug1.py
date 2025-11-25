#!/usr/bin/env python3
"""
Test script for Bug #1: setup.project_config import error
"""
print("Testing setup.project_config import...")

try:
    from setup.project_config import get_project_config
    print("✓ setup.project_config import SUCCESS")
    print(f"  Function available: {get_project_config}")
except ImportError as e:
    print(f"✗ setup.project_config import FAILED")
    print(f"  Error: {e}")
except Exception as e:
    print(f"✗ setup.project_config import UNEXPECTED ERROR")
    print(f"  Error: {e}")

print("\nTesting alternative import path...")
try:
    from src.context_control.project import load_project_config
    print("✓ src.context_control.project.load_project_config import SUCCESS")
    print(f"  Function available: {load_project_config}")
except ImportError as e:
    print(f"✗ src.context_control.project import FAILED")
    print(f"  Error: {e}")
except Exception as e:
    print(f"✗ src.context_control.project import UNEXPECTED ERROR")
    print(f"  Error: {e}")

print("\nTesting if setup/ directory exists...")
import os
setup_dir = os.path.join(os.getcwd(), 'setup')
if os.path.exists(setup_dir):
    print("✓ setup/ directory exists")
    files = os.listdir(setup_dir)
    print(f"  Files in setup/: {files}")
else:
    print("✗ setup/ directory does not exist")

print("\nTesting if src/context_control/project.py exists...")
src_dir = os.path.join(os.getcwd(), 'src', 'context_control')
project_file = os.path.join(src_dir, 'project.py')
if os.path.exists(project_file):
    print("✓ src/context_control/project.py exists")
else:
    print("✗ src/context_control/project.py does not exist")
    if os.path.exists(src_dir):
        print(f"  Files in src/context_control/: {os.listdir(src_dir)}")
    else:
        print("  src/context_control/ directory does not exist")