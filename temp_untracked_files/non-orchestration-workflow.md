# Non-Orchestration Workflow Guide

## Overview

This guide explains how to work on setup files and configuration independently when you need to bypass the orchestration-tools framework.

The orchestration-tools branch provides a canonical source for shared configuration and setup files. However, sometimes developers need to:

- Modify setup files directly in their feature branches
- Test configuration changes without automatic sync
- Debug setup issues in isolation
- Develop setup improvements specific to a branch

## Quick Start

### Disable Hook Synchronization

To prevent automatic syncing from orchestration-tools:

```bash
./scripts/disable-hooks.sh
```

This moves all Git hooks to a disabled state, allowing you to work freely on setup files.

### Work Independently

After disabling hooks, you can:

```bash
# Modify setup files as needed
nano setup/setup_environment_system.sh
nano deployment/setup_env.py

# Commit changes to your branch
git add setup/ deployment/
git commit -m "feat: customize setup for this branch"

# Checkout other branches without auto-sync
git checkout another-branch
```

### Re-enable Hook Synchronization

When you're done with independent development:

```bash
./scripts/enable-hooks.sh
```

This restores all hooks and resumes automatic synchronization from orchestration-tools.

## Bypass Hooks on Single Operations

If you only need to bypass hooks for one operation, use the environment variable:

```bash
# Checkout without triggering post-checkout sync
DISABLE_ORCHESTRATION_CHECKS=1 git checkout feature-branch

# Merge without triggering post-merge sync
DISABLE_ORCHESTRATION_CHECKS=1 git merge main

# Work on setup files without post-commit sync
DISABLE_ORCHESTRATION_CHECKS=1 git commit -m "setup changes"
```

## Workflow Comparison

### With Hooks Enabled (Default)

```
git checkout main
  ↓
post-checkout hook triggered
  ↓
Automatically syncs setup/ and deployment/ from orchestration-tools
  ↓
Local changes overwritten with canonical versions
```

**Use this for:** Working on application code while keeping setup files consistent.

### With Hooks Disabled

```
git checkout main
  ↓
post-checkout hook skipped
  ↓
Your branch-specific setup files remain unchanged
  ↓
No automatic synchronization from orchestration-tools
```

**Use this for:** Developing setup improvements specific to your branch.

## Files Affected by Hook Synchronization

When hooks are enabled, the following files are automatically synced from orchestration-tools:

### Setup Files
- `setup/setup_environment_system.sh`
- `setup/setup_environment_wsl.sh`

### Deployment Files
- `deployment/setup_env.py`

### Scripts & Configuration
- `scripts/lib/` (entire directory)
- `scripts/install-hooks.sh`
- `scripts/sync_setup_worktrees.sh`
- `scripts/reverse_sync_orchestration.sh`
- `scripts/cleanup_orchestration.sh`

### Development Configuration
- `.flake8`
- `.pylintrc`
- `launch.py`
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- `uv.lock`

### Build Configuration
- `tsconfig.json`
- `tailwind.config.ts`
- `vite.config.ts`
- `drizzle.config.ts`
- `components.json`

### Git Configuration
- `.gitignore`
- `.gitattributes`

## Common Scenarios

### Scenario 1: Testing Setup Changes

```bash
# Disable hooks to test setup changes
./scripts/disable-hooks.sh

# Modify setup files
nano setup/setup_environment_system.sh

# Test the setup
./setup/setup_environment_system.sh

# Commit if satisfied
git add setup/
git commit -m "fix: resolve setup issue for Linux"

# Re-enable hooks
./scripts/enable-hooks.sh

# Push to your branch
git push origin your-branch
```

### Scenario 2: Quick Checkout During Development

```bash
# Need to check something in another branch without setup sync?
DISABLE_ORCHESTRATION_CHECKS=1 git checkout temp-branch

# Do your work
# ...

# Return to your branch
DISABLE_ORCHESTRATION_CHECKS=1 git checkout your-branch
```

### Scenario 3: Merge Conflicts in Setup Files

```bash
# Disable hooks to handle merge conflicts manually
./scripts/disable-hooks.sh

# Attempt merge
git merge main

# If conflicts in setup files, resolve them manually
git status

# Complete merge
git add setup/ deployment/
git commit -m "merge: resolve setup file conflicts"

# Re-enable hooks to sync canonical versions
./scripts/enable-hooks.sh
```

### Scenario 4: Extended Development on Setup

```bash
# Disable hooks for the duration of your setup work
./scripts/disable-hooks.sh

# Work on multiple setup improvements
git checkout -b feature/setup-improvements

# Several commits...
git commit -m "setup: improve Docker configuration"
git commit -m "setup: add development mode setup"
git commit -m "setup: improve error messages"

# When done, re-enable and let orchestration sync if needed
./scripts/enable-hooks.sh

# Push your branch
git push origin feature/setup-improvements
```

## Checking Hook Status

To see if hooks are currently enabled or disabled:

```bash
# Check if hooks exist
ls -la .git/hooks/pre-commit .git/hooks/post-*

# If files exist, hooks are enabled
# If files don't exist but .git/hooks.disabled/ has files, hooks are disabled
ls -la .git/hooks.disabled/
```

## Troubleshooting

### Hooks aren't working after re-enabling

```bash
# Verify hooks are executable
chmod +x .git/hooks/*

# Reinstall hooks from orchestration-tools
./scripts/install-hooks.sh --force
```

### Setup files reverted unexpectedly

```bash
# Check if hooks are still enabled
ls -la .git/hooks/

# If so, your changes were overwritten by post-checkout/post-merge
# Disable hooks and try again:
./scripts/disable-hooks.sh
```

### Need to check orchestration-tools version of files

```bash
# View what's in orchestration-tools
git show orchestration-tools:setup/setup_environment_system.sh

# Or switch to orchestration-tools temporarily
git checkout orchestration-tools
# ... review/test ...
git checkout your-branch
```

## Best Practices

1. **Be intentional about disabling hooks** - Only disable them when you need independent setup development
2. **Document your setup changes** - If you customize setup, explain why in your commit message
3. **Test thoroughly** - Test your setup changes locally before pushing
4. **Re-enable as soon as done** - Enable hooks again when you finish independent setup work
5. **Consider PRs for setup improvements** - If your setup changes are valuable, submit them to orchestration-tools as a PR
6. **Use environment variables for quick bypasses** - Use `DISABLE_ORCHESTRATION_CHECKS=1` for one-off operations

## Integration with CI/CD

The hook disable/enable scripts only affect your local git hooks. CI/CD pipelines run independently and always use the canonical orchestration-tools setup files.

If you need CI/CD to use your branch's setup files instead:
1. Create a feature branch for your setup changes
2. Test locally with hooks disabled
3. Submit a PR to orchestration-tools to make your changes canonical
4. Once merged to orchestration-tools, all branches will use the updated versions

## Related Documentation

- [Orchestration Workflow](./orchestration-workflow.md) - Main orchestration system documentation
- [Environment Management](./env_management.md) - How environment setup works
- [Setup Worktrees](../scripts/sync_setup_worktrees.sh) - Synchronizing setup across worktrees
