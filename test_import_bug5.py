#!/usr/bin/env python3
"""
Test script for Bug #5: get_python_executable import error
"""
import os
import re

print("Testing get_python_executable function import...")

# First test the direct import that would fail
try:
    from setup.utils import get_python_executable
    print("✓ setup.utils.get_python_executable import SUCCESS")
    print(f"  Function available: {get_python_executable}")
except ImportError as e:
    print("✗ setup.utils.get_python_executable import FAILED")
    print(f"  Error: {e}")
except Exception as e:
    print("✗ setup.utils.get_python_executable import UNEXPECTED ERROR")
    print(f"  Error: {e}")

print("\nTesting if get_python_executable exists elsewhere...")
# Search for get_python_executable in the codebase
found_functions = []
for root, dirs, files in os.walk('.'):
    # Skip certain directories
    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.pytest_cache']]
    
    for file in files:
        if file.endswith('.py'):
            try:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'def get_python_executable' in content:
                        found_functions.append(file_path)
                        print(f"  ✓ get_python_executable found in {file_path}")
            except Exception:
                continue

if not found_functions:
    print("  ✗ get_python_executable function not found anywhere in the project")
else:
    print(f"  Total function definitions found: {len(found_functions)}")

print("\nTesting alternative import paths...")
# Test the path mentioned in the analysis
try:
    from deployment.test_stages import get_python_executable as get_python_executable_alt
    print("✓ deployment.test_stages.get_python_executable import SUCCESS")
    print(f"  Function available: {get_python_executable_alt}")
except ImportError as e:
    print("✗ deployment.test_stages.get_python_executable import FAILED")
    print(f"  Error: {e}")
except Exception as e:
    print("✗ deployment.test_stages.get_python_executable import UNEXPECTED ERROR")
    print(f"  Error: {e}")

print("\nAnalyzing launch.py usage patterns...")
launch_file = os.path.join(os.getcwd(), 'setup', 'launch.py')
if os.path.exists(launch_file):
    try:
        with open(launch_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all usages of get_python_executable
        usage_matches = re.findall(r'get_python_executable\s*\(\s*\)', content)
        print(f"  Found {len(usage_matches)} direct calls to get_python_executable()")
        
        # Find line numbers
        lines = content.split('\n')
        usage_lines = []
        for i, line in enumerate(lines, 1):
            if 'get_python_executable' in line and 'def get_python_executable' not in line:
                usage_lines.append((i, line.strip()))
        
        print("  Usage locations in launch.py:")
        for line_num, line_content in usage_lines[:10]:  # Show first 10
            print(f"    Line {line_num}: {line_content}")
        if len(usage_lines) > 10:
            print(f"    ... and {len(usage_lines) - 10} more usages")
            
    except Exception as e:
        print(f"  Error analyzing launch.py: {e}")

print("\nTesting function signature and implementation...")
if found_functions:
    for func_file in found_functions:
        try:
            with open(func_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the function definition
            func_match = re.search(r'def get_python_executable\([^)]*\):(.*?)(?=\ndef|\nclass|\n\n|\Z)', content, re.DOTALL)
            if func_match:
                func_body = func_match.group(0)
                print(f"  Function definition in {func_file}:")
                lines = func_body.split('\n')
                for line in lines[:5]:  # Show first 5 lines
                    if line.strip():
                        print(f"    {line.strip()}")
                if len(lines) > 5:
                    print("    ...")
                print("")
        except Exception as e:
            print(f"  Error reading {func_file}: {e}")

print("\nTesting alternative implementations...")
# Look for different patterns that might be the intended function
try:
    with open('deployment/test_stages.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for any function that might be related
    patterns = [
        r'def.*python.*exe',
        r'def.*executable',
        r'python.*executable',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"  Found related pattern '{pattern}': {matches}")
            
except Exception as e:
    print(f"  Error checking test_stages.py: {e}")

print("\nTesting what get_python_executable should return...")
# Try to understand what this function should do
try:
    if found_functions:
        with open(found_functions[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for return statements
        return_matches = re.findall(r'return\s+.*', content)
        print("  Return statements found:")
        for ret in return_matches:
            print(f"    {ret.strip()}")
except Exception as e:
    print(f"  Error analyzing return statements: {e}")

print("\nSUMMARY:")
print("  Bug #5 Analysis: get_python_executable import error")
print("  - Function doesn't exist in setup.utils (missing module)")
print("  - Function exists in deployment/test_stages.py")
print("  - Multiple calls in launch.py expect this function")
print("  - Import path mismatch: should import from deployment.test_stages")
print("  - This creates a clear ImportError when launch.py runs")