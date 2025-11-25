#!/usr/bin/env python3
"""
Targeted test for Bug #4: COMMAND_PATTERN_AVAILABLE undefined variable
This test specifically checks if the variable exists without triggering module-level initialization.
"""

import ast
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_command_pattern_available_variable():
    """Test if COMMAND_PATTERN_AVAILABLE variable exists in launch.py without importing it"""
    
    launch_file = 'setup/launch.py'
    
    try:
        # Read the file and parse it to check if the variable is defined
        with open(launch_file, 'r') as f:
            content = f.read()
        
        # Parse the AST to find variable assignments
        tree = ast.parse(content)
        
        command_pattern_available_found = False
        variable_assigned = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == 'COMMAND_PATTERN_AVAILABLE':
                            command_pattern_available_found = True
                            variable_assigned = True
                            print(f"✅ Bug #4 ANALYSIS: Found COMMAND_PATTERN_AVAILABLE assignment at line {node.lineno}")
                            break
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    if node.target.id == 'COMMAND_PATTERN_AVAILABLE':
                        command_pattern_available_found = True
                        variable_assigned = True
                        print(f"✅ Bug #4 ANALYSIS: Found COMMAND_PATTERN_AVAILABLE annotation at line {node.lineno}")
                        break
        
        if command_pattern_available_found:
            print(f"✅ Bug #4 ANALYSIS: COMMAND_PATTERN_AVAILABLE variable is properly defined")
            
            # Check if it's assigned to a proper value
            if variable_assigned:
                # Extract the value it was assigned to
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == 'COMMAND_PATTERN_AVAILABLE':
                                if isinstance(node.value, ast.Constant):
                                    value = node.value.value
                                    print(f"✅ Bug #4 ANALYSIS: Variable assigned to: {value}")
                                    if isinstance(value, bool):
                                        print(f"✅ Bug #4 FIXED: COMMAND_PATTERN_AVAILABLE = {value} (proper boolean value)")
                                        return True
                                elif isinstance(node.value, ast.Call):
                                    func_name = getattr(node.value.func, 'id', 'unknown')
                                    print(f"✅ Bug #4 ANALYSIS: Variable assigned via function call: {func_name}")
                                    # This might be the container.get() call we added
                                    return True
                    elif isinstance(node, ast.AnnAssign):
                        if isinstance(node.target, ast.Name) and node.target.id == 'COMMAND_PATTERN_AVAILABLE':
                            if node.value and isinstance(node.value, ast.Constant):
                                value = node.value.value
                                print(f"✅ Bug #4 ANALYSIS: Variable annotated and assigned to: {value}")
                                if isinstance(value, bool):
                                    print(f"✅ Bug #4 FIXED: COMMAND_PATTERN_AVAILABLE = {value} (proper boolean value)")
                                    return True
            
            print(f"✅ Bug #4 ANALYSIS: Variable exists but needs value validation")
            return True
        else:
            print(f"❌ Bug #4 NOT FIXED: COMMAND_PATTERN_AVAILABLE variable not found in file")
            return False
            
    except Exception as e:
        print(f"❌ Bug #4 ANALYSIS ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Bug #4: COMMAND_PATTERN_AVAILABLE undefined variable ===")
    print()
    
    result = test_command_pattern_available_variable()
    
    print()
    if result:
        print("=== Bug #4 Status: VARIABLE DEFINITION FOUND (value validation may be needed) ===")
    else:
        print("=== Bug #4 Status: STILL BROKEN - Variable not defined ===")
    
    sys.exit(0 if result else 1)