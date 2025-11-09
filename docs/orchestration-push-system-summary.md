# Orchestration Push System Summary

## What We've Built

A complete system that manages setup files and configuration across all branches, with automatic propagation and review controls.

```
┌─────────────────────────────────────────────────────────────┐
│          Orchestration Push System Architecture             │
└─────────────────────────────────────────────────────────────┘

ORCHESTRATION-TOOLS BRANCH (Source of Truth)
├── setup/
│   ├── setup_environment_system.sh
│   ├── setup_environment_wsl.sh
│   └── launch.py
├── deployment/
│   └── setup_env.py
├── scripts/
│   ├── disable-hooks.sh ← New: Allow independent work
│   ├── enable-hooks.sh  ← New: Re-enable syncing
│   ├── sync_setup_worktrees.sh
│   ├── reverse_sync_orchestration.sh
│   └── lib/
├── Configuration files (.flake8, .pylintrc, etc.)
└── Build configs (tsconfig.json, vite.config.ts, etc.)

                            ↓
                    
        ┌───────────────────────────────────────┐
        │        Git Hooks (Auto-Sync)          │
        ├───────────────────────────────────────┤
        │ • post-checkout → sync on branch switch
        │ • post-merge    → sync on merge
        │ • post-commit   → prompt on orchestration-tools
        │ • post-push     → detect changes, create PRs
        │ • pre-commit    → validation
        └───────────────────────────────────────┘

                            ↓

    ┌──────────────────────────────────────────┐
    │     Propagates to All Branches           │
    ├──────────────────────────────────────────┤
    │ main, scientific, feature/*, etc.        │
    │                                          │
    │ Files sync automatically via hooks       │
    └──────────────────────────────────────────┘
```

## Complete Workflow Paths

### Path 1: Direct Changes on orchestration-tools

**Use when:** Making improvements that benefit all branches

```
Developer on orchestration-tools
    ↓
    Modify setup files
    ↓
    git commit
    ↓
    git push origin orchestration-tools
    ↓
    post-push hook runs
    ↓
    Records the push (CI/notifications could trigger)
    ↓
    When developers on other branches do:
    - git pull
    - git merge
    - git checkout
    ↓
    post-checkout/post-merge hooks auto-sync setup files
    ↓
    ✓ All branches have latest setup
```

### Path 2: Feature Branch with Setup Changes

**Use when:** Testing setup improvements before broad rollout

```
Developer on feature/improve-setup
    ↓
    Modify setup files
    ↓
    git commit & git push origin feature/improve-setup
    ↓
    post-push hook detects orchestration file changes
    ↓
    ⚠️ AUTO-CREATES DRAFT PR
    - Base: orchestration-tools
    - Head: feature/improve-setup
    - Status: DRAFT (can't merge yet)
    ↓
    Developer tests thoroughly locally
    ↓
    Mark PR "Ready for Review"
    ↓
    Code review & approval
    ↓
    Tests pass in CI/CD
    ↓
    Merge or use reverse_sync_orchestration.sh:
    git checkout orchestration-tools
    ./scripts/reverse_sync_orchestration.sh feature/... <sha>
    git push origin orchestration-tools
    ↓
    post-push hook runs
    ↓
    All branches auto-sync on next pull/checkout
    ↓
    ✓ Changes available everywhere
```

### Path 3: Independent Setup Work (Hooks Disabled)

**Use when:** Developing setup improvements without auto-sync interference

```
Developer on feature/custom-setup
    ↓
    ./scripts/disable-hooks.sh
    (Hooks moved to .git/hooks.disabled/)
    ↓
    Work freely on setup files
    - No auto-sync from orchestration-tools
    - Can checkout other branches without sync
    ↓
    Test locally
    ↓
    When done:
    ./scripts/enable-hooks.sh
    (Hooks restored to .git/hooks/)
    ↓
    Ready for PR/reverse sync process
    ↓
    ✓ Continue with Path 2 (Feature Branch) if merging to orchestration-tools
```

## Key Components

### 1. Git Hooks (Automatic Syncing)

Located in: `scripts/hooks/` → `.git/hooks/`

| Hook | Triggers | Action |
|------|----------|--------|
| **post-checkout** | `git checkout` | Sync setup files from orchestration-tools |
| **post-merge** | `git merge`, `git pull` | Sync setup files from orchestration-tools |
| **post-commit** | `git commit` on orchestration-tools | Prompt to run sync script |
| **post-push** | `git push` | Detect orchestration changes, create draft PR |
| **pre-commit** | `git commit` | Validate files before committing |

### 2. Synchronization Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| **disable-hooks.sh** | Disable auto-sync | Allow independent setup work |
| **enable-hooks.sh** | Re-enable auto-sync | Resume orchestration-tools sync |
| **sync_setup_worktrees.sh** | Manual sync | Manually sync to worktrees |
| **reverse_sync_orchestration.sh** | Cherry-pick approved changes | Merge feature branch changes to orchestration-tools |
| **install-hooks.sh** | Install/update hooks | Set up hooks from orchestration-tools |

### 3. PR Automation

**Auto-Draft PR Creation**
- Triggers on push to non-orchestration-tools branch
- Requires: `gh` CLI installed and authenticated
- Creates DRAFT PR (not ready to merge)
- Labels with `orchestration,auto-created`
- Guides developer through review process

**Fallback**
- If `gh` unavailable: Manual PR creation instructions
- PR template: `.github/pull_request_templates/orchestration-pr.md`

### 4. Documentation

| Document | Purpose |
|----------|---------|
| **orchestration-workflow.md** | Overall system overview |
| **orchestration-push-workflow.md** | Complete push workflow details |
| **non-orchestration-workflow.md** | Disabling hooks and independent work |
| **orchestration-quick-reference.md** | TL;DR guide and examples |
| **env_management.md** | Environment setup details |

## Lifecycle of a Setup File Change

```
1. DEVELOPMENT PHASE
   └─ Developer works on setup file (orchestration-tools or feature branch)

2. PUSH PHASE
   └─ git push origin <branch>
   └─ post-push hook triggers
      └─ If orchestration-tools: Records update
      └─ If feature branch: Creates draft PR (if orchestration files changed)

3. REVIEW PHASE
   ├─ If feature branch:
   │  └─ Code review in draft PR
   │  └─ Feedback addressed
   │  └─ Approval received
   └─ If orchestration-tools:
      └─ Already in canonical location

4. PROPAGATION PHASE
   ├─ Merge to orchestration-tools (if feature branch)
   │  └─ post-push hook runs
   └─ All other branches sync on next:
      └─ git pull
      └─ git merge
      └─ git checkout

5. AVAILABILITY PHASE
   └─ All branches have latest setup files
   └─ Developers continue normal workflow
```

## File Propagation Map

```
orchestration-tools Branch
├── Changes to setup/
│   └─ SETUP FILES
│      ├─ setup_environment_system.sh → All branches
│      └─ setup_environment_wsl.sh    → All branches
│
├── Changes to deployment/
│   └─ DEPLOYMENT FILES
│      └─ setup_env.py → All branches
│
├── Changes to scripts/
│   └─ SCRIPTS
│      ├─ lib/           → All branches
│      ├─ disable-hooks.sh → All branches
│      ├─ enable-hooks.sh  → All branches
│      └─ sync_*.sh       → All branches
│
├── Changes to config files
│   └─ CONFIG FILES
│      ├─ .flake8         → All branches
│      ├─ .pylintrc       → All branches
│      ├─ pyproject.toml  → All branches
│      └─ etc.            → All branches
│
└── Changes to build configs
   └─ BUILD FILES
      ├─ tsconfig.json     → All branches
      ├─ package.json      → All branches
      ├─ vite.config.ts    → All branches
      └─ etc.              → All branches
```

## Decision Making Guide

```
Do you need to modify setup files?

├─ YES, it's a general improvement
│  └─ git checkout orchestration-tools
│     └─ Make changes
│        └─ git push origin orchestration-tools
│           └─ ✓ Auto-propagates to all branches

├─ YES, but testing on feature branch first
│  └─ git checkout -b feature/test-setup
│     └─ Make changes
│        └─ git push origin feature/test-setup
│           └─ ⚠️ Draft PR created for review
│              └─ After approval:
│                 └─ ./scripts/reverse_sync_orchestration.sh
│                    └─ git push origin orchestration-tools
│                       └─ ✓ Auto-propagates to all branches

├─ YES, but need independent work (no auto-sync)
│  └─ ./scripts/disable-hooks.sh
│     └─ Make changes freely
│        └─ Test thoroughly
│           └─ When ready:
│              └─ ./scripts/enable-hooks.sh
│                 └─ Follow Path 1 or 2 above

└─ NO, don't modify setup files
   └─ No need for orchestration-tools or reverse sync
      └─ Normal development on any branch
```

## Permissions & Roles

### Developers (Everyone)

- [ ] Can work on feature branches
- [ ] Can create draft PRs for orchestration changes
- [ ] Can test setup changes locally
- [ ] Can disable hooks for independent work
- [ ] Cannot merge to orchestration-tools without approval

### Orchestration Maintainers

- [ ] Can commit directly to orchestration-tools
- [ ] Can review/approve orchestration PRs
- [ ] Can use reverse_sync_orchestration.sh
- [ ] Responsible for testing changes broadly
- [ ] Ensure no breaking changes

### CI/CD

- [ ] Validates changes on push
- [ ] Runs tests on orchestration changes
- [ ] Blocks merge if tests fail
- [ ] Notifies on failures

## Configuration

### Hooks Control

```bash
# Check if hooks enabled
ls -la .git/hooks/

# Disable all hooks
./scripts/disable-hooks.sh

# Enable all hooks
./scripts/enable-hooks.sh

# Bypass for single operation
DISABLE_ORCHESTRATION_CHECKS=1 git checkout branch
```

### Environment Variables

```bash
# Disable hooks for single operation
export DISABLE_ORCHESTRATION_CHECKS=1

# Specify orchestration branch (default: orchestration-tools)
export ORCHESTRATION_BRANCH=my-orchestration-branch

# Verbose logging
export LOG_LEVEL=DEBUG
```

## Troubleshooting Matrix

| Symptom | Cause | Solution |
|---------|-------|----------|
| Setup files not updating | Hooks disabled | `./scripts/enable-hooks.sh` |
| Changes reverted | Auto-sync working | Expected behavior - make changes on orchestration-tools |
| PR not created | No `gh` or not authenticated | Use manual PR creation |
| Merge conflicts | Stale local branch | Pull orchestration-tools first |
| Files locked | Hooks running | Wait for hook to complete |

## Best Practices

### ✓ DO

- [ ] Test setup changes locally before pushing
- [ ] Use orchestration-tools directly for broad improvements
- [ ] Use feature branches when testing new approaches
- [ ] Mark PRs "Ready for review" when tested
- [ ] Request reviews from orchestration maintainers
- [ ] Document breaking changes clearly
- [ ] Test on multiple platforms when possible

### ✗ DON'T

- [ ] Force push to orchestration-tools (breaks other branches)
- [ ] Merge draft PRs without approval
- [ ] Skip testing setup changes locally
- [ ] Commit hardcoded paths in setup files
- [ ] Ignore post-push hook warnings
- [ ] Disable hooks permanently
- [ ] Modify setup files without considering impact

## Integration Points

### With Git Worktrees

Hooks automatically sync to worktrees on merge/checkout:
```bash
# In worktree for 'main' branch
git merge another-branch
# post-merge hook syncs setup files
```

### With CI/CD

Setup files validated before merge:
```yaml
- name: Validate orchestration changes
  run: |
    ./setup/setup_environment_system.sh --validate
    python setup/launch.py --check
```

### With GitHub

Draft PRs auto-created for orchestration changes:
- Base: orchestration-tools
- Labels: orchestration, auto-created
- Status: Draft (can't merge)

## Performance Notes

- Hooks run quickly (< 1 second typically)
- File sync uses git internally (efficient)
- Can disable hooks for batch operations
- Manual sync with `--dry-run` for preview

## Related Systems

- **Git Worktrees**: Automatically synced via hooks
- **CI/CD Pipeline**: Validates orchestration changes
- **GitHub Actions**: Could be triggered on orchestration-tools push
- **Development Tools**: Use synced configs automatically

---

**For detailed information, see:**
- [Orchestration Workflow](./orchestration-workflow.md)
- [Push Workflow Details](./orchestration-push-workflow.md)
- [Non-Orchestration Workflow](./non-orchestration-workflow.md)
- [Quick Reference](./orchestration-quick-reference.md)
