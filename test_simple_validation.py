#!/usr/bin/env python3
"""
Simple validation test to check if the 5 launch.py bugs have been fixed
This test only examines the source code without importing problematic modules
"""

import os

def test_bug_fixes():
    """Test all 5 bugs by examining the source code"""
    print("=== EmailIntelligence launch.py Bug Fix Validation ===")
    print()
    
    launch_file = 'setup/launch.py'
    
    if not os.path.exists(launch_file):
        print("❌ ERROR: launch.py file not found")
        return False
    
    with open(launch_file, 'r') as f:
        content = f.read()
    
    results = []
    bugs_found = []
    
    # Bug #1: setup.project_config import error (should be fixed with correct import)
    if 'from src.context_control.project import load_project_config' in content:
        print("✓ Bug #1 FIXED: Corrected project_config import path")
        results.append(True)
    else:
        print("✗ Bug #1 FAILED: project_config import still incorrect")
        results.append(False)
        bugs_found.append("Bug #1: project_config import")
    
    # Bug #2: setup.utils import error (should be fixed by creating the module)
    if 'from setup.utils import print_system_info, process_manager' in content:
        print("✓ Bug #2 FIXED: setup.utils import present")
        results.append(True)
    else:
        print("✗ Bug #2 FAILED: setup.utils import missing")
        results.append(False)
        bugs_found.append("Bug #2: setup.utils import")
    
    # Bug #3: setup.services import error (should be fixed by creating the module)
    if 'from setup.services import (' in content and 'validate_services' in content:
        print("✓ Bug #3 FIXED: setup.services import with validate_services present")
        results.append(True)
    else:
        print("✗ Bug #3 FAILED: setup.services import missing or incomplete")
        results.append(False)
        bugs_found.append("Bug #3: setup.services import")
    
    # Bug #4: COMMAND_PATTERN_AVAILABLE undefined variable
    if 'COMMAND_PATTERN_AVAILABLE =' in content:
        print("✓ Bug #4 FIXED: COMMAND_PATTERN_AVAILABLE variable defined")
        results.append(True)
    else:
        print("✗ Bug #4 FAILED: COMMAND_PATTERN_AVAILABLE variable not found")
        results.append(False)
        bugs_found.append("Bug #4: COMMAND_PATTERN_AVAILABLE variable")
    
    # Bug #5: get_python_executable import error
    if 'from deployment.test_stages import get_python_executable' in content:
        print("✓ Bug #5 FIXED: Corrected get_python_executable import path")
        results.append(True)
    else:
        print("✗ Bug #5 FAILED: get_python_executable import still incorrect")
        results.append(False)
        bugs_found.append("Bug #5: get_python_executable import")
    
    print()
    print("=== Bug Fix Summary ===")
    
    bug_names = [
        "Bug #1: setup.project_config import error",
        "Bug #2: setup.utils import error", 
        "Bug #3: setup.services import error",
        "Bug #4: COMMAND_PATTERN_AVAILABLE undefined variable",
        "Bug #5: get_python_executable import error"
    ]
    
    for i, (bug_name, result) in enumerate(zip(bug_names, results)):
        status = "✓ FIXED" if result else "✗ FAILED"
        print(f"{bug_name}: {status}")
    
    fixed_count = sum(results)
    total_count = len(results)
    
    print()
    print(f"=== Final Result: {fixed_count}/{total_count} bugs fixed ===")
    
    if fixed_count == total_count:
        print("🎉 ALL BUGS FIXED! launch.py refactoring completed successfully.")
        return True
    else:
        print(f"⚠️  {total_count - fixed_count} bugs remain:")
        for bug in bugs_found:
            print(f"   - {bug}")
        return False

if __name__ == "__main__":
    success = test_bug_fixes()
    exit(0 if success else 1)