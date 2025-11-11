# Orchestration Tools Branch

This branch (`orchestration-tools`) serves as the **central source of truth** for development environment tooling, configuration management, scripts, and Git hooks that ensure consistency across all project branches.

## Purpose

The primary goal is to keep the core email intelligence codebase clean by separating orchestration concerns from application code. This branch will **NOT** be merged with other branches, but instead provides essential tools and configurations that are synchronized to other branches via Git hooks.

## Files to KEEP (Essential for Orchestration)

### Orchestration Scripts & Tools
- `scripts/` - All orchestration scripts and utilities
  - `install-hooks.sh` - Installs Git hooks for automated environment management
  - `cleanup_orchestration.sh` - Removes orchestration-specific files when not on orchestration-tools
  - `sync_setup_worktrees.sh` - Synchronizes worktrees for different branches
  - `reverse_sync_orchestration.sh` - Reverse synchronization for orchestration updates
  - `cleanup.sh` - Cleanup utilities
  - `lib/` - Shared utility libraries (common.sh, error_handling.sh, git_utils.sh, logging.sh, validation.sh)
  - `hooks/` - Git hook source files (pre-commit, post-checkout, post-commit, post-merge, post-push)

### Setup & Environment Management
- `setup/` - Launch scripts and environment setup
  - `launch.py` - Main launcher with environment setup functionality
  - `pyproject.toml` - Python project configuration
  - `requirements.txt` - Runtime dependencies
  - `requirements-dev.txt` - Development dependencies
  - `setup_environment_*.sh` - Environment setup scripts
  - `launch.*` - Cross-platform launch scripts

### Configuration Files
- `.flake8`, `.pylintrc` - Python linting configuration
- `.gitignore`, `.gitattributes` - Git configuration
- `launch.py` (root wrapper) - Forwards to setup/launch.py (backward compatibility)

### Orchestration Documentation
- `docs/orchestration_summary.md` - Summary of orchestration workflow
- `docs/orchestration_validation_tests.md` - Validation tests for orchestration
- `docs/env_management.md` - Environment management documentation
- `docs/git_workflow_plan.md` - Git workflow planning
- `docs/current_orchestration_docs/` - All orchestration-specific documentation
- `docs/guides/` - Orchestration guides

## Files to REMOVE (Application-Specific)

The following files are NOT needed in this orchestration-focused branch and can be safely removed:

### Application Source Code
- `src/` - Application source code
- `modules/` - Application modules
- `backend/` - Backend implementation
- `client/` - Frontend implementation
- `tests/` - Application tests

### Application Data & Dependencies
- `data/` - Application data
- `node_modules/` - Node.js dependencies
- `performance_metrics_log.jsonl` - Runtime logs

### Application-Specific Configurations
- `.env.example` - Application environment example
- `.mcp.json` - MCP-specific configuration (if application-specific)
- `.rules` - Application-specific rules
- Any documentation files in `docs/` that are not orchestration-related

## Git Hook Behavior

### `pre-commit` Hook
- **Purpose**: Prevent accidental changes to orchestration-managed files
- **Behavior**: Allows all changes on orchestration-tools; warns on orchestration-managed file changes on other branches

### `post-checkout` Hook
- **Purpose**: Sync essential files when switching branches
- **Behavior**: Syncs setup/ directory, shared configs, and installs hooks when switching FROM orchestration-tools; skips sync when switching TO orchestration-tools

### `post-merge` Hook
- **Purpose**: Ensure environment consistency after merges
- **Behavior**: Syncs setup/ directory, installs/updates Git hooks, cleans up temporary worktrees

### `post-push` Hook
- **Purpose**: Detect orchestration changes and create PRs
- **Behavior**: Creates automatic draft PRs when orchestration-managed files are changed on non-orchestration branches

## Development Workflow

1. **For orchestration development**: Work directly in `orchestration-tools` branch
2. **For environment setup**: The `setup/` directory contains all necessary tools
3. **For configuration changes**: Make changes in orchestration-tools, they propagate automatically
4. **For Git hook management**: Use `install-hooks.sh` to install consistent hook versions

## Branch Policy

- **This branch will NOT be merged with other branches**
- **Focus only on orchestration tools, scripts, and configurations**
- **Remove application-specific files to keep the branch clean**
- **Maintain backward compatibility for the launch system**
- **Ensure all hooks and automation scripts work correctly**

## Hook Management and Updates

When making changes to orchestration files, follow these important steps:

1. **Always work in the orchestration-tools branch**
2. **Test your changes thoroughly**
3. **After pushing changes, other developers will receive updates automatically when switching branches**
4. **For immediate updates, run**: `scripts/install-hooks.sh --force`
5. **Refer to**: `docs/orchestration_hook_management.md` for detailed procedures

## Cleanup Strategy

To clean this branch for orchestration-only purposes:

```bash
# Remove application-specific directories
rm -rf src/
rm -rf modules/
rm -rf tests/
rm -rf data/
rm -rf backend/
rm -rf client/
rm -rf node_modules/

# Remove application-specific files
rm -f .env.example
rm -f .mcp.json
rm -f .rules
rm -f performance_metrics_log.jsonl

# Review docs/ and remove non-orchestration documentation
# (Keep orchestration_summary.md, orchestration_validation_tests.md, env_management.md, git_workflow_plan.md, and directories)
```

## Important Notes

- The root `launch.py` wrapper is essential and should be kept for backward compatibility
- The `setup/` directory is critical for environment setup and should be maintained
- All Git hooks in `scripts/hooks/` are essential for the orchestration workflow
- This branch serves as the single source of truth for all environment and tooling configurations
- Changes to orchestration-managed files require PRs through the automated system