# Orchestration Tools Branch

This branch (`orchestration-tools`) serves as the **central source of truth** for development environment tooling, configuration management, scripts, and Git hooks that ensure consistency across all project branches.

## Purpose

The primary goal is to keep the core email intelligence codebase clean by separating orchestration concerns from application code. This branch will **NOT** be merged with other branches, but instead provides essential tools and configurations that are synchronized to other branches via Git hooks.

## Files to KEEP (Essential for Orchestration)

### Orchestration Scripts & Tools
- `scripts/` - All orchestration scripts and utilities
  - `install-hooks.sh` - Installs Git hooks for automated environment management
  - `cleanup_orchestration.sh` - Removes orchestration-specific files when not on orchestration-tools
  - `reverse_sync_orchestration.sh` - Reverse synchronization for orchestration updates
  - `cleanup.sh` - Cleanup utilities
  - `handle_stashes.sh` - Automated stash resolution for multiple branches
  - `stash_analysis.sh` - Analyze stashes and provide processing recommendations
  - `stash_details.sh` - Show detailed information about each stash
  - `interactive_stash_resolver.sh` - Interactive conflict resolution for stashes
  - `stash_manager.sh` - Main interface for all stash operations (deprecated, use optimized version)
  - `stash_manager_optimized.sh` - Optimized main interface with improved performance
  - `handle_stashes_optimized.sh` - Optimized automated stash resolution for multiple branches
  - `stash_analysis.sh` - Analyze stashes and provide processing recommendations
  - `stash_details.sh` - Show detailed information about each stash
  - `interactive_stash_resolver_optimized.sh` - Optimized interactive conflict resolution for stashes
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

### Agent Context & Development Environment Files
- `AGENTS.md` - Task Master and agent integration guide
- `CLAUDE.md` - Claude Code auto-loaded context and MCP configuration
- `.claude/` - Claude Code integration directory (settings, custom commands)
- `.mcp.json` - MCP server configuration for agent tools integration
- `.context-control/profiles/` - Context profiles for branch-specific agent access control
- `.specify/` - Agent specification and rule files
- **Note on .taskmaster**: This is a Git submodule managed on other branches (scientific, main) that points to the taskmaster branch. It is NOT present on orchestration-tools branch. See TASKMASTER_SUBMODULE_INTEGRATION.md for details.

### Orchestration Documentation
- `docs/orchestration_summary.md` - Summary of orchestration workflow
- `docs/orchestration_validation_tests.md` - Validation tests for orchestration
- `docs/env_management.md` - Environment management documentation
- `docs/git_workflow_plan.md` - Git workflow planning
- `docs/stash_resolution_procedure.md` - Basic procedure for resolving stashes
- `docs/complete_stash_resolution_procedure.md` - Complete procedure with all details
- `docs/interactive_stash_resolution.md` - Guide to using interactive conflict resolution
- `docs/stash_management_tools.md` - Comprehensive guide to stash management tools
- `docs/stash_scripts_improvements.md` - Summary of improvements made to stash scripts
- `docs/current_orchestration_docs/` - All orchestration-specific documentation
- `docs/guides/` - Orchestration guides

## Files to REMOVE (Application-Specific)

The following files are NOT needed in this orchestration-focused branch and can be safely removed:

### Application Source Code
- `src/` - Application source code (except `src/core/` if shared with core utilities)
- `modules/` - Application modules
- `backend/` - Backend implementation
- `client/` - Frontend implementation
- `tests/` - Application tests
- `plugins/` - Plugin implementations

### Application Data & Dependencies
- `data/` - Application data
- `node_modules/` - Node.js dependencies
- `performance_metrics_log.jsonl` - Runtime logs
- `.venv/` - Virtual environment (will be recreated)
- `venv/` - Alternative virtual environment directory

### Deprecated or Redundant Files
- `.rules` - Application-specific rules (keep integration settings, remove app-specific rules)
- `.env.example` - Application environment example (keep shared environment config templates only)
- Old deployment configs or scripts unrelated to orchestration setup
- Any documentation files in `docs/` that are application-specific (not orchestration-related)

## Git Hook Behavior

### `pre-commit` Hook
- **Purpose**: Prevent accidental changes to orchestration-managed files
- **Behavior**: Allows all changes on orchestration-tools; warns on orchestration-managed file changes on other branches

### `post-checkout` Hook
- **Purpose**: Sync essential files when switching branches
- **Behavior**: Syncs setup/ directory, shared configs, and installs hooks when switching FROM orchestration-tools; skips sync when switching TO orchestration-tools

### `post-merge` Hook
- **Purpose**: Ensure environment consistency after merges
- **Behavior**: Syncs setup/ directory, installs/updates Git hooks

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

To clean this branch for orchestration-only purposes, follow this comprehensive cleanup guide:

### Phase 1: Remove Application Code
```bash
# Remove application source directories
rm -rf src/backend/ src/core/ src/frontend/  # Keep only src/context_control if shared
rm -rf modules/
rm -rf tests/
rm -rf plugins/
```

### Phase 2: Remove Application Data & Runtime Files
```bash
# Remove runtime artifacts
rm -rf data/
rm -rf node_modules/
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf .venv/ venv/
rm -f performance_metrics_log.jsonl
rm -f *.db *.sqlite*
```

### Phase 3: Clean Documentation
```bash
# Keep orchestration docs, remove application-specific documentation
# Keep: docs/orchestration_*.md, docs/env_management.md, docs/git_workflow_plan.md, 
#       docs/stash_*.md, docs/guides/, docs/current_orchestration_docs/
# Remove application-specific docs and READMEs from feature/module directories
```

### Phase 4: Clean Configuration Files
```bash
# Keep MCP, Claude, and context control configs (for agent integration)
# Keep: .mcp.json, .claude/, AGENTS.md, CLAUDE.md, .context-control/profiles/, .specify/, .taskmaster/

# Remove application-specific configs
rm -f .env.example  # (or keep only shared templates)
rm -f deployment/docker-compose*.yml  # Unless essential for orchestration
rm -f nginx/  # Remove unless used for setup
```

### Phase 5: Documentation Review
After cleanup, run:
```bash
git status --short
# Review remaining files to ensure all are orchestration-related
# Run: git rm --cached <file> to untrack files, then commit
```

### Important: Preserve Agent Integration Context
When cleaning, **DO NOT REMOVE** these files as they are essential for:
- Automated task management with Task Master
- Claude Code context and MCP tool integration
- Branch-specific agent access control
- Development environment consistency

Keep:
- `AGENTS.md` - Essential for agent workflow documentation
- `CLAUDE.md` - Auto-loaded context for AI development tools
- `.claude/` - Custom slash commands and tool configurations
- `.mcp.json` - MCP server configuration for orchestration tools
- `.context-control/` - Context profiles ensuring agents have appropriate access per branch
- `.specify/` - Agent specifications and behavioral rules
- `.taskmaster/` - Task tracking and orchestration task management

## Important Notes

- The root `launch.py` wrapper is essential and should be kept for backward compatibility
- The `setup/` directory is critical for environment setup and should be maintained
- All Git hooks in `scripts/hooks/` are essential for the orchestration workflow
- This branch serves as the single source of truth for all environment and tooling configurations
- Changes to orchestration-managed files require PRs through the automated system
- Agent context files (AGENTS.md, CLAUDE.md, .claude/, .mcp.json, .context-control/, .specify/, .taskmaster/) are CRITICAL for maintaining agent integration and should always be preserved
- These agent integration files are synchronized across all branches via the post-checkout hook to ensure consistent agent access control and task management
- Context control profiles ensure agents have appropriate access per branch (e.g., scientific branch agents don't see orchestration scripts)
- Task Master configurations are used for centralized task tracking and workflow automation across branches