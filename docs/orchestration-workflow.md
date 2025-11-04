# Orchestration Workflow Documentation

## Overview
The `orchestration-tools` branch serves as the central hub for development environment tooling and configuration management. It maintains scripts, hooks, and configurations that ensure consistency across all project branches while keeping the core email intelligence codebase clean.

## Current Workflow

### Branch Structure
- **orchestration-tools**: Contains all orchestration scripts, Git hooks, and shared configurations
- **Other branches** (main, scientific, etc.): Use synced versions of essential files for development

### Key Components

#### Scripts Directory (`scripts/`)
- `install-hooks.sh`: Installs Git hooks to `.git/hooks/` for automated environment management
- `cleanup_orchestration.sh`: Removes orchestration-specific files when not on orchestration-tools branch
- `currently_disabled/`: Archive of deprecated scripts (worktree and sync utilities)

#### Git Hooks (`scripts/hooks/`)
- `post-checkout`: Automatically syncs essential files from orchestration-tools to other branches and runs cleanup
- `post-commit-setup-sync`: Handles synchronization setup after commits
- `pre-commit`, `post-commit`, `post-merge`, `post-push`: Standard development workflow hooks

### Synchronization Logic
1. **On orchestration-tools branch**: All files present, full functionality available
2. **On other branches**: Post-checkout hook syncs canonical versions of:
   - Setup scripts (`setup/`)
   - Git hooks (`scripts/hooks/`)
   - Launch scripts (`launch.*`)
   - Configuration files (`.gitattributes`, `.gitignore`, `pyproject.toml`, `requirements.*`)
3. **Cleanup on branch switch**: When leaving orchestration-tools, cleanup removes:
   - `scripts/currently_disabled/` directory
   - Orchestration-specific hooks (`.git/hooks/post-commit-setup-sync`)

### Development Workflow
1. **Work on orchestration-tools**: Modify scripts, hooks, and shared configs here
2. **Switch to feature branches**: Automatic sync ensures consistent environment
3. **Return to orchestration-tools**: Cleanup prevents conflicts, full tools available
4. **Merge updates**: Changes to orchestration files propagate via sync mechanism

## Alignment with Project Goals
Score: 9/10

**Strengths:**
- Maintains clean separation between tooling and core email intelligence code
- Ensures consistent development environments across branches
- Automates environment setup and cleanup
- Supports scalable development workflow

**Areas for Improvement:**
- Consider documenting hook behaviors more explicitly
- Add validation for synced file integrity

## Usage
- Stay on `orchestration-tools` for script/hook development
- Switch branches normally - sync happens automatically
- Manual cleanup available via `scripts/cleanup_orchestration.sh`