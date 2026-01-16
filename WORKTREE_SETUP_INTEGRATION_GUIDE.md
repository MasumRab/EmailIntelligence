# Worktree-Based Setup Integration Guide

## Overview

This guide explains the worktree-based approach for managing setup files across different branches of the Email Intelligence Platform. The worktree system allows for seamless synchronization of shared setup components while maintaining branch independence.

## Worktree Structure

The current worktree setup includes:

1. **`launch-setup-fixes`** - Contains the canonical setup files that are shared across all branches
2. **`docs-main`** - Documentation for the main branch (**documentation-only**)
3. **`docs-scientific`** - Documentation for the scientific branch (**documentation-only**)
4. **`main`** - The main production branch
5. **`worktree-workflow-system`** - Workflow system branch

**Note:** The `docs-main` and `docs-scientific` worktrees are documentation-only and should NOT contain setup files.

## Setup Files Location

The shared setup files are located in:
```
worktrees/launch-setup-fixes/setup/
```

This directory contains essential launch and setup files that are synchronized to:
- `main` worktree
- `worktree-workflow-system` worktree
- Any other code worktrees that need shared setup components

**Note:** Setup files are NOT synchronized to documentation-only worktrees (`docs-main`, `docs-scientific`).

## Synchronization Process

### Automatic Synchronization

The worktree system uses Git hooks to automatically synchronize setup files:

1. **Pre-commit hook** - Validates that documentation files are in correct locations
2. **Post-commit hook** - Runs documentation synchronization when needed

### Manual Synchronization

To manually synchronize setup files between worktrees:

```bash
# Synchronize setup files (only to non-documentation worktrees)
bash scripts/sync_setup_worktrees.sh

# Show what would be synchronized without making changes
bash scripts/sync_setup_worktrees.sh --dry-run

# Synchronize with verbose output
bash scripts/sync_setup_worktrees.sh --verbose
```

**Note:** The synchronization script automatically excludes documentation-only worktrees (`docs-main`, `docs-scientific`) from receiving setup files.

## Adding New Worktrees

To add a new worktree for a branch:

```bash
# Create a new worktree for an existing branch
git worktree add worktrees/<branch-name> <branch-name>

# Create a new worktree for a new branch
git worktree add worktrees/<branch-name> -b <branch-name>
```

## Best Practices

1. **Always work in the appropriate worktree** - Use the worktree that corresponds to your branch
2. **Keep setup files in the canonical location** - Modify setup files only in the `launch-setup-fixes` worktree
3. **Synchronize regularly** - Run the sync script after making changes to setup files
4. **Test across worktrees** - Verify that changes work correctly in all relevant worktrees
5. **Use Git hooks** - Let the automated hooks handle routine synchronization tasks

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

### Synchronization Issues

If synchronization is not working correctly:

1. **Verify worktree structure**:
   ```bash
   ls -la worktrees/
   ```

2. **Check setup directory in each worktree**:
   ```bash
   ls -la worktrees/*/setup/
   ```

3. **Run manual synchronization**:
   ```bash
   bash scripts/sync_setup_worktrees.sh --verbose
   ```

## Future Enhancements

Planned improvements to the worktree system include:

1. **Enhanced automation** - More sophisticated synchronization triggers
2. **Conflict resolution** - Better handling of merge conflicts in setup files
3. **Performance optimization** - Faster synchronization for large setups
4. **Cross-platform support** - Improved handling of platform-specific setup files