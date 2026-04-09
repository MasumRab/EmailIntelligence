# AGENTS_orchestration-tools.md - Orchestration Tools Branch Extensions

This document extends the core `AGENTS.md` guide with orchestration-tools branch-specific commands, workflows, and considerations.

## Branch Overview

The `orchestration-tools` branch implements **git hook-based orchestration** for automated branch management, conflict resolution, and specification-driven workflows. All developments on this branch interact with the orchestration system.

---

## Orchestration-Specific Commands

### Orchestration Control

```bash
# Check current orchestration status
echo $ORCHESTRATION_ENABLED                          # Empty = active, "true" = force-enabled, "false" = disabled

# Disable Orchestration (hooks + env var)
./scripts/disable-all-orchestration.sh               # Disable hooks only (fastest)
./scripts/disable-all-orchestration-with-branch-sync.sh  # Full disable + sync main/scientific branches

# Enable Orchestration (hooks + env var)
./scripts/enable-all-orchestration.sh                # Enable hooks only (fastest)
./scripts/enable-all-orchestration-with-branch-sync.sh   # Full enable + sync main/scientific branches

# Hook-Only Control
./scripts/disable-orchestration-hooks.sh             # Disable git hooks without env var
./scripts/restore-orchestration-hooks.sh             # Restore hooks from backup
```

### Git Hooks Verification

```bash
# Verify hooks are installed and executable
ls -la .git/hooks/pre-commit .git/hooks/post-commit .git/hooks/post-merge

# Test hook execution (dry-run)
.git/hooks/pre-commit --dry-run                      # If script supports it

# View hook logs
tail -f .git/hooks.log 2>/dev/null                   # If logging configured
```

---

## Development Workflow on orchestration-tools

### 1. Starting Work

```bash
# Check orchestration status
echo "ORCHESTRATION_ENABLED: ${ORCHESTRATION_ENABLED:-active}"

# Pull latest (triggers post-merge hook)
git pull origin orchestration-tools

# Verify hooks ran without errors
git log -1 --format="%H %s"
```

### 2. Making Changes

**Important:** The pre-commit hook will run before commits. It may:
- Validate branch consistency
- Check specification compliance
- Prevent commits that violate orchestration rules

```bash
# Make your changes
# ... edit files ...

# Stage changes
git add <files>

# Commit (pre-commit hook runs automatically)
git commit -m "feat: description (orchestration-tools branch)"
```

### 3. Post-Commit Automation

The post-commit hook automatically:
- Syncs changes to `main` or `scientific` branches (if configured)
- Updates branch profiles
- Triggers specification compliance checks
- May create worktree updates

**Do not disable hooks** unless you understand the consequences for branch synchronization.

### 4. Handling Merge Conflicts

If you pull and encounter conflicts:

```bash
# post-merge hook will attempt resolution if spec exists
git pull origin orchestration-tools

# Check hook output
git status

# If hook auto-resolved: verify changes
git diff

# If hook couldn't resolve: 
git merge --abort  # to try again
# OR manually resolve conflicts per normal git workflow
```

---

## Branch Synchronization

### Understanding Branch Sync

The orchestration system maintains consistency across three branches:

- **orchestration-tools** (main development) ← your current branch
- **main** (production) ← auto-synced
- **scientific** (research) ← auto-synced

Changes you make on orchestration-tools may automatically propagate to these branches via post-commit hooks.

### Controlling Branch Sync

```bash
# Sync with full branch propagation
./scripts/enable-all-orchestration-with-branch-sync.sh

# Sync but don't auto-push
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push

# Disable sync (work on orchestration-tools only)
./scripts/disable-all-orchestration-with-branch-sync.sh

# Push after manual changes
git push origin orchestration-tools
git push origin main
git push origin scientific
```

---

## Key Files on orchestration-tools Branch

### Orchestration Core Files

```
scripts/bash/
├── disable-all-orchestration.sh          # Disable hooks + env var
├── disable-all-orchestration-with-branch-sync.sh  # Full disable + sync
├── enable-all-orchestration.sh           # Enable hooks + env var
├── enable-all-orchestration-with-branch-sync.sh   # Full enable + sync
├── disable-orchestration-hooks.sh        # Hooks only
├── restore-orchestration-hooks.sh        # Restore from backup
├── create-pr-resolution-spec.sh          # Generate conflict resolution specs
├── gh-pr-ci-integration.sh              # GitHub Actions integration
└── pr-test-executor.sh                  # Test PR changes

.git/hooks/
├── pre-commit                            # Validates before commits
├── post-commit                           # Syncs after commits
└── post-merge                            # Handles merge automation

Documentation Files
├── ORCHESTRATION_PROCESS_GUIDE.md        # Complete orchestration guide
├── ORCHESTRATION_IDE_QUICK_REFERENCE.md  # IDE-specific quick ref
├── ORCHESTRATION_IMPLEMENTATION_SUMMARY.md # Architecture overview
├── ORCHESTRATION_CONTROL_MODULE.md       # Control system details
└── ORCHESTRATION_DOCS_INDEX.md          # Documentation index
```

### EmailIntelligence CLI Integration

```
.emailintelligence/
├── config.yaml                          # Orchestration + CLI config
├── constitutions/                       # Spec-based resolution rules
└── strategies/                          # Conflict resolution strategies

emailintelligence_cli.py                # Main CLI - handles orchestration tasks
```

---

## Troubleshooting orchestration-tools Issues

### Hooks Not Running

```bash
# Verify hooks exist and are executable
test -x .git/hooks/pre-commit && echo "pre-commit: OK" || echo "pre-commit: FAILED"
test -x .git/hooks/post-commit && echo "post-commit: OK" || echo "post-commit: FAILED"
test -x .git/hooks/post-merge && echo "post-merge: OK" || echo "post-merge: FAILED"

# Restore hooks if missing
./scripts/restore-orchestration-hooks.sh

# Check orchestration is enabled
[ -z "$ORCHESTRATION_ENABLED" ] && echo "Orchestration: ACTIVE" || echo "Orchestration: $ORCHESTRATION_ENABLED"
```

### Branch Sync Not Working

```bash
# Check if branch sync scripts exist
test -f scripts/disable-all-orchestration-with-branch-sync.sh && echo "Branch sync: YES" || echo "Branch sync: NO"

# Check remote branches exist
git branch -r | grep -E "main|scientific"

# Test sync manually
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push
git status
```

### Conflict Resolution Failed

```bash
# Check if EmailIntelligence CLI is accessible
python emailintelligence_cli.py --help

# Verify constitutions exist
ls -la .emailintelligence/constitutions/

# Review orchestration logs
git log --oneline orchestration-tools | head -10

# Fallback to manual resolution
git merge --abort
# ... manually resolve conflicts ...
git add .
git commit -m "resolve: manual conflict resolution"
```

### ORCHESTRATION_ENABLED Env Var Issues

```bash
# Check current value
echo "Current: ${ORCHESTRATION_ENABLED:-empty (active)}"

# Clear if stuck
unset ORCHESTRATION_ENABLED

# Re-enable orchestration
./scripts/enable-all-orchestration.sh
```

---

## Important Notes for orchestration-tools Branch

### Do NOT

- ❌ Manually edit `.git/hooks/` files (use `restore-orchestration-hooks.sh` instead)
- ❌ Run `git filter-branch` or `git filter-repo` (conflicts with orchestration)
- ❌ Force-push to `orchestration-tools` without coordinating branch syncs
- ❌ Delete the `.emailintelligence/` directory (orchestration depends on it)
- ❌ Disable hooks permanently without understanding the impact

### Do

- ✅ Use the branch sync scripts for coordinated multi-branch updates
- ✅ Review hook output after commits (check for sync success)
- ✅ Keep constitutions in `.emailintelligence/constitutions/` current
- ✅ Test conflict resolution with `emailintelligence_cli.py` before problematic merges
- ✅ Reference `ORCHESTRATION_IDE_QUICK_REFERENCE.md` for IDE-specific setup

---

## Integration with Task Master

On the orchestration-tools branch, Task Master tasks (in `.taskmaster/`) are **not auto-committed**. Manage them separately:

```bash
# Work on tasks locally
task-master next
task-master show <id>
task-master set-status --id=<id> --status=done

# Orchestration commits only include:
# - src/ (application code)
# - scripts/bash/ (orchestration scripts)
# - Documentation updates (ORCHESTRATION_*.md, AGENTS*.md)
# - .emailintelligence/ (orchestration config)

# Task tracking remains local - do not include .taskmaster/ in branch commits
```

---

## Reference Documentation

For complete orchestration system details, see:

- `ORCHESTRATION_PROCESS_GUIDE.md` - Full orchestration workflow
- `ORCHESTRATION_IDE_QUICK_REFERENCE.md` - IDE integration quickstart
- `ORCHESTRATION_IMPLEMENTATION_SUMMARY.md` - Architecture and design
- `AGENTS.md` - Core agent integration guide (this file extends it)
- `ORCHESTRATION_DOCS_INDEX.md` - Complete documentation index

---

_Last updated: 2025-11-18_
_For orchestration-tools branch development_
