# .taskmaster Worktree Configuration

## Overview

This project uses **Git worktrees** for managing the `.taskmaster/` directory. The `taskmaster` branch is checked out as a worktree at `.taskmaster/` within the main repository working directory.

**As of March 2026**, the setup has been migrated **back to Git worktrees** from the previous submodule approach (December 2025) because:

1. **Agent accessibility**: Worktrees are visible as regular directories; agents can read/access freely
2. **Simpler workflow**: No need for `git submodule update --init --recursive` after cloning
3. **Better isolation**: Pre-commit hooks enforce branch isolation without needing `.gitignore` tricks
4. **Natural integration**: Worktrees are lightweight and don't require special git commands for daily work

## Current Configuration

### .taskmaster (Git Worktree)

- **Path**: `.taskmaster/`
- **Branch**: `taskmaster` (remote: `origin/taskmaster`)
- **Repository**: Same repository (EmailIntelligence)
- **Purpose**: Task management, orchestration, and AI agent integration
- **Key Files**:
  - `AGENTS.md` - Agent integration guide
  - `CLAUDE.md` - Claude Code integration
  - `config.json` - Configuration file
  - `docs/` - Documentation
  - `GEMINI.md`, `IFLOW.md` - AI tool integrations

## Setup

### Initial Worktree Creation

```bash
# From the main repository directory
git worktree add .taskmaster origin/taskmaster
```

### Verify Setup

```bash
# List all worktrees
git worktree list

# Verify .taskmaster contents
ls -la .taskmaster/

# Verify branch isolation
cd .taskmaster && git log --oneline -5 && cd ..
```

### After Cloning (New Developer Setup)

```bash
# Clone the repository
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence

# Fetch all branches
git fetch origin

# Create the worktree
git worktree add .taskmaster origin/taskmaster

# Install hooks for isolation enforcement
./scripts/install-hooks.sh
```

## Branch Isolation

### How It Works

The `.taskmaster/` directory is a Git worktree and must **never** be committed on non-taskmaster branches:

1. **Pre-commit hook** blocks staging `.taskmaster/` files on other branches
2. **`.gitignore`** includes `.taskmaster/` to prevent accidental tracking
3. **Agents can read** `.taskmaster/` files freely (directory is visible on disk)

### Pre-Commit Hook Protection

```bash
# In scripts/hooks/pre-commit
TASKMASTER_FILES=$(git diff --cached --name-only | grep "^\.taskmaster/" || true)
if [[ -n "$TASKMASTER_FILES" ]]; then
    echo "ERROR: Task Master worktree files cannot be committed"
    echo "Use 'git restore --staged .taskmaster/' to unstage"
    exit 1
fi
```

## Working with the Worktree

### Making Changes to Task Master

```bash
# Enter the worktree
cd .taskmaster

# Create a branch for changes
git checkout -b feature/my-taskmaster-change

# Make changes, commit, push
git add .
git commit -m "feat: description"
git push origin feature/my-taskmaster-change

# Return to main repo
cd ..
```

### Updating to Latest

```bash
cd .taskmaster
git fetch origin
git checkout taskmaster
git pull origin taskmaster
cd ..
```

### Removing the Worktree

```bash
git worktree remove .taskmaster
```

## Important Notes

- `.taskmaster/` is listed in `.gitignore` — this is intentional (prevents tracking on non-taskmaster branches)
- The pre-commit hook provides a second layer of protection
- **DO NOT** remove `.taskmaster/` from `.gitignore`
- **DO NOT** create a `.gitmodules` file — submodules are no longer used
- Agents and tools can still access `.taskmaster/` files on disk despite `.gitignore`

## Migration History

| Date | Change | Reason |
|------|--------|--------|
| Pre-Dec 2025 | Git worktrees | Original approach |
| Dec 2025 | Git submodules | CI/CD integration (SUBMODULE_SETUP_SUMMARY.md) |
| Mar 2026 | Git worktrees (reverted) | Agent accessibility, simpler workflow |

## Deprecated Files

The following files document the previous submodule approach and are retained for historical reference:

- `SUBMODULE_SETUP_SUMMARY.md` — Documents the Dec 2025 submodule migration (now superseded)

## References

- [Git Worktrees Documentation](https://git-scm.com/docs/git-worktree)
- `TASKMASTER_BRANCH_CONVENTIONS.md` — Complete isolation requirements
- `TASKMASTER_ISOLATION_FIX.md` — Pre-commit hook approach details
