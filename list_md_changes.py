#!/usr/bin/env python3
"""List modified markdown files from git status."""

import subprocess
import sys


def get_modified_md_files():
    """Get list of modified markdown files."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=".", timeout=10
        )

        if result.returncode != 0:
            print(f"Error running git: {result.stderr}", file=sys.stderr)
            return []

        md_files = []
        for line in result.stdout.splitlines():
            if line.strip() and line.endswith(".md"):
                # Format: "XY filename" where X is staged, Y is unstaged
                status = line[:2]
                filename = line[3:].strip()
                md_files.append((status, filename))

        return md_files

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def main():
    print("Modified/Untracked Markdown Files:\n")

    md_files = get_modified_md_files()

    if not md_files:
        print("No modified markdown files found.")
        return

    # Group by status
    modified = []
    untracked = []
    added = []

    for status, filename in md_files:
        status_code = status.strip()
        if status_code.startswith("??"):
            untracked.append(filename)
        elif "M" in status_code:
            modified.append(filename)
        elif "A" in status_code:
            added.append(filename)

    if modified:
        print(f"\nModified ({len(modified)}):")
        for f in sorted(modified):
            print(f"  M {f}")

    if added:
        print(f"\nAdded ({len(added)}):")
        for f in sorted(added):
            print(f"  A {f}")

    if untracked:
        print(f"\nUntracked ({len(untracked)}):")
        for f in sorted(untracked):
            print(f"  ?? {f}")

    print(f"\nTotal: {len(md_files)} markdown files")


if __name__ == "__main__":
    main()
