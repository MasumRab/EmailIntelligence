# Orchestration Workflow Documentation

## Overview

⚠️ **SCOPE NOTE**: See [Orchestration Branch Scope](../orchestration_branch_scope.md) for a clear definition of what files belong in this branch.

The `orchestration-tools` branch serves as the central hub for development environment tooling and configuration management. It maintains scripts, hooks, and configurations that ensure consistency across all project branches while keeping the core email intelligence codebase clean.

**IMPORTANT**: This branch will NOT be merged with other branches. It exists solely as the source of truth for environment tools that are synchronized to other branches.

## Core Principle: Separation of Concerns

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  orchestration-tools branch:                                   │
│  ├─ Contains: Orchestration tooling & shared configs           │
│  └─ Purpose: Development environment management                │
│                                                                 │
│  main/scientific/feature branches:                              │
│  ├─ Contains: Core application code + synced essentials        │
│  └─ Purpose: Feature development & application logic           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## File Ownership Matrix

### Files ONLY in `orchestration-tools` branch:
- `scripts/` - All orchestration scripts and utilities
  - `install-hooks.sh`: Installs Git hooks to `.git/hooks/` for automated environment management
  - `cleanup_orchestration.sh`: Removes orchestration-specific files when not on orchestration-tools branch
- `scripts/lib/` - Shared utility libraries
- `scripts/hooks/` - Hook source files

### Files synced TO other branches (orchestration-managed):
- `setup/` - Launch scripts and environment setup
- `docs/orchestration-workflow.md` - Orchestration workflow documentation
- `docs/orchestration_summary.md` - Orchestration summary
- `docs/env_management.md` - Environment management documentation
- `.flake8`, `.pylintrc` - Python linting configuration
- `.gitignore`, `.gitattributes` - Git configuration
- `uv.lock` - Python dependency lock file

### Files that remain BRANCH-SPECIFIC (not orchestration-managed):
- `tsconfig.json` - TypeScript configuration
- `package.json` - Node.js dependencies
- `tailwind.config.ts` - Tailwind CSS configuration
- `vite.config.ts` - Vite build configuration
- `drizzle.config.ts` - Database configuration
- `components.json` - UI component configuration
- All application source code

## Hook Behavior Matrix

### pre-commit Hook
**Purpose**: Prevent accidental changes to orchestration-managed files

```
pre-commit Flow:
├── Check current branch
├── If orchestration-tools: Allow all changes
└── If other branch:
    ├── Warn about setup/ changes → Require PR
    ├── Warn about orchestration scripts → Require PR
    ├── Warn about shared configs (.flake8, .pylintrc, etc.) → Require PR
    └── Allow project-specific changes (tsconfig.json, package.json, etc.)
```

### post-commit Hook
**Purpose**: Trigger synchronization after orchestration changes

```
post-commit Flow:
├── Check current branch
├── If orchestration-tools:
│   └── Offer to run worktree sync
└── If other branch: No action
```

### post-merge Hook
**Purpose**: Ensure environment consistency after merges

```
post-merge Flow:
├── Skip if documentation worktree (docs-main, docs-scientific)
├── Sync setup/ directory
├── If main/scientific worktree:
│   ├── Create temp worktree from orchestration-tools
│   ├── Copy setup files and shared configs
│   └── Apply branch-specific configurations
├── Sync orchestration scripts (for reference)
├── Install/update Git hooks
└── Clean up temp worktree
```

### post-push Hook
**Purpose**: Detect orchestration changes and create PRs

```
post-push Flow:
├── Parse push information (local_sha → remote_sha)
├── If orchestration-tools pushed: Log completion
└── If other branch pushed:
    └── Check for orchestration-managed file changes
        ├── If changes detected: Create automatic draft PR
        └── If no changes: Continue normally
```

### post-checkout Hook
**Purpose**: Sync essential files when switching branches

```
post-checkout Flow:
├── Skip if switching TO orchestration-tools
├── Sync setup/ directory
├── Sync deployment/ directory (if exists)
├── Sync shared configuration files (.flake8, .pylintrc, etc.)
├── Sync documentation
├── Install/update Git hooks to .git/hooks/
└── DO NOT sync orchestration tooling (scripts/, etc.)
```

## Workflow Diagrams

### Branch Switching Workflow

```
User runs: git checkout main

post-checkout hook activates:
├── Current branch: main
├── Source branch: orchestration-tools
├── Actions:
│   ├── Sync setup/launch.py → main
│   ├── Sync .flake8 → main
│   ├── Install hooks to main/.git/hooks/
│   └── Skip: scripts/ (orchestration-only)
└── Result: main has clean environment + synced essentials

User runs: git checkout orchestration-tools

post-checkout hook activates:
├── Current branch: orchestration-tools
├── Source branch: main
├── Actions: NONE (skip sync on orchestration-tools)
└── Result: Full orchestration tooling available
```

### Development Workflow

```
Developer working on feature:

1. On main branch:
   ├── Edit: src/components/Button.tsx ✓ (project-specific)
   ├── Edit: tsconfig.json ✓ (branch-specific)
   ├── Edit: setup/launch.py ⚠️ (orchestration-managed)
   └── pre-commit: "WARNING: setup/ changes require PR"

2. Push to feature branch:
   ├── post-push detects setup/launch.py change
   ├── Creates automatic draft PR to orchestration-tools
   └── Developer reviews and merges PR

3. Merge orchestration changes:
   ├── post-merge syncs to all branches
   └── All worktrees get updated setup/launch.py
```

### File Synchronization Flow

```
orchestration-tools (source of truth)
├── setup/launch.py
├── .flake8
├── scripts/install-hooks.sh
└── scripts/hooks/pre-commit

↓ post-checkout syncs ↓

main/scientific branches
├── setup/launch.py ← synced
├── .flake8 ← synced
├── .git/hooks/pre-commit ← installed
└── scripts/ ← NOT synced (orchestration-only)
```

## Key Rules

1. **Orchestration-tools is the source of truth** for shared configurations
2. **Main/other branches get synced essentials** but not orchestration tooling
3. **Project-specific files stay branch-local** (no orchestration management)
4. **Hooks enforce PR process** for orchestration-managed file changes
5. **Post-merge ensures consistency** across all worktrees

## Troubleshooting

### "Scripts directory shouldn\'t be in main branch"
**Cause**: Orchestration tooling was accidentally committed to main
**Fix**: Remove scripts/ from main, ensure only orchestration-tools has it

### "Pre-commit warns about tsconfig.json changes"
**Cause**: tsconfig.json is incorrectly marked as orchestration-managed
**Fix**: tsconfig.json is project-specific, warnings should not appear

### "Post-checkout syncs too many files"
**Cause**: Hook syncing orchestration source files to other branches
**Fix**: Only sync essentials (setup/, shared configs), not tooling

## Canonical File List

This section lists the files and directories that are considered canonical for the `orchestration-tools` branch. This list should be updated if there are intentional changes to the files or directories that constitute the core of this branch\'s functionality.

### Core Orchestration Files:
*   `orchestration-workflow.md`: This documentation file.
*   `scripts/install-hooks.sh`: Script to install Git hooks.
*   `scripts/hooks/`: Directory containing Git hook scripts (e.g., `pre-commit`, `post-checkout`, etc.).
*   `setup/`: Directory for setup scripts and configurations.
*   `launch.*`: Files related to launching the application.
*   `.gitattributes`: Git attribute configurations.
*   `.gitignore`: Git ignore patterns.
*   `pyproject.toml`: Python project configuration.
*   `requirements.*`: Python dependency files (e.g., `requirements.txt`, `uv.lock`).

---

## Usage

- **For orchestration development**: Work in `orchestration-tools` branch
- **For feature development**: Use main/scientific branches, orchestration-managed files will sync automatically
- **For configuration changes**: Make changes in orchestration-tools, they propagate via sync
- **For project-specific changes**: Edit directly in feature branches (no PR required)
