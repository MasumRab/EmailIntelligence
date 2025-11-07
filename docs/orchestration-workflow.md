# Orchestration Workflow Documentation

## Overview

The `orchestration-tools` branch serves as the central hub for development environment tooling and configuration management. It maintains scripts, hooks, and configurations that ensure consistency across all project branches while keeping the core email intelligence codebase clean.

## Launch System Architecture

The EmailIntelligence project uses a modern command pattern architecture for its launch system, providing a clean, extensible way to manage development environments and application lifecycle.

### Command Pattern Structure

```
setup/
├── launch.py                 # Main entry point with command routing
├── commands/                 # Command implementations
│   ├── command_interface.py  # Abstract base class for commands
│   ├── command_factory.py    # Factory for creating command instances
│   ├── setup_command.py      # Environment setup command
│   ├── run_command.py        # Application execution command
│   └── test_command.py       # Testing command
├── container.py              # Dependency injection container
├── environment.py            # Environment management
├── services.py               # Service orchestration
├── validation.py             # Input validation
├── utils.py                  # Shared utilities
└── test_stages.py            # Test execution logic
```

### Available Commands

#### `python launch.py setup`
**Purpose**: Set up the development environment
- Creates virtual environment (venv or conda)
- Installs Python dependencies via uv
- Downloads NLTK data
- Configures WSL environment (if applicable)
- Handles system-specific requirements

#### `python launch.py run`
**Purpose**: Run the EmailIntelligence application
- Starts all required services (backend, frontend, database)
- Provides development mode with hot reloading
- Manages service dependencies and startup order

#### `python launch.py test`
**Purpose**: Run comprehensive test suites
- Unit tests (`--unit`)
- Integration tests (`--integration`)
- End-to-end tests (`--e2e`)
- Performance tests (`--performance`)
- Security tests (`--security`)
- Coverage reporting (`--coverage`)

### Key Features

#### WSL Support
- Automatic WSL environment detection and setup
- WSL-specific dependency installation
- GPU acceleration configuration for WSL

#### Conda Integration
- Optional conda environment support
- Automatic conda environment creation and activation
- Fallback to venv if conda unavailable

#### Dependency Management
- Uses `uv` for fast Python package management
- Platform-specific requirements files
- CPU/GPU-specific dependency handling

#### Service Orchestration
- Parallel service startup
- Health checking and dependency validation
- Graceful shutdown handling

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
- `scripts/lib/` - Shared utility libraries
- `scripts/hooks/` - Hook source files
- `scripts/install-hooks.sh` - Hook installation script

### Files synced TO other branches (orchestration-managed):
- `setup/` - Launch scripts and environment setup (command pattern architecture)
- `docs/orchestration-workflow.md` - This documentation
- `.flake8`, `.pylintrc` - Python linting configuration
- `.gitignore`, `.gitattributes` - Git configuration

#### Setup Directory Structure (Orchestration-Managed):
```
setup/
├── launch.py              # Main launcher with command pattern
├── launch.bat             # Windows batch launcher
├── launch.sh              # Unix shell launcher
├── commands/              # Command implementations
├── container.py           # Dependency injection
├── environment.py         # Environment setup utilities
├── services.py            # Service orchestration
├── validation.py          # Input validation
├── utils.py               # Shared utilities
├── test_stages.py         # Test execution
├── project_config.py      # Project configuration
├── pyproject.toml         # Python project configuration
├── requirements*.txt      # Platform-specific requirements
└── README.md              # Setup documentation
```

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

### "Scripts directory shouldn't be in main branch"
**Cause**: Orchestration tooling was accidentally committed to main
**Fix**: Remove scripts/ from main, ensure only orchestration-tools has it

### "Pre-commit warns about tsconfig.json changes"
**Cause**: tsconfig.json is incorrectly marked as orchestration-managed
**Fix**: tsconfig.json is project-specific, warnings should not appear

### "Post-checkout syncs too many files"
**Cause**: Hook syncing orchestration source files to other branches
**Fix**: Only sync essentials (setup/, shared configs), not tooling

## Usage

### Launch System Commands

```bash
# Set up development environment
python launch.py setup

# Set up with conda instead of venv
python launch.py setup --use-conda --conda-env emailintelligence

# Run the application
python launch.py run

# Run in development mode
python launch.py run --dev

# Run specific test suites
python launch.py test --unit
python launch.py test --integration
python launch.py test --e2e
python launch.py test --coverage

# Legacy usage (still supported)
python launch.py --setup
```

### Development Workflow

- **For orchestration development**: Work in `orchestration-tools` branch
- **For feature development**: Use main/scientific branches, orchestration-managed files will sync automatically
- **For configuration changes**: Make changes in orchestration-tools, they propagate via sync
- **For project-specific changes**: Edit directly in feature branches (no PR required)

### Environment Setup

The launch system automatically handles:
- **Python version validation** (requires Python 3.8+)
- **Virtual environment creation** (venv or conda)
- **Dependency installation** via uv package manager
- **WSL environment detection** and configuration
- **Platform-specific requirements** (Linux/Windows/macOS)
- **GPU/CPU-specific dependencies** based on hardware