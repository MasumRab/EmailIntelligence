# Worktree-Based Setup Integration Guide

## Overview

This guide explains the worktree-based approach for managing setup files across different branches of the Email Intelligence Platform. The worktree system allows for seamless synchronization of shared setup components while maintaining branch independence.

## Worktree Structure

The current worktree setup includes:

1.  **`docs-main`** - Documentation for the main branch (**documentation-only**)
2.  **`docs-scientific`** - Documentation for the scientific branch (**documentation-only**)
3.  **`main`** - The main production branch
4.  **`worktree-workflow-system`** - Workflow system branch

**Note:** The `docs-main` and `docs-scientific` worktrees are documentation-only and should NOT contain setup files. Shared setup files are now sourced from the `orchestration-tools` branch.

## Setup Files Location

The shared setup files (including essential launch and setup files) are now centrally managed within the `orchestration-tools` remote branch. They are automatically synchronized to relevant worktrees by the `post-merge` hook.

**Note:** Setup files are NOT synchronized to documentation-only worktrees (`docs-main`, `docs-scientific`).

## Orchestration Tools Branch

A dedicated remote branch, `orchestration-tools`, serves as the single source of truth for managing and synchronizing the worktree environment. This branch houses:

-   **Canonical Setup and Launch Files**: All essential setup and launch configurations for the platform.
-   **Orchestration Scripts**: Including `scripts/sync_setup_worktrees.sh` (repurposed for mass updates).
-   **Git Hooks**: Such as `pre-commit`, `post-commit`, and the `post-merge` hook itself, which ensures these tools and setup files are kept up-to-date across all worktrees.

This branch is designed to centralize the management of the worktree infrastructure, allowing for consistent updates and deployment of orchestration logic and shared environment configurations.

## Synchronization Process

### Automatic Synchronization

The worktree system uses Git hooks for automation and synchronization:

1.  **Post-merge hook**: Automatically updates the `sync_setup_worktrees.sh` script, other Git hooks, and the canonical setup/launch files from the `orchestration-tools` branch whenever a `git pull` or `git merge` occurs.
2.  **Pre-commit hook** - Validates that documentation files are in correct locations (managed by the `orchestration-tools` branch).
3.  **Post-commit hook** - Runs documentation synchronization when needed (managed by the `orchestration-tools` branch).

### Manual Synchronization

To manually update all local worktrees with the latest orchestration tools and setup files from the `orchestration-tools` remote branch, use the repurposed `sync_setup_worktrees.sh` script:

```bash
# Update all local worktrees by performing a git pull in each
bash scripts/sync_setup_worktrees.sh

# Show what would be synchronized without making changes (if implemented in script)
bash scripts/sync_setup_worktrees.sh --dry-run

# Synchronize with verbose output (if implemented in script)
bash scripts/sync_setup_worktrees.sh --verbose
```

This script iterates through all active local worktrees and performs a `git pull` in each, which in turn triggers the `post-merge` hook to update the tools and setup files. This effectively provides a "push to all local worktrees" mechanism from the central `orchestration-tools` branch.

**Note:** The `post-merge` hook automatically excludes documentation-only worktrees (`docs-main`, `docs-scientific`) from receiving setup files.

## Adding New Worktrees

To add a new worktree for a branch:

```bash
# Create a new worktree for an existing branch
git worktree add worktrees/<branch-name> <branch-name>

# Create a new worktree for a new branch
git worktree add worktrees/<branch-name> -b <branch-name>
```

## Best Practices

1.  **Always work in the appropriate worktree** - Use the worktree that corresponds to your branch.
2.  **Modify shared setup/launch files only in `orchestration-tools` branch** - All changes to canonical setup and launch files must be committed to the `orchestration-tools` branch. Do NOT modify these files directly in other worktrees, as your changes will be overwritten by the `post-merge` hook.
3.  **Regularly update your worktrees** - Perform `git pull` frequently in your worktrees to ensure you receive the latest orchestration tools and setup files via the `post-merge` hook. Use `bash scripts/sync_setup_worktrees.sh` to update all your local worktrees conveniently.
4.  **Test changes to `orchestration-tools` thoroughly** - Due to its critical nature, all changes to the `orchestration-tools` branch (scripts, hooks, setup files) must undergo strict code review and testing.
5.  **Ensure `post-merge` hook is active** - Verify that the `.git/hooks/post-merge` file is correctly installed and executable in your worktree to receive automatic updates.
6.  **Use Git hooks** - Let the automated hooks handle routine synchronization tasks.

## Troubleshooting

### Worktree Issues

If you encounter issues with worktrees:

1. **Check worktree status**:
   ```bash
   git worktree list
   ```

2. **Remove problematic worktrees**:
   ```bash
   git worktree remove <worktree-name>
   ```

3. **Prune stale worktree references**:
   ```bash
   git worktree prune
   ```

### Orchestration Tools Issues

If the orchestration tools (sync script, Git hooks) or setup files are not updating or behaving as expected:

1.  **Verify `orchestration-tools` branch**: Ensure the `orchestration-tools` remote branch exists, is accessible, and contains the correct scripts, hooks, and setup files.
2.  **Check `post-merge` hook**: Verify that the `.git/hooks/post-merge` file exists in your worktree, is executable, and contains the correct logic for updating orchestration tools and setup files.
3.  **Manually trigger update**: Run `git pull` or `git merge` to trigger the `post-merge` hook, or manually execute the `post-merge` script to debug.
4.  **Check temporary directory**: Inspect the temporary directory created by the `post-merge` hook (e.g., `/tmp/git-checkout-XXXXXX`) to see if the files from `orchestration-tools` are being correctly checked out.
5.  **Accidental Overwrites**: If you made local modifications to files in the `setup/` directory and they were overwritten, this is expected behavior. Always make changes to canonical setup files directly in the `orchestration-tools` branch. Consider backing up local changes before pulling if necessary.

## Future Enhancements

Planned improvements to the worktree system include:

1. **Enhanced automation** - More sophisticated synchronization triggers
2. **Conflict resolution** - Better handling of merge conflicts in setup files
3. **Performance optimization** - Faster synchronization for large setups
4. **Cross-platform support** - Improved handling of platform-specific setup files