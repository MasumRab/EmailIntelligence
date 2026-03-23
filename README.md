
This branch (`orchestration-tools`) serves as the **central source of truth** for development environment tooling, configuration management, scripts, and Git hooks that ensure consistency across all project branches.

## Purpose

The primary goal is to keep the core email intelligence codebase clean by separating orchestration concerns from application code. This branch will **NOT** be merged with other branches, but instead provides essential tools and configurations that are synchronized to other branches via Git hooks.


### Orchestration Scripts & Tools
- `scripts/` - All orchestration scripts and utilities
  - `install-hooks.sh` - Installs Git hooks for automated environment management
  - `cleanup_orchestration.sh` - Removes orchestration-specific files when not on orchestration-tools
  - `sync_setup_worktrees.sh` - Synchronizes worktrees for different branches
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


### Deprecated or Redundant Files
- `.rules` - Application-specific rules (keep integration settings, remove app-specific rules)
- `.env.example` - Application environment example (keep shared environment config templates only)
- Old deployment configs or scripts unrelated to orchestration setup
- Any documentation files in `docs/` that are application-specific (not orchestration-related)

## Git Hook Behavior


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