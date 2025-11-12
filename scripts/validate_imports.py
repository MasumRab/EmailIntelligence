#!/usr/bin/env python3
"""
Import validation script for CI/CD pipeline.

This script systematically attempts to import all core application modules
to detect import errors before they cause runtime failures.
"""

import sys
import importlib
from pathlib import Path
from typing import List

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Core modules to validate
CORE_MODULES = [
    'setup.test_stages',
    'setup.commands',
    'setup.container',
    'src.core.workflow_engine',
    'src.backend.python_backend.main',
]

def validate_imports(modules: List[str]) -> bool:
    """
    Validate that all specified modules can be imported.

    Args:
        modules: List of module names to import

    Returns:
        True if all imports succeed, False otherwise
    """
    failed_imports = []

    for module_name in modules:
        try:
            print(f"Importing {module_name}...")
            importlib.import_module(module_name)
            print(f"✓ Successfully imported {module_name}")
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {e}")
            failed_imports.append((module_name, str(e)))
        except Exception as e:
            print(f"✗ Unexpected error importing {module_name}: {e}")
            failed_imports.append((module_name, str(e)))

    if failed_imports:
        print(f"\n❌ Import validation failed! {len(failed_imports)} module(s) failed to import:")
        for module, error in failed_imports:
            print(f"  - {module}: {error}")
        return False
    else:
        print(f"\n✅ Import validation passed! All {len(modules)} modules imported successfully.")
        return True

def main() -> int:
    """Main entry point."""
    print("🔍 Starting import validation...")

    success = validate_imports(CORE_MODULES)

    if success:
        print("🎉 All imports validated successfully!")
        return 0
    else:
        print("💥 Import validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())