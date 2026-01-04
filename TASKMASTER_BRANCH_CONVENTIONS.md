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

✅ **Prevent commits via pre-commit hook (not .gitignore):**
```bash
# scripts/hooks/pre-commit
TASKMASTER_FILES=$(git diff --cached --name-only | grep "^\.taskmaster/" || true)
if [[ -n "$TASKMASTER_FILES" ]]; then
    echo "ERROR: Task Master worktree files cannot be committed"
    exit 1
fi
```

✅ **Must NOT be in .gitignore (allows agent access):**
- Keep `.taskmaster/` visible to agents/tools
- Not in `.gitignore`, not whitelisted with `!.taskmaster/**`
- Just left untracked naturally

✅ **Pre-commit hook propagates across clones:**
- Hook installed by `install-hooks.sh` on setup
- Consistent behavior across all clones
- Can't be bypassed accidentally

❌ **Must NOT whitelist files from it:**
```gitignore
# WRONG - would track taskmaster files in orchestration-tools
!.taskmaster/**
```

❌ **Must NOT create .taskmaster/.gitignore:**
- Worktree directories are working copies, not tracked
- Creating .gitignore inside violates isolation principle

**Key approach:**
- **Not in .gitignore**: Files visible to agents
- **Pre-commit hook checks**: Prevents commits, propagates via hook installation

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

**Fixed with pre-commit hook approach:**
- ✅ `.taskmaster/` remains visible to agents (not in .gitignore)
- ✅ Pre-commit hook rejects commits of `.taskmaster/` files
- ✅ Hook propagates via `install-hooks.sh` (consistent across clones)
- ✅ Branch isolation enforced without blocking agent access

## Prevention Checklist

Before committing to taskmaster or orchestration-tools branches:

- [ ] No `.taskmaster/` files added to git index
- [ ] `.taskmaster/` is NOT in `.gitignore` (preserves agent access)
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

# Verify .taskmaster is NOT in gitignore
git check-ignore -v .taskmaster/ || echo "✓ .taskmaster not in gitignore"

# Verify pre-commit hook is installed
ls -la .git/hooks/pre-commit

# Verify no taskmaster files in git index
git ls-files | grep -i taskmaster  # Should return nothing on orchestration-tools

# Test the hook by trying to stage and commit a taskmaster file
git add .taskmaster/config.json 2>/dev/null && git commit -m "test" 2>&1 | grep "ERROR"  # Should show error
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

**Git worktrees are completely independent clones of a branch.** The `.taskmaster/` worktree working directory should:

- Never be tracked on orchestration-tools branch
- Never have its files whitelisted in orchestration-tools .gitignore
- Never have its own .gitignore file
- Maintain complete separation from parent repository state

Violating these principles contaminates branch isolation and creates merge conflicts.
