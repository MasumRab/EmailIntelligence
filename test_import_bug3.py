#!/usr/bin/env python3
"""
Test script for Bug #3: setup.services import error
"""
print("Testing setup.services imports...")

try:
    from setup.services import (
        start_services, start_backend, start_node_service, start_gradio_ui, validate_services
    )
    print("✓ setup.services import SUCCESS")
    print(f"  start_services available: {start_services}")
    print(f"  start_backend available: {start_backend}")
    print(f"  start_node_service available: {start_node_service}")
    print(f"  start_gradio_ui available: {start_gradio_ui}")
    print(f"  validate_services available: {validate_services}")
except ImportError as e:
    print("✗ setup.services import FAILED")
    print(f"  Error: {e}")
except Exception as e:
    print("✗ setup.services import UNEXPECTED ERROR")
    print(f"  Error: {e}")

print("\nTesting if setup/services.py exists...")
import os
services_file = os.path.join(os.getcwd(), 'setup', 'services.py')
if os.path.exists(services_file):
    print("✓ setup/services.py exists")
    print("  Checking content...")
    try:
        with open(services_file, 'r', encoding='utf-8') as f:
            content = f.read()
            functions = ['start_services', 'start_backend', 'start_node_service', 'start_gradio_ui', 'validate_services']
            for func in functions:
                if f'def {func}' in content:
                    print(f"    ✓ {func} found in services.py")
                elif func in content:
                    print(f"    ⚠ {func} mentioned but not as function definition in services.py")
    except Exception as e:
        print(f"    Error reading file: {e}")
else:
    print("✗ setup/services.py does not exist")

print("\nTesting if functions exist inline in setup/launch.py...")
try:
    with open('setup/launch.py', 'r', encoding='utf-8') as f:
        content = f.read()
        functions = ['start_services', 'start_backend', 'start_node_service', 'start_gradio_ui', 'validate_services']
        found_functions = []
        for func in functions:
            if f'def {func}' in content:
                found_functions.append(func)
                print(f"    ✓ {func} found as function definition in setup/launch.py")
        
        if found_functions:
            print(f"  Found {len(found_functions)} functions inline in launch.py")
        else:
            print("  ✗ No service functions found in launch.py")
except Exception as e:
    print(f"  Error reading launch.py: {e}")

print("\nTesting if setup/commands directory has related functionality...")
commands_dir = os.path.join(os.getcwd(), 'setup', 'commands')
if os.path.exists(commands_dir):
    print("✓ setup/commands directory exists")
    files = os.listdir(commands_dir)
    print(f"  Files in commands/: {files}")
    
    # Check if any commands might be related to services
    for file in files:
        if file.endswith('.py') and 'service' in file.lower():
            print(f"    ⚠ Potentially related file: {file}")
else:
    print("✗ setup/commands directory does not exist")

print("\nSearching for service-related functions in project...")
found_anywhere = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            try:
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    functions = ['start_services', 'start_backend', 'start_node_service', 'start_gradio_ui', 'validate_services']
                    for func in functions:
                        if f'def {func}' in content:
                            full_path = os.path.join(root, file)
                            found_anywhere.append((func, full_path))
                            print(f"    ✓ {func} found in {full_path}")
            except Exception:
                continue

if not found_anywhere:
    print("    ✗ No service functions found anywhere in the project")
else:
    print(f"  Total functions found: {len(found_anywhere)}")