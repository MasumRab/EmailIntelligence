#!/usr/bin/env python3
"""
Test script for Secure Merge Task Manager
"""

import os
import sys
import yaml
from pathlib import Path

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        # Test main module
        import secure_merge_task_manager
        print("✓ Main module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import main module: {e}")
        return False
    
    try:
        # Test validation module
        import validation_security
        print("✓ Validation module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import validation module: {e}")
        return False
    
    try:
        # Test logging module
        import logging_audit
        print("✓ Logging module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import logging module: {e}")
        return False
    
    try:
        # Test config module
        import config_validation
        print("✓ Config module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config module: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from config_validation import ConfigManager
        config_manager = ConfigManager("merge_config.yaml")
        print("✓ Configuration loaded successfully")
        
        # Test getting a config value
        max_size = config_manager.get("security.max_file_size_mb")
        print(f"✓ Config value retrieved: max_file_size_mb = {max_size}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_sample_task():
    """Test sample task configuration."""
    print("\nTesting sample task configuration...")
    
    try:
        with open("sample_task.yaml", 'r') as f:
            task_config = yaml.safe_load(f)
        
        required_fields = ["source_branch", "target_branch", "task_id"]
        for field in required_fields:
            if field not in task_config:
                print(f"✗ Missing required field in sample task: {field}")
                return False
        
        print("✓ Sample task configuration is valid")
        print(f"  - Task ID: {task_config['task_id']}")
        print(f"  - Source Branch: {task_config['source_branch']}")
        print(f"  - Target Branch: {task_config['target_branch']}")
        
        return True
    except Exception as e:
        print(f"✗ Sample task test failed: {e}")
        return False

def test_directory_structure():
    """Test that required directories exist."""
    print("\nTesting directory structure...")
    
    required_files = [
        "secure_merge_task_manager.py",
        "validation_security.py", 
        "logging_audit.py",
        "config_validation.py",
        "README.md",
        "merge_config.yaml",
        "sample_task.yaml"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("Running tests for Secure Merge Task Manager...\n")
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Sample Task", test_sample_task),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
        if test_func():
            print(f"\n✓ {test_name} PASSED")
            passed += 1
        else:
            print(f"\n✗ {test_name} FAILED")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 All tests passed! The Secure Merge Task Manager is ready for use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    # Change to the scripts directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    sys.exit(main())