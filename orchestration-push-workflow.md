# Orchestration Push Workflow

## Overview

This document describes what happens when changes to orchestration-tools files are pushed to the repository, and how to manage changes that need to propagate across all branches.

There are two distinct workflows:

1. **Forward Push** - Pushing changes to orchestration-tools that propagate to all branches
2. **Reverse Sync** - Pulling approved changes from feature branches back into orchestration-tools

## Forward Push Workflow

When you push changes to the `orchestration-tools` branch, those changes automatically propagate to all other branches through Git hooks.

### How It Works

```
Developer pushes to orchestration-tools
  ↓
post-push hook triggered
  ↓
Updates orchestration-tools metadata
  ↓
(CI/CD could trigger here)
  ↓
When other branches checkout/merge:
  ↓
post-checkout or post-merge hooks triggered
  ↓
Hooks sync changed files from orchestration-tools
```

### Files That Propagate

When you push to orchestration-tools, the following files automatically sync to all branches:

**Setup Files**
- `setup/setup_environment_system.sh`
- `setup/setup_environment_wsl.sh`
- `deployment/setup_env.py`

**Scripts & Libraries**
- `scripts/lib/` (entire directory)
- `scripts/install-hooks.sh`
- `scripts/sync_setup_worktrees.sh`
- `scripts/reverse_sync_orchestration.sh`
- `scripts/cleanup_orchestration.sh`

**Development Configuration**
- `.flake8`
- `.pylintrc`
- `launch.py`
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- `uv.lock`

**Build Configuration**
- `tsconfig.json`
- `tailwind.config.ts`
- `vite.config.ts`
- `drizzle.config.ts`
- `components.json`

**Git Configuration**
- `.gitignore`
- `.gitattributes`

### Push to orchestration-tools

Direct commits to orchestration-tools are straightforward:

```bash
# On orchestration-tools branch
git checkout orchestration-tools
git pull origin orchestration-tools

# Make your changes
nano setup/setup_environment_system.sh

# Commit
git add setup/setup_environment_system.sh
git commit -m "fix: improve environment detection in setup script"

# Push - post-push hook will handle the rest
git push origin orchestration-tools
```

The post-push hook notes the push and any other branches will automatically sync on their next checkout/merge operation.

## Reverse Sync Workflow

When developers make changes to orchestration-managed files in their feature branches, those changes need to be reviewed and approved before merging back into orchestration-tools.

### Detection & Draft PR Creation

When a developer pushes changes to orchestration-managed files on a non-orchestration-tools branch:

```
Developer commits changes to orchestration files on feature branch
  ↓
git push origin feature-branch
  ↓
post-push hook detects orchestration file changes
  ↓
Automatically creates a DRAFT PR:
  - Base: orchestration-tools
  - Head: feature-branch
  - Label: "orchestration,auto-created"
  - Status: DRAFT (not ready for merge)
  ↓
Developer reviews and tests the draft PR
```

### Example: Detecting Orchestration Changes

```bash
# On feature branch
git checkout -b feature/improve-setup

# Modify setup files
nano setup/setup_environment_system.sh
git add setup/setup_environment_system.sh
git commit -m "feat: add Python version detection"

# Push
git push origin feature/improve-setup

# OUTPUT:
# ⚠️  ORCHESTRATION CHANGES DETECTED on branch 'feature/improve-setup'
#    Files changed: setup/setup_environment_system.sh
#
#    IMPORTANT: These files are managed by the orchestration-tools branch.
#    Changes here will be OVERWRITTEN when this branch pulls from orchestration-tools.
#
# 🤖 Attempting to create automatic draft PR...
# ✅ DRAFT PR CREATED SUCCESSFULLY!
# 🔗 PR URL: https://github.com/MasumRab/EmailIntelligence/pull/123
#
# 📋 Next Steps:
# 1. Review the auto-generated PR
# 2. Test changes thoroughly
# 3. Mark as ready for review when prepared
# 4. Request reviews from orchestration maintainers
#
# ⚠️  REMEMBER: Do not merge until fully tested and approved!
```

### Manual PR Creation

If the automatic PR creation fails (no GitHub CLI, not authenticated, etc.):

1. Go to: https://github.com/MasumRab/EmailIntelligence/pulls
2. Click "New Pull Request"
3. Set:
   - Base: `orchestration-tools`
   - Compare: `your-feature-branch`
4. Use PR template: `orchestration-pr.md`
5. Fill out the impact assessment and testing plan
6. Request reviews from orchestration maintainers

### Merging Changes to orchestration-tools

There are two paths for merging changes to orchestration-tools:

#### Path 1: Standard PR Merge (Recommended)

For most changes:

```bash
# 1. Draft PR is created automatically
# 2. Developer tests thoroughly locally
# 3. Mark PR as "Ready for review"
# 4. Orchestration maintainers review
# 5. Tests pass in CI/CD
# 6. Merge PR via GitHub
```

#### Path 2: Manual Reverse Sync (For Approved Changes)

For urgent fixes or when you want to manually control the process:

```bash
# First, ensure the change is approved
# Then, on the orchestration-tools branch:
git checkout orchestration-tools
git pull origin orchestration-tools

# Use reverse sync to apply approved commit
./scripts/reverse_sync_orchestration.sh feature/fix-setup abc123def

# Review the changes
git log --oneline -5

# Push
git push origin orchestration-tools
```

## Step-by-Step: Complete Reverse Sync Process

### 1. Develop Your Changes

```bash
# Create feature branch
git checkout -b feature/better-setup-detection

# Make changes to setup files
nano setup/setup_environment_system.sh

# Test locally
./setup/setup_environment_system.sh
# Verify it works correctly

# Commit
git add setup/setup_environment_system.sh
git commit -m "feat: add automatic environment detection"
```

### 2. Push and See Draft PR

```bash
# Push your changes
git push origin feature/better-setup-detection

# A draft PR is automatically created if orchestration files changed
# Example output shows the PR URL
```

### 3. Test Thoroughly

```bash
# Test on multiple platforms/conditions
# Example test checklist:
# - [ ] Test on Linux
# - [ ] Test on WSL
# - [ ] Test on macOS (if applicable)
# - [ ] Test with Python 3.10+
# - [ ] Test with missing dependencies
# - [ ] Verify no breaking changes to other branches
```

### 4. Mark PR Ready and Request Review

In the GitHub PR:
1. Click "Ready for review" to promote from draft
2. Request review from orchestration maintainers
3. Add a detailed description of impact

### 5. Resolve Review Comments

```bash
# If review requests changes:
git checkout feature/better-setup-detection
# ... make changes ...
git add setup/
git commit -m "fix: address review feedback"
git push origin feature/better-setup-detection
# PR updates automatically
```

### 6. Merge to orchestration-tools

Once approved:

```bash
# Option A: Merge via GitHub UI
# (Click "Merge pull request" button)

# Option B: Manual merge
git checkout orchestration-tools
git pull origin orchestration-tools
git merge --no-ff feature/better-setup-detection
git push origin orchestration-tools
```

### 7. Cleanup

After merge:

```bash
# Delete feature branch locally
git branch -d feature/better-setup-detection

# Delete remote branch
git push origin --delete feature/better-setup-detection

# All other branches will automatically sync on next checkout/merge
```

## Reverse Sync Script Usage

The `reverse_sync_orchestration.sh` script provides controlled reverse synchronization:

### Basic Usage

```bash
# Switch to orchestration-tools branch first
git checkout orchestration-tools
git pull origin orchestration-tools

# Apply a specific commit from a feature branch
./scripts/reverse_sync_orchestration.sh feature/fix-setup abc123def

# The script will:
# 1. Show the commit details
# 2. List affected files
# 3. Show the diff
# 4. Ask for confirmation
# 5. Cherry-pick the commit
# 6. Provide next steps
```

### Dry Run

Preview what the script will do without making changes:

```bash
./scripts/reverse_sync_orchestration.sh feature/fix-setup abc123def --dry-run

# Output shows exactly what would happen without modifying files
```

### Handling Conflicts

If the cherry-pick encounters conflicts:

```bash
# Script will report the conflict
# Resolve conflicts manually
nano setup/setup_environment_system.sh

# After resolving
git add setup/
git cherry-pick --continue

# Or cancel if there are issues
git cherry-pick --abort
```

## Propagation Timeline

### How quickly changes propagate

1. **Immediately on orchestration-tools**: Changes are available
2. **Next checkout**: Other branches automatically sync setup files
3. **Next merge**: Setup files are automatically synced
4. **With hooks disabled**: No automatic sync until re-enabled

### Example Timeline

```
09:00 - Developer pushes to orchestration-tools
        (post-push hook logs the update)

09:15 - Developer on 'main' branch does: git pull
        (post-merge hook triggers, syncs setup files)

09:20 - Developer on 'scientific' branch does: git checkout main
        (post-checkout hook triggers, syncs setup files)

09:30 - Developer with hooks disabled manually pulls:
        DISABLE_ORCHESTRATION_CHECKS=1 git pull
        (no auto-sync occurs)
```

## Best Practices

### For Changes to orchestration-tools

1. **Test thoroughly** before pushing
   ```bash
   ./setup/setup_environment_system.sh
   python setup/launch.py --help
   pytest tests/test_setup.py
   ```

2. **Use descriptive commit messages**
   ```bash
   git commit -m "fix: resolve Python 3.12 compatibility in setup script

   - Update shebang to use python3
   - Add version detection
   - Handle missing pip gracefully"
   ```

3. **Push with confidence** - hooks handle propagation
   ```bash
   git push origin orchestration-tools
   ```

### For Changes in Feature Branches

1. **Be aware** if you're modifying orchestration files
   ```bash
   # Understand this will create a PR
   nano setup/setup_environment_system.sh
   ```

2. **Avoid unnecessary changes** to managed files
   - Only modify if your feature requires it
   - Prefer changes in orchestration-tools if broadly useful

3. **Test before push**
   - Ensure your changes work correctly
   - Verify they don't break other branches

4. **Monitor the auto-created PR**
   - Respond to review comments
   - Keep the PR updated
   - Don't merge draft PRs without approval

## Troubleshooting

### Changes didn't propagate

```bash
# Check current branch
git status

# Manually trigger sync
git checkout orchestration-tools
git checkout your-branch
# post-checkout hook should run

# Or manually sync if hooks are disabled
./scripts/enable-hooks.sh
./scripts/sync_setup_worktrees.sh --verbose
```

### Draft PR not created automatically

Requirements for auto-creation:
- [ ] GitHub CLI (`gh`) installed: `gh --version`
- [ ] Authenticated: `gh auth status`
- [ ] Network connectivity
- [ ] Sufficient GitHub permissions

Manual creation fallback:
1. Go to: https://github.com/MasumRab/EmailIntelligence/pulls
2. Create PR manually with orchestration template

### Cherry-pick conflicts during reverse sync

```bash
# View the conflict
git status

# Resolve manually
nano setup/setup_environment_system.sh

# Mark as resolved
git add setup/setup_environment_system.sh

# Continue cherry-pick
git cherry-pick --continue
```

### Changes to orchestration-tools not syncing to branches

```bash
# Check if hooks are enabled
ls -la .git/hooks/post-*

# If disabled, enable them
./scripts/enable-hooks.sh

# Force sync to all branches
./scripts/sync_setup_worktrees.sh --verbose

# Verify in other branches
git checkout another-branch
# Should see updated files
```

## Migration from Non-Orchestration to Orchestration

If a branch has been developed without the orchestration framework:

```bash
# 1. Switch to the branch
git checkout developed-branch

# 2. Enable hooks (if they weren't installed)
./scripts/install-hooks.sh

# 3. Sync from orchestration-tools
git checkout orchestration-tools -- setup/ deployment/ scripts/lib/

# 4. Review changes
git status
git diff

# 5. Commit the sync
git add setup/ deployment/ scripts/lib/
git commit -m "chore: sync orchestration files from orchestration-tools"

# 6. Verify everything still works
./setup/setup_environment_system.sh
```

## Related Documentation

- [Orchestration Workflow](./orchestration-workflow.md) - Overall orchestration system
- [Non-Orchestration Workflow](./non-orchestration-workflow.md) - Working independently
- [Environment Management](./env_management.md) - Setup and environment files
- [Worktree Setup](../scripts/sync_setup_worktrees.sh) - Syncing across worktrees
