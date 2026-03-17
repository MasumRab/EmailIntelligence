#!/usr/bin/env python3
"""
update_references.py - Update file references after path changes

Usage:
    python3 update_references.py <old_pattern> <new_pattern> <file_pattern>

Example:
    python3 update_references.py "from src.context_control.core" "from src.context_control.agent_context" "src/**/*.py"
    python3 update_references.py "backend/python_backend" "src/backend/python_backend" "**/*.py"
"""

import subprocess
import sys
from pathlib import Path
from typing import List


def update_file_references(file_path: str, old_pattern: str, new_pattern: str) -> bool:
    """Update all occurrences of old_pattern to new_pattern in a file"""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content = content.replace(old_pattern, new_pattern)

        if content != updated_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return True
    except Exception as e:
        print(f"  ❌ Failed: {file_path} - {e}")

    return False


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python3 update_references.py <old_pattern> <new_pattern> <file_pattern>"
        )
        print("")
        print("Arguments:")
        print("  old_pattern - Pattern to find (e.g., 'from src.core')")
        print("  new_pattern - Pattern to replace with (e.g., 'from core')")
        print("  file_pattern - File pattern to search (e.g., 'src/**/*.py')")
        print("")
        print("Example:")
        print(
            '  python3 update_references.py "from src.context_control.core" "from src.context_control.agent_context" "src/**/*.py"'
        )
        print("")
        print("Note: Use quotes for patterns with spaces")
        sys.exit(1)

    old_pattern = sys.argv[1]
    new_pattern = sys.argv[2]
    file_pattern = sys.argv[3]

    print("=" * 60)
    print("Reference Updater")
    print("=" * 60)
    print(f"Old pattern: {old_pattern}")
    print(f"New pattern: {new_pattern}")
    print(f"Files: {file_pattern}")
    print("")

    # Build file list
    print("Finding files...")

    # Convert glob pattern to pathlib pattern
    if "**/" in file_pattern:
        # Recursive search
        pattern_parts = file_pattern.replace("**/", "").split("*")
        base_dir = Path(".")
        if pattern_parts[0]:
            base_dir = base_dir / pattern_parts[0].rstrip("/")

        if base_dir.exists() and base_dir.is_dir():
            py_files = list(base_dir.rglob("*.py"))
        else:
            py_files = list(Path(".").rglob("*.py"))
    elif "*" in file_pattern:
        # Simple glob
        py_files = list(Path(".").glob(file_pattern))
    else:
        # Specific file
        py_files = [Path(file_pattern)]

    # Filter out unwanted directories
    filtered_files = []
    for py_file in py_files:
        if "venv" in py_file.parts or "__pycache__" in py_file.parts:
            continue
        if py_file.suffix != ".py":
            continue
        filtered_files.append(py_file)

    print(f"Found {len(filtered_files)} Python files to check")
    print("")

    # Update references
    print("Updating references...")
    updated_count = 0
    found_count = 0

    for py_file in filtered_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            if old_pattern in content:
                found_count += 1
                if update_file_references(str(py_file), old_pattern, new_pattern):
                    updated_count += 1
                    print(f"  ✅ Updated: {py_file}")
        except Exception as e:
            print(f"  ❌ Error: {py_file} - {e}")

    print("")
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Files containing pattern: {found_count}")
    print(f"Files updated: {updated_count}")
    print("")

    if updated_count > 0:
        print("✅ Updates complete!")
        print("Next steps:")
        print("1. Review changes: git diff")
        print("2. Run import audit: python3 import_audit.py .")
        print("3. Test imports: python -c 'from module import *'")
    else:
        print("⚠️ No files were updated.")
        print("Possible reasons:")
        print("- Pattern not found in any files")
        print("- Files already have new pattern")
        print("- Pattern includes special characters that need escaping")

    print("")


if __name__ == "__main__":
    main()
