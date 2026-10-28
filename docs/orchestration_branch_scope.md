# Orchestration Tools Branch - Clear Scope Definition

## ⚠️ IMPORTANT: BRANCH SCOPE

This branch (`orchestration-tools`) is **exclusively** for:
- Development environment tooling
- Configuration management
- Scripts and Git hooks for consistency
- **NOT** for application code or features

**This branch will NOT be merged with other branches.**

## Purpose & Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│                    BRANCH SEPARATION                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  orchestration-tools:         main/scientific/feature:      │
│  ┌─────────────────────┐     ┌────────────────────────┐    │
│  │ Orchestration Tools │     │ Application Code       │    │
│  │ - Setup Scripts     │     │ - Email Intelligence   │    │
│  │ - Git Hooks         │     │ - Features             │    │
│  │ - Configurations    │     │ - Tests                │    │
│  │ - Environment Mgmt  │     │ - Documentation        │    │
│  └─────────────────────┘     └────────────────────────┘    │
│                                                             │
│  These concerns are SEPARATED to keep each branch focused.  │
└─────────────────────────────────────────────────────────────┘
```

## What Files BELONG in This Branch

### ✅ KEEP: Core Orchestration Files

1. **Orchestration Scripts** (`scripts/`)
   - `install-hooks.sh` - Installs Git hooks consistently
   - `cleanup_orchestration.sh` - Removes orchestration files when needed
   - `sync_setup_worktrees.sh` - Synchronizes worktrees
   - `hooks/` - Git hook source files
   - `lib/` - Shared utility libraries

2. **Environment Setup** (`setup/`)
   - `launch.py` - Main launcher (essential for all branches)
   - `requirements*.txt` - Dependency management
   - `pyproject.toml` - Python configuration
   - Environment setup scripts

3. **Configuration Files**
   - `.flake8`, `.pylintrc` - Linting configuration
   - `.gitignore`, `.gitattributes` - Git configuration
   - Root `launch.py` wrapper (backward compatibility)

4. **Orchestration Documentation**
   - `docs/orchestration_summary.md`
   - `docs/orchestration_validation_tests.md`
   - `docs/env_management.md`
   - `docs/current_orchestration_docs/`
   - `docs/guides/`

## What Files DO NOT BELONG in This Branch

### ❌ REMOVE: Application-Specific Files

1. **Application Source Code**
   - `src/` - Email intelligence application code
   - `modules/` - Application modules
   - `backend/` - Backend implementation
   - `client/` - Frontend implementation

2. **Application Data & Dependencies**
   - `data/` - Email data, databases
   - `node_modules/` - Node.js dependencies
   - `tests/` - Application-specific tests

3. **Application Configurations**
   - `.env.example` - Application environment examples
   - Project-specific config files (tsconfig.json, package.json, etc.)
   - Runtime logs and temporary files

## Why This Separation Matters

### Benefits of Orchestration-Only Branch:
1. **Clean Focus**: Only environment and tooling concerns
2. **Consistent Setup**: All developers get identical environment tools
3. **Automated Management**: Git hooks handle synchronization
4. **Reduced Conflicts**: No application code to merge
5. **Clear Ownership**: Orchestration tools have single source of truth

### What Other Branches Get:
```
When you switch to main/scientific/feature branches:
├── You get essential setup tools (synced from orchestration-tools)
├── You get consistent Git hooks (installed from orchestration-tools)
├── You get proper environment configuration (synced)
└── You DON'T get orchestration source code (scripts/, etc.)
```

## Cleanup Checklist

Before committing to this branch, ensure:

- [ ] No application source code (`src/`, `modules/`, etc.)
- [ ] No application data (`data/`, `node_modules/`, etc.)
- [ ] No application tests (`tests/`)
- [ ] No application-specific configurations
- [ ] All orchestration tools are present and functional
- [ ] Documentation is clear about this branch's scope
- [ ] Git hooks work correctly
- [ ] Environment setup scripts function properly

## Key Principle

> **This branch = Development Environment Tools**
> **Other branches = Application Features**

Never mix these concerns. If you need to work on application features, do it in the appropriate application branch.

## Emergency Cleanup Command

If this branch accidentally accumulates application files:

```bash
# Remove application-specific content
rm -rf src/ modules/ tests/ data/ backend/ client/ node_modules/

# Remove application-specific configs
rm -f .env.example .mcp.json .rules performance_metrics_log.jsonl

# Verify only orchestration tools remain
ls -la  # Should show: scripts/, setup/, docs/, and config files only
```

This branch should contain only what's needed to set up and manage the development environment - nothing more.