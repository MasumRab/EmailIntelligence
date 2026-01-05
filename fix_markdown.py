#!/usr/bin/env python3
"""
Markdown Linter and Fixer
Systematically fixes common markdown linting issues across all .md files.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def fix_markdown_file(filepath: Path) -> Tuple[bool, List[str]]:
    """
    Fix common markdown linting issues in a file.

    Returns:
        (changed, issues_fixed)
    """
    issues_fixed = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(filepath, "r", encoding="latin-1") as f:
            content = f.read()

    original_content = content
    lines = content.splitlines(keepends=True)

    # Fix 1: Remove trailing spaces (MD009)
    new_lines = []
    for line in lines:
        if line.rstrip() != line.rstrip("\r\n"):
            new_lines.append(line.rstrip() + line[len(line.rstrip()) :])
            if "trailing spaces" not in issues_fixed:
                issues_fixed.append("MD009: trailing spaces")
        else:
            new_lines.append(line)
    lines = new_lines

    # Fix 2: Ensure single blank line before headers (MD022)
    new_lines = []
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            # Check if previous line exists and isn't blank
            if i > 0 and lines[i - 1].strip():
                new_lines.append("\n")
                if "MD022: blank line before header" not in issues_fixed:
                    issues_fixed.append("MD022: blank line before header")
        new_lines.append(line)
    lines = new_lines

    # Fix 3: Ensure files end with single newline (MD047)
    content = "".join(lines)
    if not content.endswith("\n"):
        content += "\n"
        issues_fixed.append("MD047: file must end with newline")
    elif content.endswith("\n\n"):
        content = content.rstrip("\n") + "\n"
        issues_fixed.append("MD047: removed extra newlines at EOF")

    # Fix 4: Convert CRLF to LF (for consistency)
    if "\r\n" in content:
        content = content.replace("\r\n", "\n")
        issues_fixed.append("Normalized line endings (CRLF -> LF)")

    # Check if anything changed
    if content != original_content:
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        return True, issues_fixed

    return False, issues_fixed


def main():
    """Find and fix all markdown files."""
    base_dir = Path(".")
    md_files = list(base_dir.glob("**/*.md"))

    # Exclude certain directories
    excluded_dirs = {"node_modules", ".git", "__pycache__", ".venv", "venv"}
    md_files = [f for f in md_files if not any(excl in f.parts for excl in excluded_dirs)]

    print(f"Found {len(md_files)} markdown files to process\n")

    total_fixed = 0
    for md_file in sorted(md_files):
        changed, issues = fix_markdown_file(md_file)
        if changed:
            total_fixed += 1
            print(f"[FIXED] {md_file}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[OK] {md_file}")

    print(f"\n{'='*60}")
    print(f"Fixed {total_fixed}/{len(md_files)} files")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
