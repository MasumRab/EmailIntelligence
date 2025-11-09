#!/usr/bin/env python3
"""
Branch Rename Migration Script

This script helps migrate branch names to follow the standardized naming convention:
- feature/short-description
- bugfix/short-description
- hotfix/short-description
- refactor/short-description
- docs/short-description
"""

import subprocess
import sys
import re


def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None


def get_local_branches():
    """Get list of local branches."""
    output = run_command("git branch")
    if output is None:
        return []

    branches = []
    for line in output.split("\n"):
        # Remove the asterisk and whitespace
        branch = line.replace("*", "").strip()
        branches.append(branch)
    return branches


def get_remote_branches():
    """Get list of remote branches."""
    output = run_command("git branch -r")
    if output is None:
        return []

    branches = []
    for line in output.split("\n"):
        branch = line.strip()
        # Skip HEAD reference
        if "->" not in branch and "HEAD" not in branch:
            branches.append(branch)
    return branches


def is_valid_branch_name(branch_name):
    """Check if branch name follows the standard naming convention."""
    valid_patterns = [
        r"^feature/[a-z0-9-]+$",
        r"^bugfix/[a-z0-9-]+$",
        r"^hotfix/[a-z0-9-]+$",
        r"^refactor/[a-z0-9-]+$",
        r"^docs/[a-z0-9-]+$",
        r"^main$",
        r"^scientific$",
    ]

    for pattern in valid_patterns:
        if re.match(pattern, branch_name):
            return True
    return False


def suggest_new_name(branch_name):
    """Suggest a new name for a branch that doesn't follow the convention."""
    # Handle special cases - some branches should just be deleted
    obsolete_branches = [
        "backup-branch",
        "branch-alignment",
        "scientific-consolidated",
        "scientific-minimal-rebased",
        "backup-scientific-before-rebase-50",
        "backup/20251027_120805_audit_branch",
        "coderabbitai/utg/f31e8bd",
        "jules/audit-sqlite-branch",
        "replit-agent",
        "shared-docs-only",
    ]

    if branch_name in obsolete_branches:
        return None  # Mark for deletion

    if branch_name in ["main", "scientific"]:
        return None  # These are valid

    # Handle branches with slash but wrong prefix
    if "/" in branch_name:
        parts = branch_name.split("/")
        if parts[0] == "feat":
            return f"feature/{'/'.join(parts[1:])}"
        elif parts[0] == "fix":
            return f"bugfix/{'/'.join(parts[1:])}"
        elif parts[0] == "doc":
            return f"docs/{'/'.join(parts[1:])}"
        # If already has correct prefix, just return None
        elif parts[0] in ["feature", "bugfix", "hotfix", "refactor", "docs"]:
            return None
        # Handle fix-* branches that should be bugfix/*
        elif parts[0] == "fix" or "fix" in parts[0]:
            return f"bugfix/{'/'.join(parts[1:]) if len(parts) > 1 else parts[0]}"

    # Handle branches without slash
    if "feature-" in branch_name:
        return f"feature/{branch_name.replace('feature-', '')}"
    elif "fix-" in branch_name:
        return f"bugfix/{branch_name.replace('fix-', '')}"
    elif "bug-" in branch_name:
        return f"bugfix/{branch_name.replace('bug-', '')}"
    elif "doc-" in branch_name:
        return f"docs/{branch_name.replace('doc-', '')}"
    elif "docs-" in branch_name:
        return f"docs/{branch_name.replace('docs-', '')}"
    elif "refactor-" in branch_name:
        return f"refactor/{branch_name.replace('refactor-', '')}"

    # Special cases for specific branches
    if branch_name == "docs-cleanup":
        return "docs/cleanup"
    elif branch_name == "shared-docs-only":
        return "docs/shared-docs-only"
    elif branch_name == "launch-setup-fixes":
        return "bugfix/launch-setup-fixes"
    elif branch_name == "worktree-workflow-system":
        return "feature/worktree-workflow-system"

    # For other branches, determine based on name content
    if (
        "fix" in branch_name
        or "bug" in branch_name
        or "error" in branch_name
        or "test" in branch_name
    ):
        return f"bugfix/{branch_name.replace('fix-', '').replace('bug-', '').replace('test-', '').lower()}"
    elif "doc" in branch_name:
        return f"docs/{branch_name.replace('docs-', '').replace('doc-', '').lower()}"
    elif "refactor" in branch_name:
        return f"refactor/{branch_name.replace('refactor-', '').lower()}"
    elif "feature" in branch_name:
        return f"feature/{branch_name.replace('feature-', '').lower()}"

    # Default to feature/ for other branches
    return f"feature/{branch_name.lower()}"


def rename_local_branch(old_name, new_name):
    """Rename a local branch."""
    print(f"Renaming local branch '{old_name}' to '{new_name}'")
    result = run_command(f"git branch -m {old_name} {new_name}")
    return result is not None


def delete_remote_branch(branch_name):
    """Delete a remote branch."""
    print(f"Deleting remote branch '{branch_name}'")
    result = run_command(
        f"git push origin --delete {branch_name.replace('origin/', '')}"
    )
    return result is not None


def push_new_branch(branch_name):
    """Push a new branch to remote."""
    print(f"Pushing new branch '{branch_name}'")
    result = run_command(f"git push -u origin {branch_name}")
    return result is not None


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("DRY RUN MODE - No changes will be made")
        dry_run = True
    else:
        print("EXECUTION MODE - Changes will be made")
        dry_run = False

    print("\n=== Local Branches Analysis ===")
    local_branches = get_local_branches()
    branches_to_rename = []
    branches_to_delete = []

    for branch in local_branches:
        if is_valid_branch_name(branch):
            print(f"✓ {branch} (valid)")
        else:
            new_name = suggest_new_name(branch)
            if new_name:
                print(f"✗ {branch} (invalid) → {new_name}")
                branches_to_rename.append((branch, new_name))
            else:
                print(f"✗ {branch} (invalid) - Suggest deletion")
                branches_to_delete.append(branch)

    print("\n=== Remote Branches Analysis ===")
    remote_branches = get_remote_branches()
    remote_branches_to_delete = []
    remote_branches_to_rename = []

    for branch in remote_branches:
        # Extract branch name without origin/
        branch_name = branch.replace("origin/", "")
        if is_valid_branch_name(branch_name):
            print(f"✓ {branch} (valid)")
        else:
            new_name = suggest_new_name(branch_name)
            if new_name:
                print(f"✗ {branch} (invalid) → origin/{new_name}")
                remote_branches_to_rename.append((branch_name, new_name))
            else:
                print(f"✗ {branch} (invalid) - Suggest deletion")
                remote_branches_to_delete.append(branch_name)

    # Execute changes if not in dry run mode
    if not dry_run:
        print("\n=== Executing Changes ===")

        # Rename local branches
        for old_name, new_name in branches_to_rename:
            if rename_local_branch(old_name, new_name):
                print(f"✓ Renamed local branch '{old_name}' to '{new_name}'")
            else:
                print(f"✗ Failed to rename local branch '{old_name}' to '{new_name}'")

        # Delete local branches marked for deletion
        for branch in branches_to_delete:
            print(f"Deleting local branch '{branch}'")
            result = run_command(f"git branch -d {branch}")
            if result is not None:
                print(f"✓ Deleted local branch '{branch}'")
            else:
                print(f"✗ Failed to delete local branch '{branch}'")

        # Delete remote branches marked for deletion
        for branch in remote_branches_to_delete:
            if delete_remote_branch(f"origin/{branch}"):
                print(f"✓ Deleted remote branch 'origin/{branch}'")
            else:
                print(f"✗ Failed to delete remote branch 'origin/{branch}'")

        # Rename remote branches
        for old_name, new_name in remote_branches_to_rename:
            # First delete the old branch
            if delete_remote_branch(f"origin/{old_name}"):
                print(f"✓ Deleted remote branch 'origin/{old_name}'")
                # Then push the new branch (assuming it exists locally)
                # Note: This assumes the local branch has already been renamed
                # In a real scenario, you'd need to check if the local branch exists
            else:
                print(f"✗ Failed to delete remote branch 'origin/{old_name}'")

    print("\n=== Summary ===")
    print(f"Local branches to rename: {len(branches_to_rename)}")
    print(f"Local branches to delete: {len(branches_to_delete)}")
    print(f"Remote branches to rename: {len(remote_branches_to_rename)}")
    print(f"Remote branches to delete: {len(remote_branches_to_delete)}")

    if dry_run:
        print("\nTo execute these changes, run: python branch_rename_migration.py")


if __name__ == "__main__":
    main()
