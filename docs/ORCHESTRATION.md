# Orchestration System Guide

## The Basics

**orchestration-tools** is the source of truth for setup files. Changes there automatically sync to all branches.

## Two Ways to Work

### Option 1: Direct Changes (Recommended)

```bash
git checkout orchestration-tools
nano setup/setup_environment_system.sh
git add setup/ && git commit -m "fix: ..." && git push origin orchestration-tools
# Done. Other branches sync automatically.
```

### Option 2: Feature Branch Changes

```bash
git checkout -b feature/improve-setup
nano setup/setup_environment_system.sh
git add setup/ && git commit -m "feat: ..." && git push origin feature/improve-setup
# ⚠️ Auto-creates draft PR for review
# After approval:
git checkout orchestration-tools
./scripts/reverse_sync_orchestration.sh feature/improve-setup <commit-sha>
git push origin orchestration-tools
# Done. Other branches sync automatically.
```

## Disable/Enable Hooks

### Global Disable/Enable (Recommended)

```bash
./scripts/disable-hooks.sh      # Disable automatic sync
# ... work freely on setup files ...
./scripts/enable-hooks.sh       # Re-enable when done
```

### Per-Branch Control (Advanced)

Control orchestration hooks on individual branches without affecting others:

```bash
# Enable hooks on current branch (even if not on orchestration-tools)
git config hooks.orchestration-tools.enable true

# Disable hooks on current branch
git config hooks.orchestration-tools.enable false

# Reset to default behavior (hooks only run on orchestration-tools)
git config --unset hooks.orchestration-tools.enable

# Check current setting
git config hooks.orchestration-tools.enable
```

**Default behavior:**
- Hooks run automatically on `orchestration-tools` branch
- Hooks check for orchestration-managed file changes on other branches
- Can override per-branch with `git config` to enable/disable independently

## What Files Sync

From orchestration-tools to all branches:
- `setup/` - all setup scripts
- `deployment/` - deployment configs
- `scripts/` - orchestration scripts
- Build configs (tsconfig.json, package.json, etc.)
- Dev configs (.flake8, .pylintrc, pyproject.toml, etc.)

## How It Works

```
orchestration-tools branch
         ↓
    (you push)
         ↓
   post-push hook records update
         ↓
When other developers pull/checkout:
         ↓
post-checkout/post-merge hooks auto-sync setup files
         ↓
All branches have latest setup ✓
```

## Common Commands

| Task | Command |
|------|---------|
| Check if hooks enabled | `ls -la .git/hooks/post-*` |
| Disable hooks globally | `./scripts/disable-hooks.sh` |
| Enable hooks globally | `./scripts/enable-hooks.sh` |
| Enable hooks on current branch | `git config hooks.orchestration-tools.enable true` |
| Disable hooks on current branch | `git config hooks.orchestration-tools.enable false` |
| Check branch hook setting | `git config hooks.orchestration-tools.enable` |
| Reset to default behavior | `git config --unset hooks.orchestration-tools.enable` |
| Sync manually | `./scripts/sync_setup_worktrees.sh` |
| View orchestration files | `git ls-tree -r orchestration-tools \| grep setup` |
| Compare with orchestration | `git diff orchestration-tools:setup/ -- setup/` |
| Cherry-pick approved changes | `./scripts/reverse_sync_orchestration.sh <branch> <sha>` |

## Draft PR Auto-Creation

When you push setup file changes on a non-orchestration-tools branch:
- ✅ Draft PR created automatically (if `gh` CLI available)
- ✅ Requires review before merging
- ✅ Ensures changes are approved

If `gh` unavailable:
1. Go to: https://github.com/MasumRab/EmailIntelligence/pulls
2. Create PR manually with base: `orchestration-tools`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Setup files not syncing | `./scripts/enable-hooks.sh` |
| Need independent setup work | `./scripts/disable-hooks.sh` |
| Changes got overwritten | Expected - hooks re-sync from orchestration-tools |
| Manual sync needed | `./scripts/sync_setup_worktrees.sh --verbose` |

## Key Rules

1. **orchestration-tools is canonical** - it's the source of truth
2. **Hooks sync automatically** - no manual intervention usually needed
3. **Feature branch changes create draft PRs** - ensures review
4. **Reverse sync for approved changes** - controlled merge to orchestration-tools
5. **Can disable hooks** - for independent work, then re-enable

## Examples

### Fix a Setup Bug

```bash
git checkout orchestration-tools
git pull origin orchestration-tools
nano setup/setup_environment_system.sh
git add setup/ && git commit -m "fix: resolve Python 3.12 issue"
git push origin orchestration-tools
# ✓ All branches sync automatically
```

### Test New Setup Feature

```bash
git checkout -b feature/add-docker
nano setup/setup_environment_system.sh
git add setup/ && git commit -m "feat: add Docker setup"
git push origin feature/add-docker
# ⚠️ Draft PR created automatically
# After testing and approval:
git checkout orchestration-tools
./scripts/reverse_sync_orchestration.sh feature/add-docker <sha>
git push origin orchestration-tools
# ✓ All branches sync automatically
```

### Work Independently on Setup

```bash
./scripts/disable-hooks.sh
# Now you can modify setup without auto-sync
git checkout other-branch
# ✓ Your setup changes stay (hooks disabled)
nano setup/setup_environment_system.sh
git add setup/ && git commit -m "test: experimental setup"
./scripts/enable-hooks.sh
# Hooks re-enabled, normal sync resumes
```

## More Details

- **Full Workflow**: See [orchestration-push-workflow.md](./orchestration-push-workflow.md)
- **Independent Work**: See [non-orchestration-workflow.md](./non-orchestration-workflow.md)
- **System Architecture**: See [orchestration-workflow.md](./orchestration-workflow.md)
- **Quick Reference**: See [orchestration-quick-reference.md](./orchestration-quick-reference.md)
- **Dependency Management & Troubleshooting**: See [dependency_management_guide.md](./troubleshooting/dependency_management_guide.md)
