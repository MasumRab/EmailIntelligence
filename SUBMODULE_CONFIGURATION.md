# Git Submodule Configuration

## Overview

This project uses Git submodules and branch-based directories to manage specialized development:

1. **.taskmaster/** - Task Management and Orchestration (Git submodule, points to `taskmaster` branch)
2. **orchestration-tools/** - Orchestration Tools and Utilities (Regular directory from `orchestration-tools` branch, not a submodule)

## Submodule Details

### .taskmaster (Task Master AI)

- **Path**: `.taskmaster/`
- **Remote URL**: https://github.com/MasumRab/EmailIntelligence.git
- **Branch**: `taskmaster`
- **Purpose**: Provides task management, orchestration, and AI agent integration
- **Key Files**:
  - `AGENTS.md` - Agent integration guide
  - `CLAUDE.md` - Claude Code integration
  - `config.json` - Configuration file
  - `docs/` - Documentation
  - `GEMINI.md`, `IFLOW.md`, `LLXPRT.md` - AI tool integrations

### orchestration-tools (NOT a Submodule)

- **Path**: `orchestration-tools/`
- **Type**: Regular directory (checked out from `orchestration-tools` branch)
- **Branch**: `orchestration-tools`
- **Purpose**: Provides orchestration capabilities and tools
- **Note**: This is a regular directory, not a git submodule. It's a branch of the main repository that gets checked out in the working directory.
- **Key Files**: Tool definitions, scripts, and orchestration utilities

**Important**: The orchestration-tools directory is part of the main repository's branch structure, not a separate git submodule. To work with orchestration-tools changes, switch to the orchestration-tools branch.

## Usage

### Cloning with Submodules

```bash
# Clone the repository with all submodules
git clone --recurse-submodules https://github.com/MasumRab/EmailIntelligence.git

# Or if already cloned, initialize submodules
git submodule update --init --recursive
```

### Updating Submodules

```bash
# Fetch latest changes for all submodules
git submodule foreach git pull origin

# Update a specific submodule to latest commit on its branch
cd .taskmaster
git pull origin taskmaster
cd ..

cd orchestration-tools
git pull origin orchestration-tools
cd ..
```

### Working on Submodule Changes

```bash
# Make changes in a submodule
cd .taskmaster
git checkout -b feature/my-feature
# ... make changes ...
git add .
git commit -m "feat: description"
git push origin feature/my-feature
cd ..

# Update the parent repository's reference
git add .taskmaster
git commit -m "chore: update taskmaster submodule reference"
git push origin <your-branch>
```

### Checking Submodule Status

```bash
# Show all submodules and their status
git submodule status

# Show detailed submodule information
git config --file .gitmodules --list

# Check if submodules are at the correct commits
git submodule status --recursive
```

## Important Notes

### Submodule Independence

- Each submodule maintains its own git history
- Changes in a submodule do NOT affect the parent repository unless explicitly committed
- Submodules are pinned to specific commits; they don't automatically update

### Avoiding Common Issues

1. **Detached HEAD**: When checking out a submodule, you're on a detached HEAD (the pinned commit). To make changes, create a branch first: `git checkout -b my-branch`

2. **Stale Submodules**: Run `git submodule update --init --recursive` after pulling changes to ensure submodules are at the correct commits

3. **Protecting Key Files**: The following files in each submodule should NOT be deleted:
   - `.taskmaster/AGENTS.md`
   - `.taskmaster/CLAUDE.md`
   - `.taskmaster/CRUSH.md`
   - `.taskmaster/GEMINI.md`
   - `.taskmaster/IFLOW.md`
   - `.taskmaster/LLXPRT.md`
   - `.taskmaster/config.json`
   - `.taskmaster/docs/`

### .gitignore Configuration

Submodules are explicitly excluded from the `.gitignore` ignore-all rule (`.*`) with these exceptions:

```gitignore
!.gitmodules
!.taskmaster
!orchestration-tools
```

## Migration from Worktrees

Previously, this project used Git worktrees:
- `.taskmaster` was set up as a worktree
- Various feature branches had their own worktrees

**As of December 2025**, the setup has been migrated to use Git submodules instead of worktrees because:

1. **Better integration**: Submodules are part of git's standard workflow
2. **Cleaner history**: No worktree-specific branches cluttering the repository
3. **Easier collaboration**: Submodules are recognized by all git tools
4. **Simplified CI/CD**: Submodules integrate better with automation

### What Changed

- ✅ Removed: Git worktrees (`.taskmaster` as worktree, `taskmaster-worktree` setup)
- ✅ Added: Git submodules (`.taskmaster/`, `orchestration-tools/`)
- ✅ Updated: `.gitignore` to properly exclude/include submodules
- ⏳ To be updated: Documentation references to worktrees

### Cleanup

Old worktree setup files have been retained for reference but are no longer used:
- `scripts/sync_setup_worktrees.sh` - Deprecated (was for worktree sync)
- `WORKTREE_SETUP_INTEGRATION_GUIDE.md` - Archived
- `SUBTREE_TESTING_GUIDE.md` - Archived

## References

- [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Submodule Best Practices](https://github.blog/2016-02-01-working-with-submodules/)
