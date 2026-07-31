# Task Master Branch Orchestration Conventions

## Overview

The `taskmaster` branch is a **separate, isolated development environment** designed specifically for Task Master AI integration. It must maintain strict separation from `orchestration-tools` and other branches to prevent contamination.

## Critical Requirements

### 1. Branch Isolation - NO Orchestration Files

The taskmaster branch must **never include** orchestration infrastructure:

- ❌ `.specify/` - Orchestration-specific rules
- ❌ `.gemini/` - IDE-specific orchestration
- ❌ `.qwen/` - IDE-specific orchestration  
- ❌ `.kilo/` - IDE-specific orchestration
- ❌ `.roo/` - IDE-specific orchestration
- ❌ `.clinerules/` - Cursor IDE orchestration rules
- ❌ `.cursor/rules/orchestration-tools/` - Branch-specific Cursor rules
- ❌ `.windsurf/` - Branch-specific Windsurf rules
- ❌ `deployment/orchestration-tools*` - Orchestration deployment
- ❌ Orchestration hook scripts
- ❌ `.context-control/profiles/orchestration-tools.json`

### 2. Worktree Isolation - .taskmaster Directory

The `.taskmaster/` directory is a **git worktree**, not a regular directory:

✅ **Defense in depth — two layers of protection:**

**Layer 1: `.gitignore` contains `.taskmaster/`**
- Prevents `git add .` or `git add -A` from staging worktree files
- Standard across all branches (`main`, `scientific`, `orchestration-tools`)
- Agents can still read `.taskmaster/` on disk — `.gitignore` only affects git tracking

**Layer 2: Pre-commit hook blocks commits**
```bash
# scripts/hooks/pre-commit
TASKMASTER_FILES=$(git diff --cached --name-only | grep "^\.taskmaster/" || true)
if [[ -n "$TASKMASTER_FILES" ]]; then
    echo "ERROR: Task Master worktree files cannot be committed"
    exit 1
fi
```

✅ **Pre-commit hook propagates across clones:**
- Hook source lives at `scripts/hooks/pre-commit`
- Installed by `install-hooks.sh` on setup
- Catches explicit `git add .taskmaster/file` even if `.gitignore` is bypassed

❌ **Must NOT whitelist files from it:**
```gitignore
# WRONG - would track taskmaster files on non-taskmaster branches
!.taskmaster/**
```

❌ **Must NOT create .taskmaster/.gitignore:**
- Worktree directories are working copies, not tracked
- Creating .gitignore inside violates isolation principle

**Key approach:**
- **In `.gitignore`**: Prevents accidental staging (agents can still read files on disk)
- **Pre-commit hook**: Catches any remaining staging attempts as a safety net

### 3. .gitignore Rules - Clean Whitelisting

Only whitelist files/directories that should exist on **this specific branch**:

```gitignore
# ✅ CORRECT - Whitelisted files belong on this branch
!.github/
!.flake8
!.pylintrc
!.claude/

# ❌ WRONG - These don't belong on orchestration-tools
!.taskmaster/**
!.kilo/**
```

### 4. Configuration Files

Orchestration-tools branch must use **orchestration-specific** configuration:

✅ `.context-control/profiles/orchestration-tools.json` - Orchestration context
❌ Mixed context profiles from multiple branches

### 5. Documentation

Branch-specific guidance must be clearly separated:

✅ `AGENTS_orchestration-tools.md` - Orchestration-tools branch guidance
✅ `.taskmaster/AGENTS.md` - Task Master guidance (in taskmaster branch)
❌ Mixing guidance in single AGENTS.md

## Violations in Previous Commit

The commit to taskmaster branch violated several requirements:

1. **Whitelist violation**: Added `!.taskmaster/**` to orchestration-tools .gitignore
2. **Worktree isolation violation**: Created `.taskmaster/.gitignore` file
3. **Merge conflict**: Unresolved `<<<<<<< HEAD` in .taskmaster/.gitignore
4. **Configuration mixing**: Orchestration files included in taskmaster branch state

### Impact & Resolution

- ❌ TaskMaster worktree files would have been tracked on orchestration-tools branch
- ❌ Branch isolation compromised  
- ❌ Potential contamination of branch-specific configurations

**Fixed with defense-in-depth approach:**
- ✅ `.taskmaster/` in `.gitignore` prevents accidental staging (agents can still read on disk)
- ✅ Pre-commit hook rejects commits of `.taskmaster/` files as a safety net
- ✅ Hook propagates via `install-hooks.sh` (consistent across clones)
- ✅ Branch isolation enforced without blocking agent access

## Prevention Checklist

Before committing to taskmaster or orchestration-tools branches:

- [ ] No `.taskmaster/` files added to git index
- [ ] `.taskmaster/` IS in `.gitignore` (prevents accidental staging)
- [ ] No `!.taskmaster/**` whitelist in .gitignore
- [ ] No `.taskmaster/.gitignore` file exists
- [ ] Pre-commit hook installed (via `scripts/install-hooks.sh`)
- [ ] Pre-commit hook checks for `.taskmaster/` files
- [ ] Branch-specific configuration files present:
  - [ ] taskmaster: `.taskmaster/AGENTS.md`, `.taskmaster/config.json`
  - [ ] orchestration-tools: `AGENTS_orchestration-tools.md`, proper context profiles
- [ ] No orchestration files in taskmaster branch
- [ ] All merge conflicts resolved (no `<<<<<<<`)

## Command Reference

### Setup Task Master Worktree

```bash
# Create worktree (from main branch)
git worktree add .taskmaster taskmaster

# Verify isolation
cd .taskmaster
git log --oneline | head -5
cd ..
```

### Verify Branch Isolation

```bash
# Check what would be tracked on current branch
git status

# Verify .taskmaster IS in gitignore (defense in depth)
git check-ignore -v .taskmaster/ && echo "✓ .taskmaster in gitignore"

# Verify pre-commit hook is installed
ls -la .git/hooks/pre-commit

# Verify no taskmaster files in git index
git ls-files | grep -i taskmaster  # Should return nothing on non-taskmaster branches

# Test the hook by trying to force-stage and commit a taskmaster file
git add -f .taskmaster/config.json 2>/dev/null && git commit -m "test" 2>&1 | grep "ERROR"  # Should show error
```

### Fix Violations

```bash
# Remove accidentally tracked taskmaster files
git rm --cached .taskmaster/**
git restore --staged .gitignore

# Reset to correct state
git reset HEAD~1  # If just committed

# Verify status
git status
```

## Related Documentation

- `AGENTS.md` - Main agent integration guide (applies to both branches)
- `AGENTS_orchestration-tools.md` - Orchestration-tools specific guidance
- `.taskmaster/AGENTS.md` - Task Master specific guidance (taskmaster branch only)
- `BRANCH_UPDATE_PROCEDURE.md` - Proper branch update process
- `.context-control/profiles/orchestration-tools.json` - Orchestration context config

## Key Principle

**Git worktrees are completely independent checkouts of a branch.** The `.taskmaster/` worktree working directory should:

- Be listed in `.gitignore` on all non-taskmaster branches (prevents accidental staging)
- Be protected by a pre-commit hook (catches force-adds as a safety net)
- Never have its files whitelisted with `!.taskmaster/**` in .gitignore
- Never have its own .gitignore file
- Maintain complete separation from parent repository state

Agents and tools can still read `.taskmaster/` files on disk — `.gitignore` only affects git tracking, not filesystem visibility.
