#!/usr/bin/env python3
"""
Worktree Context Detector
Detects and reports the current worktree context for git hooks.
"""

import subprocess
import sys
import os
from pathlib import Path

def get_current_branch():
    """Get the current branch name, or empty if detached HEAD."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    except Exception:
        return ""

def get_worktree_path():
    """Get the worktree path if in a worktree."""
    try:
        # Check if we're in a worktree
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            return ""

        # Get the worktree root
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    except Exception:
        return ""

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--worktree':
        branch = get_current_branch()
        print(branch)
    else:
        # Default behavior
        branch = get_current_branch()
        worktree = get_worktree_path()
        print(f"branch: {branch}, worktree: {worktree}")

if __name__ == "__main__":
    main()