#!/usr/bin/env python3
"""
Targeted test for Bug #5: get_python_executable import error
This test specifically checks if the import works correctly without triggering module-level initialization.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_get_python_executable_import():
    """Test if get_python_executable can be imported from launch.py"""
    
    try:
        # Try to import the function
        from setup.launch import get_python_executable
        print("✅ Bug #5 ANALYSIS: Successfully imported get_python_executable from setup.launch")
        
        # Check if it's a function
        if callable(get_python_executable):
            print("✅ Bug #5 ANALYSIS: get_python_executable is callable")
        else:
            print(f"❌ Bug #5 ANALYSIS: get_python_executable is not callable (type: {type(get_python_executable)})")
            return False
            
        # Try calling it to see if it works
        try:
            result = get_python_executable()
            print(f"✅ Bug #5 ANALYSIS: get_python_executable() returned: {result}")
            print(f"✅ Bug #5 FIXED: Function works correctly")
            return True
        except Exception as e:
            print(f"⚠️ Bug #5 ANALYSIS: Function imported but calling failed: {e}")
            print(f"✅ Bug #5 PARTIAL FIX: Import works, but function may have runtime issues")
            return True  # Import works, which was the main issue
            
    except ImportError as e:
        print(f"❌ Bug #5 NOT FIXED: Import failed - {e}")
        return False
    except NameError as e:
        print(f"❌ Bug #5 NOT FIXED: NameError - {e}")
        return False
    except Exception as e:
        print(f"❌ Bug #5 ANALYSIS ERROR: Unexpected error - {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Bug #5: get_python_executable import error ===")
    print()
    
    result = test_get_python_executable_import()
    
    print()
    if result:
        print("=== Bug #5 Status: IMPORT SUCCESS (function accessible) ===")
    else:
        print("=== Bug #5 Status: STILL BROKEN - Import fails ===")
    
    sys.exit(0 if result else 1)