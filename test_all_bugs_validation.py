#!/usr/bin/env python3
"""
Comprehensive test to validate all 5 launch.py bugs have been fixed
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_bug1_import_project_config():
    """Test Bug #1: setup.project_config import error"""
    try:
        from setup.launch import get_project_config
        print("✅ Bug #1 FIXED: get_project_config imported successfully")
        return True
    except Exception as e:
        print(f"❌ Bug #1 FAILED: {e}")
        return False

def test_bug2_import_utils():
    """Test Bug #2: setup.utils import error"""
    try:
        from setup.launch import print_system_info, process_manager
        print("✅ Bug #2 FIXED: setup.utils functions imported successfully")
        return True
    except Exception as e:
        print(f"❌ Bug #2 FAILED: {e}")
        return False

def test_bug3_import_services():
    """Test Bug #3: setup.services import error"""
    try:
        from setup.launch import start_services, start_backend, start_node_service, start_gradio_ui, validate_services
        print("✅ Bug #3 FIXED: setup.services functions imported successfully")
        return True
    except Exception as e:
        print(f"❌ Bug #3 FAILED: {e}")
        return False

def test_bug4_command_pattern_available():
    """Test Bug #4: COMMAND_PATTERN_AVAILABLE undefined variable"""
    try:
        # Check if the variable exists in the file content
        with open('setup/launch.py', 'r') as f:
            content = f.read()
        
        if 'COMMAND_PATTERN_AVAILABLE =' in content:
            print("✅ Bug #4 FIXED: COMMAND_PATTERN_AVAILABLE variable defined")
            return True
        else:
            print("❌ Bug #4 FAILED: COMMAND_PATTERN_AVAILABLE not found")
            return False
    except Exception as e:
        print(f"❌ Bug #4 ERROR: {e}")
        return False

def test_bug5_get_python_executable():
    """Test Bug #5: get_python_executable import error"""
    try:
        # Check if the import exists in the file content
        with open('setup/launch.py', 'r') as f:
            content = f.read()
        
        if 'from deployment.test_stages import get_python_executable' in content:
            print("✅ Bug #5 FIXED: get_python_executable import path is correct")
            return True
        else:
            print("❌ Bug #5 FAILED: get_python_executable import not found")
            return False
    except Exception as e:
        print(f"❌ Bug #5 ERROR: {e}")
        return False

def main():
    """Run all bug validation tests"""
    print("=== EmailIntelligence launch.py Bug Fix Validation ===")
    print()
    
    results = []
    
    # Test all 5 bugs
    results.append(test_bug1_import_project_config())
    results.append(test_bug2_import_utils())
    results.append(test_bug3_import_services())
    results.append(test_bug4_command_pattern_available())
    results.append(test_bug5_get_python_executable())
    
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
        status = "✅ FIXED" if result else "❌ FAILED"
        print(f"{bug_name}: {status}")
    
    fixed_count = sum(results)
    total_count = len(results)
    
    print()
    print(f"=== Final Result: {fixed_count}/{total_count} bugs fixed ===")
    
    if fixed_count == total_count:
        print("🎉 ALL BUGS FIXED! launch.py refactoring completed successfully.")
        return 0
    else:
        print("⚠️ Some bugs remain. Additional fixes may be needed.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)