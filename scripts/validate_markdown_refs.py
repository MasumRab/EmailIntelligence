#!/usr/bin/env python3
"""
Validate markdown file references in task documentation.
Checks that referenced files actually exist.
"""

import os
import re
import sys
from pathlib import Path


def find_markdown_references(content: str) -> list[str]:
    """Find markdown file references in content."""
    # Match patterns like `task-001-1.md` or [Link Text](task-001.md)
    pattern = r"(?:``|`)?(?:task-\d+(?:-\d+(?:-\d+)?)?\.md)(?:``)?"
    matches = re.findall(pattern, content, re.IGNORECASE)
    # Clean up backticks
    return [m.strip("`").strip() for m in matches]


def validate_references(base_dir: str) -> tuple[int, int]:
    """Validate all markdown file references in task files."""
    base_path = Path(base_dir)
    errors = []

    for md_file in sorted(base_path.glob("task-*.md")):
        content = md_file.read_text()
        refs = find_markdown_references(content)

        for ref in refs:
            ref_path = base_path / ref
            if not ref_path.exists():
                errors.append(f"{md_file.name}: references '{ref}' which does not exist")

    # Print results
    if errors:
        print("❌ Reference validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1, len(errors)
    else:
        print("✅ All markdown file references are valid")
        return 0, 0


if __name__ == "__main__":
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "/home/masum/github/PR/.taskmaster/tasks"
    failed, count = validate_references(base_dir)
    sys.exit(failed)
