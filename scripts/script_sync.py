#!/usr/bin/env python3
"""
Script Synchronization Workflow
Ensures all branches have the latest scripts from a master branch,
while preserving branch-specific customizations.
"""

import shutil
import sys
from pathlib import Path
from typing import List

from scripts.git_utils import GitHelper, create_git_helper

# Global git helper instance
git = create_git_helper()

def checkout_branch(branch: str) -> bool:
    """Checkout a branch."""
    if git.is_branch_checked_out_in_worktree(branch):
        print(f"Branch {branch} is currently checked out in a worktree, skipping")
        return False
    return git.checkout(branch)

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
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(scripts_dir, backup_dir)
        print(f"Backed up current scripts to {backup_dir}")

    # Check if target branch has scripts directory
    target_has_scripts = git.tree_exists(target_branch, "scripts")

    if target_has_scripts:
        success = git.read_tree(f'{master_branch}:scripts', f'{target_branch}:scripts')
        if not success:
            print(f"Failed to sync scripts: read-tree failed")
            if backup_dir.exists() and preserve_custom:
                if scripts_dir.exists():
                    shutil.rmtree(scripts_dir)
                shutil.move(str(backup_dir), str(scripts_dir))
            return False
    else:
        success = git.checkout(master_branch, ["scripts/"])
        if not success:
            print(f"Failed to sync scripts: checkout failed")
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
    if not git.is_dirty():
        print(f"No changes to commit in {branch}")
        return True

    if not git.add([Path("scripts")]):
        print(f"Failed to add scripts")
        return False

    commit_msg = "Sync scripts from master branch\n\nAutomated script synchronization"
    result = git.commit(commit_msg)
    if not result:
        print(f"Failed to commit")
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

    current_branch = git.get_current_branch()
    print(f"Current branch: {current_branch}")
    print(f"Master branch: {master_branch}")
    print(f"Preserve customizations: {preserve_custom}")

    if all_branches:
        branches = git.get_all_branches()
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

        if not commit_sync_changes(branch):
            print(f"Failed to commit changes in {branch}")

    # Return to original branch
    checkout_branch(current_branch)
    print("Script synchronization complete")

if __name__ == "__main__":
    main()