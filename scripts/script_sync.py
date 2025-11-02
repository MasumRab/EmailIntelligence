#!/usr/bin/env python3
"""
Script Synchronization Workflow
Ensures all branches have the latest scripts from a master branch,
while preserving branch-specific customizations.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Set

def run_git_command(cmd: List[str], cwd: str = None) -> str:
    """Run a git command and return output."""
    result = subprocess.run(['git'] + cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Git command failed: {' '.join(cmd)}")
        print(f"Error: {result.stderr}")
        return ""
    return result.stdout.strip()

def get_current_branch() -> str:
    """Get current branch name."""
    return run_git_command(['branch', '--show-current'])

def get_all_branches() -> List[str]:
    """Get all local branches."""
    output = run_git_command(['branch'])
    branches = [line.strip().lstrip('* ') for line in output.split('\n') if line.strip()]
    return branches

def checkout_branch(branch: str) -> bool:
    """Checkout a branch."""
    result = subprocess.run(['git', 'checkout', branch], capture_output=True, text=True)
    return result.returncode == 0

def sync_scripts_from_master(master_branch: str, target_branch: str, preserve_custom: bool = True) -> bool:
    """
    Sync scripts from master branch to target branch.
    If preserve_custom is True, keep branch-specific modifications.
    """
    print(f"Syncing scripts from {master_branch} to {target_branch}")

    # Checkout target branch
    if not checkout_branch(target_branch):
        print(f"Failed to checkout {target_branch}")
        return False

    # Create backup of current scripts if they exist
    scripts_dir = Path("scripts")
    backup_dir = Path(".scripts_backup")
    if scripts_dir.exists() and preserve_custom:
        import shutil
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(scripts_dir, backup_dir)
        print(f"Backed up current scripts to {backup_dir}")

    # Use git read-tree to merge scripts directory from master
    # This merges only the scripts/ directory
    result = subprocess.run([
        'git', 'read-tree', '-m', '-u',
        f'{master_branch}:scripts',  # Source tree
        f'{target_branch}:scripts'   # Current tree
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Failed to merge scripts: {result.stderr}")
        # Restore backup if it exists
        if backup_dir.exists() and preserve_custom:
            if scripts_dir.exists():
                shutil.rmtree(scripts_dir)
            shutil.move(str(backup_dir), str(scripts_dir))
        return False

    # Clean up backup
    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    print(f"Successfully synced scripts to {target_branch}")
    return True

def commit_sync_changes(branch: str) -> bool:
    """Commit the synced script changes."""
    # Check if there are changes
    status = run_git_command(['status', '--porcelain'])
    if not status:
        print(f"No changes to commit in {branch}")
        return True

    # Add scripts directory
    result = subprocess.run(['git', 'add', 'scripts/'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to add scripts: {result.stderr}")
        return False

    # Commit
    result = subprocess.run([
        'git', 'commit', '-m', f'Sync scripts from master branch\n\nAutomated script synchronization'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Failed to commit: {result.stderr}")
        return False

    print(f"Committed script sync in {branch}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_sync.py <master_branch> [--all-branches] [--no-preserve]")
        print("  master_branch: Branch containing the master scripts")
        print("  --all-branches: Sync to all branches")
        print("  --no-preserve: Don't preserve branch-specific customizations")
        sys.exit(1)

    master_branch = sys.argv[1]
    all_branches = '--all-branches' in sys.argv
    preserve_custom = '--no-preserve' not in sys.argv

    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")
    print(f"Master branch: {master_branch}")
    print(f"Preserve customizations: {preserve_custom}")

    if all_branches:
        branches = get_all_branches()
        branches.remove(master_branch)  # Don't sync master to itself
    else:
        branches = [current_branch] if current_branch != master_branch else []

    if not branches:
        print("No branches to sync")
        return

    print(f"Will sync to branches: {', '.join(branches)}")

    for branch in branches:
        if not sync_scripts_from_master(master_branch, branch, preserve_custom):
            print(f"Failed to sync {branch}")
            continue

        # Commit changes
        if not commit_sync_changes(branch):
            print(f"Failed to commit changes in {branch}")

    # Return to original branch
    checkout_branch(current_branch)
    print("Script synchronization complete")

if __name__ == "__main__":
    main()