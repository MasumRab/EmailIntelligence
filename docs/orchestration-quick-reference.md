# Orchestration Quick Reference

## TL;DR

**Setup files are synced automatically across branches.** Make changes on orchestration-tools, and they propagate everywhere.

## Two Workflows

### Workflow 1: Direct Changes on orchestration-tools

Simple and fast - changes propagate automatically:

```bash
git checkout orchestration-tools
nano setup/setup_environment_system.sh
git add setup/
git commit -m "fix: update setup script"
git push origin orchestration-tools
# ✓ Done! Other branches sync automatically
```

### Workflow 2: Feature Branch with Orchestration Files

Creates automatic draft PR for review:

```bash
git checkout -b feature/better-setup
nano setup/setup_environment_system.sh
git add setup/
git commit -m "feat: add Python detection"
git push origin feature/better-setup
# ⚠️ Draft PR created automatically for review!
# After approval and testing:
git checkout orchestration-tools
./scripts/reverse_sync_orchestration.sh feature/better-setup <commit-sha>
git push origin orchestration-tools
```

## Common Tasks

### Working on Setup Files

```bash
# ✓ Best practice: Work on orchestration-tools directly
git checkout orchestration-tools
nano setup/setup_environment_system.sh
git add setup/ && git commit -m "..." && git push origin orchestration-tools

# Avoid: Modifying setup in feature branches if possible
# (causes PR creation and requires reverse sync)
```

### Testing Setup Changes Locally

```bash
# Test before committing
./setup/setup_environment_system.sh
python setup/launch.py --help
pytest tests/test_setup.py

# Then commit and push
git commit -m "fix: ..." && git push origin orchestration-tools
```

### Syncing to Other Branches

Automatic on:
- `git pull` (post-merge hook)
- `git checkout` (post-checkout hook)

Manual sync:
```bash
./scripts/sync_setup_worktrees.sh --verbose
```

### Reviewing What Changed

```bash
# See what's in orchestration-tools
git show orchestration-tools:setup/setup_environment_system.sh

# Compare with your branch
git diff orchestration-tools:setup/ -- setup/
```

## Command Reference

| Task | Command | When |
|------|---------|------|
| Check hook status | `ls -la .git/hooks/` | Before starting work |
| Disable hooks | `./scripts/disable-hooks.sh` | Working independently on setup |
| Enable hooks | `./scripts/enable-hooks.sh` | Done with independent work |
| Sync files manually | `./scripts/sync_setup_worktrees.sh` | After merging, if sync didn't auto-run |
| Reverse sync | `./scripts/reverse_sync_orchestration.sh <branch> <sha>` | Approved feature branch changes |
| Check orchestration files | `git ls-tree -r orchestration-tools \| grep setup` | Verify what's managed |

## Decision Tree

```
Do you need to change setup files?
├─ YES, and it should be available everywhere
│  └─ Work on: orchestration-tools branch
│     Push normally → Auto-propagates ✓
│
└─ YES, but only for this feature/branch
   └─ Work on: feature branch
      └─ Push → Draft PR auto-created ⚠️
         └─ After approval:
            └─ Use reverse_sync_orchestration.sh
               └─ Merges to orchestration-tools ✓
                  └─ Auto-propagates everywhere ✓
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Setup files not syncing | Check hooks: `ls -la .git/hooks/` |
| Changes reverted on checkout | Hooks enabled and syncing - expected behavior |
| Need independent setup work | Disable hooks: `./scripts/disable-hooks.sh` |
| PR won't create automatically | Use `gh auth login` or create manually |
| Merge conflicts in setup | Run with `--dry-run` first, resolve manually |

## File Categories

### Always Synced (Setup)
- `setup/setup_environment_system.sh`
- `setup/setup_environment_wsl.sh`
- `deployment/setup_env.py`

### Always Synced (Scripts)
- `scripts/lib/`
- `scripts/install-hooks.sh`
- `scripts/sync_setup_worktrees.sh`

### Always Synced (Config)
- `.flake8`, `.pylintrc`
- `pyproject.toml`, `requirements*.txt`
- `tsconfig.json`, `package.json`

### Synced on Hook Event
- `.gitignore`, `.gitattributes`
- Build configs (vite, tailwind, drizzle)

## Key Principles

1. **orchestration-tools is the source of truth** for setup files
2. **Hooks handle propagation automatically** - no manual sync needed usually
3. **Feature branches with setup changes create draft PRs** - ensures review
4. **Reverse sync is for approved changes** - controlled merge path
5. **Hooks can be disabled** - for independent work, then re-enabled

## Getting Help

- **Overview**: Read [orchestration-workflow.md](./orchestration-workflow.md)
- **Push details**: Read [orchestration-push-workflow.md](./orchestration-push-workflow.md)
- **Independent work**: Read [non-orchestration-workflow.md](./non-orchestration-workflow.md)
- **Environment setup**: Read [env_management.md](./env_management.md)

## Examples

### Example 1: Fix Setup Script

```bash
# Simple fix goes directly to orchestration-tools
git checkout orchestration-tools
git pull origin orchestration-tools

# Make fix
echo '#!/bin/bash' > setup/setup_environment_system.sh
# ... add actual fix ...

# Commit and push
git add setup/setup_environment_system.sh
git commit -m "fix: resolve Python 3.12 shebang issue"
git push origin orchestration-tools

# ✓ Other branches sync automatically on next pull/checkout
```

### Example 2: Test New Setup Feature

```bash
# Feature branch with testing
git checkout -b feature/add-docker-setup
nano setup/setup_environment_system.sh

# Add Docker setup code...

# Test locally
./setup/setup_environment_system.sh --with-docker
# ✓ Works!

# Commit and push
git add setup/
git commit -m "feat: add optional Docker environment setup"
git push origin feature/add-docker-setup

# ⚠️ Draft PR created: https://github.com/.../pull/123
# Assign reviewers, wait for approval

# After approval:
git checkout orchestration-tools
./scripts/reverse_sync_orchestration.sh feature/add-docker-setup <sha>
# Review the changes, then:
git push origin orchestration-tools

# ✓ All branches sync automatically
```

### Example 3: Urgent Production Fix

```bash
# Need to fix setup without full PR process?
git checkout -b hotfix/critical-setup-issue
nano setup/setup_environment_system.sh

# Fix the critical issue

git add setup/
git commit -m "fix(critical): resolve blocker in setup"
git push origin hotfix/critical-setup-issue

# If your team allows:
git checkout orchestration-tools
./scripts/reverse_sync_orchestration.sh hotfix/critical-setup-issue <sha>
git push origin orchestration-tools

# Or wait for PR approval
# Either way: ✓ Automatic sync to all branches
```

## Remember

> **The hook system means you almost never need to manually sync.** 
> Changes to orchestration-tools automatically propagate when developers pull/checkout. 
> Focus on making good changes, and the framework handles the rest.
