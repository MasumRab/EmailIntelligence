# Orchestration Update and Hook Management Guide

## Overview
This document provides instructions for making changes to orchestration-managed files and properly updating Git hooks across all branches.

## When to Reinstall Hooks

Hooks should be reinstalled when any of the following orchestration files are modified:

### Core Hook Files
- `scripts/hooks/pre-commit`
- `scripts/hooks/post-commit`
- `scripts/hooks/post-merge`
- `scripts/hooks/post-checkout`
- `scripts/hooks/post-push`

### Supporting Scripts
- `scripts/install-hooks.sh`
- `scripts/lib/*.sh` (utility libraries)
- `scripts/cleanup_orchestration.sh`
- `scripts/sync_setup_worktrees.sh`

## Update Process

### 1. Making Changes to Orchestration Files

1. **Work in the orchestration-tools branch only**:
   ```bash
   git checkout orchestration-tools
   ```

2. **Make your changes** to the appropriate orchestration files

3. **Test your changes locally**:
   ```bash
   # Test install-hooks script
   scripts/install-hooks.sh --force --verbose
   
   # Verify hooks are working
   # Try a checkout to test post-checkout hook
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Update orchestration hooks for XYZ functionality"
   ```

5. **Push to remote**:
   ```bash
   git push origin orchestration-tools
   ```

### 2. Propagating Changes to Other Branches

Changes to orchestration-managed files automatically propagate to other branches through the Git hook system:

1. **When switching branches** (post-checkout hook):
   - Hooks are automatically reinstalled from orchestration-tools
   - Essential files are synchronized

2. **When merging** (post-merge hook):
   - Hooks are updated after merges
   - Setup files are synchronized

3. **Manual update** (if needed):
   ```bash
   # From any branch, force reinstall hooks
   scripts/install-hooks.sh --force
   ```

## Central List of Orchestration-Managed Files

### Essential Setup Files (Synced to all branches)
- `setup/` directory
- `launch.py` (root wrapper)
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- `uv.lock`
- `.flake8`
- `.pylintrc`
- `.gitignore`
- `.gitattributes`

### Hook System Files (Orchestration-tools only)
- `scripts/install-hooks.sh`
- `scripts/hooks/` directory
- `scripts/lib/` directory
- `scripts/cleanup_orchestration.sh`
- `scripts/sync_setup_worktrees.sh`

### Documentation Files (Synced to all branches)
- `docs/orchestration_summary.md`
- `docs/orchestration-workflow.md`
- `docs/env_management.md`

## Verification Process

### After Making Changes

1. **Verify hook installation**:
   ```bash
   # Check that hooks are installed
   ls -la .git/hooks/
   
   # Check specific hook content
   cat .git/hooks/post-checkout
   ```

2. **Test hook functionality**:
   ```bash
   # Test post-checkout by switching branches
   git checkout main
   git checkout orchestration-tools
   
   # Check that hooks executed properly
   ```

3. **Verify file synchronization**:
   ```bash
   # Check that setup files are properly synced
   diff setup/launch.py ../main/setup/launch.py
   ```

### Troubleshooting Hook Issues

1. **If hooks are not updating**:
   ```bash
   # Force reinstall hooks
   scripts/install-hooks.sh --force --verbose
   
   # Check for errors in installation
   ```

2. **If synchronization fails**:
   ```bash
   # Manually sync setup directory
   git checkout orchestration-tools -- setup/
   
   # Check for conflicts
   git status
   ```

3. **If hooks are outdated**:
   ```bash
   # Check current hook versions
   scripts/install-hooks.sh --verbose
   
   # Compare with remote
   git fetch origin
   ```

## Best Practices

### For Orchestration Development
1. **Always work in orchestration-tools branch**
2. **Test hooks thoroughly before committing**
3. **Update documentation when changing behavior**
4. **Use --force flag when testing locally**
5. **Verify cross-branch compatibility**

### For Other Branch Development
1. **Make orchestration changes via PR process**
2. **Run install-hooks.sh after major updates**
3. **Report hook issues immediately**
4. **Don't modify orchestration files directly**

## Emergency Procedures

### If Hooks Are Broken
1. **Restore from known good state**:
   ```bash
   # Fetch latest from remote
   git fetch origin
   
   # Force reinstall hooks from remote
   git checkout origin/orchestration-tools -- scripts/install-hooks.sh
   scripts/install-hooks.sh --force
   ```

2. **Manual hook restoration**:
   ```bash
   # Copy hooks directly from orchestration-tools
   cp -r ../orchestration-tools/.git/hooks/* .git/hooks/
   ```

### If Synchronization Fails
1. **Manual sync essential files**:
   ```bash
   git checkout orchestration-tools -- setup/
   git checkout orchestration-tools -- .flake8 .pylintrc
   ```

2. **Reinstall hooks**:
   ```bash
   scripts/install-hooks.sh --force
   ```

## Version Control

### Tracking Changes
- All orchestration changes should be committed with descriptive messages
- Major updates should include version bumps in relevant scripts
- Breaking changes should be clearly documented

### Release Process
1. **Update version numbers** in scripts when making significant changes
2. **Document breaking changes** in commit messages
3. **Test across multiple branches** before finalizing

This process ensures that all developers have consistent hook versions and that orchestration-managed files remain synchronized across all branches.