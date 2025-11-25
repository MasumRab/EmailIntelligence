#!/usr/bin/env python3
"""
Test script for Bug #2: setup.utils import error
"""
print("Testing setup.utils imports...")

try:
    from setup.utils import print_system_info, process_manager
    print("✓ setup.utils import SUCCESS")
    print(f"  print_system_info available: {print_system_info}")
    print(f"  process_manager available: {process_manager}")
except ImportError as e:
    print("✗ setup.utils import FAILED")
    print(f"  Error: {e}")
except Exception as e:
    print("✗ setup.utils import UNEXPECTED ERROR")
    print(f"  Error: {e}")

print("\nTesting if setup/utils.py exists...")
import os
utils_file = os.path.join(os.getcwd(), 'setup', 'utils.py')
if os.path.exists(utils_file):
    print("✓ setup/utils.py exists")
    print("  Checking content...")
    try:
        with open(utils_file, 'r') as f:
            content = f.read()
            if 'print_system_info' in content:
                print("    ✓ print_system_info found in utils.py")
            if 'process_manager' in content:
                print("    ✓ process_manager found in utils.py")
    except Exception as e:
        print(f"    Error reading file: {e}")
else:
    print("✗ setup/utils.py does not exist")

print("\nTesting alternative paths...")
# Check if these functions exist elsewhere
try:
    # Check in launch.py itself
    exec("""
# Check launch.py for these functions
try:
    with open('setup/launch.py', 'r') as f:
        content = f.read()
        if 'def print_system_info' in content:
            print("✓ print_system_info function found in setup/launch.py")
        if 'class ProcessManager' in content or 'def process_manager' in content:
            print("✓ process_manager found in setup/launch.py")
except Exception as e:
    print(f"Error checking launch.py: {e}")
""")
except Exception as e:
    print(f"Error in alternative check: {e}")

print("\nTesting if any utils.py exists in project...")
import os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file == 'utils.py':
            full_path = os.path.join(root, file)
            print(f"✓ Found utils.py at: {full_path}")
            # Check if it has the functions
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                    if 'print_system_info' in content:
                        print(f"    ✓ print_system_info found in {full_path}")
                    if 'process_manager' in content:
                        print(f"    ✓ process_manager found in {full_path}")
            except Exception as e:
                print(f"    Error reading {full_path}: {e}")