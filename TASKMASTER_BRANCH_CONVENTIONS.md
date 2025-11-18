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

✅ **Must be in .gitignore:**
```gitignore
# Task Master worktree - should never be committed on orchestration-tools
.taskmaster/
```

❌ **Must NOT whitelist files from it:**
```gitignore
# WRONG - violates branch isolation
!.taskmaster/**
```

❌ **Must NOT create .taskmaster/.gitignore:**
- Worktree directories are working copies, not tracked
- Creating .gitignore inside worktree violates isolation principle
- Use root .gitignore to control what's tracked

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

### Impact

- TaskMaster worktree files would be tracked on orchestration-tools branch
- Branch isolation compromised
- Potential contamination of branch-specific configurations

## Prevention Checklist

Before committing to taskmaster or orchestration-tools branches:

- [ ] No `.taskmaster/` files added to git index
- [ ] `.gitignore` explicitly ignores `.taskmaster/` directory
- [ ] No `!.taskmaster/**` whitelist present
- [ ] No `.taskmaster/.gitignore` file exists
- [ ] Branch-specific configuration files present:
  - [ ] taskmaster: `.taskmaster/AGENTS.md`, `.taskmaster/config.json`
  - [ ] orchestration-tools: `AGENTS_orchestration-tools.md`, proper context profiles
- [ ] No orchestration files in taskmaster branch
- [ ] No .taskmaster references in orchestration-tools except in .gitignore
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

# Verify .taskmaster is ignored
git check-ignore -v .taskmaster/.gitignore

# Verify no taskmaster files in git index
git ls-files | grep -i taskmaster  # Should return nothing on orchestration-tools
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
