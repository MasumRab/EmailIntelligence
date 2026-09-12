# Task Master Submodule Integration Guide

## Overview

The `.taskmaster/` Git submodule provides task management and orchestration capabilities. This guide explains how it integrates with the orchestration-tools branch and other branches.

## Architecture

### Branch Configuration

**Orchestration-Tools Branch** (This Branch):
- ❌ `.taskmaster/` is NOT present
- ✅ Contains orchestration scripts, hooks, and setup utilities
- ✅ Pure orchestration focus

**Scientific, Main, and Other Development Branches**:
- ✅ `.taskmaster/` is present as a Git submodule
- Points to the `taskmaster` branch
- Contains task management, agent integration, and configuration

### Why This Structure?

1. **Separation of Concerns**:
   - Orchestration-tools: Infrastructure and tooling only
   - Development branches: Include task management via submodule

2. **Clean History**:
   - No submodule references in orchestration-tools
   - Other branches get full task management capabilities

3. **Flexibility**:
   - Work on orchestration without task management dependencies
   - Development branches have full task tracking

## Git Submodule Details

### Configuration

Located in `.gitmodules` on development branches (not in orchestration-tools):

```
[submodule ".taskmaster"]
  path = .taskmaster
  url = https://github.com/MasumRab/EmailIntelligence.git
  branch = taskmaster
```

### Files Included in .taskmaster

**Agent Integration**:
- `AGENTS.md` - Agent integration guide
- `CLAUDE.md` - Claude Code context
- `GEMINI.md` - Gemini integration
- `IFLOW.md` - IFLOW integration
- `LLXPRT.md` - LLXPRT integration
- `CRUSH.md` - CRUSH integration

**Configuration**:
- `config.json` - Task Master configuration
- `docs/` - Complete documentation
- `tasks/` - Task management system

## Working with Both Branches

### Scenario 1: Working on Orchestration-Tools

```bash
# Switch to orchestration-tools (submodule not present)
git checkout orchestration-tools

# Verify .taskmaster doesn't exist
ls -la .taskmaster  # Should fail - doesn't exist

# Work on orchestration scripts, hooks, etc.
# No task management needed here
```

### Scenario 2: Working on Development (scientific/main)

```bash
# Switch to scientific or main branch
git checkout scientific

# Initialize submodule if needed
git submodule update --init --recursive

# .taskmaster is now available
ls -la .taskmaster/
# AGENTS.md, CLAUDE.md, config.json, docs/ visible

# Use task management
task-master list
task-master show 1
```

### Scenario 3: Switching Between Branches

```bash
# On scientific branch with submodule
git checkout orchestration-tools
# .taskmaster directory disappears (normal behavior)
# Git removes the submodule reference

git checkout scientific
# .taskmaster directory reappears
# Submodule is restored
```

## Integration with Orchestration

### How They Work Together

1. **Orchestration-Tools Branch**:
   - Provides infrastructure, scripts, and hooks
   - Works standalone on orchestration tasks
   - No task management overhead

2. **Development Branches**:
   - Use orchestration tools for consistency
   - Also have task management via .taskmaster submodule
   - Hooks keep both synchronized

3. **Synchronization**:
   - Git hooks sync orchestration content to other branches
   - Task Master stays on taskmaster branch
   - Each branch maintains its own state

## Setting Up for Development

### First Clone (Get Everything)

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/MasumRab/EmailIntelligence.git

# This will:
# - Clone main repo
# - Initialize orchestration-tools branch content
# - Initialize .taskmaster submodule (on dev branches only)
```

### If Cloned Without Submodules

```bash
# Initialize submodules
git submodule update --init --recursive

# On orchestration-tools: no submodule to init (skipped)
# On scientific/main: .taskmaster submodule initialized
```

### Switching Between Branches

```bash
# From orchestration-tools to scientific
git checkout scientific

# Submodule automatically restored (Git handles this)
# .taskmaster/ appears with all content

# From scientific to orchestration-tools
git checkout orchestration-tools

# Submodule automatically removed (Git handles this)
# .taskmaster/ disappears
```

## Common Commands

### Check Status

```bash
# On a development branch (e.g., scientific)
git submodule status
# Output: <commit> .taskmaster (heads/taskmaster)

# On orchestration-tools
git submodule status
# Output: (empty - no submodules)
```

### Update Submodule

```bash
# Get latest taskmaster branch content
cd .taskmaster
git pull origin taskmaster
cd ..

# Update parent repository reference
git add .taskmaster
git commit -m "chore: update taskmaster submodule reference"
git push origin scientific
```

### View Submodule Configuration

```bash
# See all submodule settings
git config --file .gitmodules --list

# On orchestration-tools: empty
# On development branches: shows .taskmaster config
```

## Migration from Worktrees to Submodules

### What Changed

**Before** (Deprecated):
- `.taskmaster` was a Git worktree
- Cluttered `.git/worktrees/` directory
- Complex worktree synchronization

**Now** (Current):
- `.taskmaster` is a Git submodule
- Clean, standard Git feature
- Simpler branch switching
- Better CI/CD integration

### Why This Is Better

1. **Standard Git Feature**: Submodules are part of core Git
2. **Better CI/CD**: Automatic initialization with `--recurse-submodules`
3. **Cleaner History**: No worktree-specific branches
4. **Easier Collaboration**: Everyone uses same approach
5. **Simpler Switching**: Git handles it automatically

## Troubleshooting

### Submodule Not Updating

```bash
# Ensure you're on a dev branch
git branch
# Should show: scientific, main, etc. (NOT orchestration-tools)

# Then update
git submodule update --init --recursive
```

### Detached HEAD in Submodule

```bash
# This is normal when switching branches
# To fix, checkout the correct branch
cd .taskmaster
git checkout taskmaster
cd ..

# Parent repo will need update
git add .taskmaster
git commit -m "fix: restore taskmaster branch head"
```

### Can't Find .taskmaster

```bash
# Check which branch you're on
git branch

# If on orchestration-tools, .taskmaster won't exist - this is correct
# Switch to scientific/main to get it
git checkout scientific
```

### Merge Conflicts in .gitmodules

```bash
# This is rare but can happen
# View current state
git status

# Accept their version (usually safest)
git checkout --theirs .gitmodules

# Or manually edit to match:
[submodule ".taskmaster"]
  path = .taskmaster
  url = https://github.com/MasumRab/EmailIntelligence.git
  branch = taskmaster

# Then resolve
git add .gitmodules
git commit -m "resolve: fix .gitmodules merge conflict"
```

## Important Notes

⚠️ **Orchestration-Tools Branch**:
- `.taskmaster` is NOT present (by design)
- This branch is orchestration-focused only
- No task management needed here

✅ **Development Branches**:
- `.taskmaster` submodule available
- Full task management access
- Use `task-master` commands freely

✅ **Submodule Files ARE Protected**:
- Never delete files in `.taskmaster/`
- Don't modify taskmaster-specific configs
- Let Git manage submodule updates

## References

- **Main Configuration**: .gitmodules (in development branches)
- **Setup Guide**: FINAL_SETUP_STATUS.md
- **Quick Reference**: SUBMODULE_QUICK_START.md
- **Submodule Details**: SUBMODULE_CONFIGURATION.md
