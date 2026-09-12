#!/usr/bin/env python3
"""
Dependency Management Validation Script

This script validates that the project uses consistent dependency management
and prevents mixed usage of uv and Poetry.
"""

import os
import sys
from pathlib import Path

def validate_dependency_management():
    """Validate that only uv is used for dependency management."""
    project_root = Path(__file__).parent
    errors = []

    # Check for Poetry files
    poetry_files = [
        "poetry.lock",
        "poetry.toml",
    ]

    for poetry_file in poetry_files:
        if (project_root / poetry_file).exists():
            errors.append(f"Found Poetry file: {poetry_file}. This project uses uv for dependency management.")

    # Check for uv.lock (should exist)
    uv_lock = project_root / "uv.lock"
    if not uv_lock.exists():
        errors.append("Missing uv.lock file. Run 'uv sync' to generate it.")

    # Check pyproject.toml exists
    pyproject_toml = project_root / "pyproject.toml"
    if not pyproject_toml.exists():
        errors.append("Missing pyproject.toml file.")

    if errors:
        print("❌ Dependency management validation failed:")
        for error in errors:
            print(f"  - {error}")
        print("\n🔧 To fix:")
        print("  - Remove Poetry files: rm poetry.lock poetry.toml")
        print("  - Generate uv lock: uv sync")
        return False

    print("✅ Dependency management validation passed.")
    print("  - Using uv for dependency management")
    print("  - uv.lock file present")
    print("  - No Poetry files found")
    return True

if __name__ == "__main__":
    success = validate_dependency_management()
    sys.exit(0 if success else 1)
