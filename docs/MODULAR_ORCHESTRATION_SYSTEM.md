# Modular Orchestration Distribution System Documentation

## Overview

The Modular Orchestration Distribution System is a centralized, SOLID-principles-based system that replaces the previous distributed file distribution logic from git hooks. The system follows Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles.

## Architecture

The system consists of a main entry point (~50 lines) and 7 modular components (~200 lines each):

- **Main Entry Point**: `scripts/distribute-orchestration-files.sh` (~50 lines)
- **Configuration Module**: `modules/config.sh` - Handles configuration loading and validation
- **Validation Module**: `modules/validate.sh` - Performs validation checks
- **Distribution Module**: `modules/distribute.sh` - Handles file distribution operations
- **Logging Module**: `modules/logging.sh` - Handles logging and reporting
- **Branch Module**: `modules/branch.sh` - Manages branch-specific operations
- **Safety Module**: `modules/safety.sh` - Implements safety checks and protections
- **Utilities Module**: `modules/utils.sh` - Provides general utility functions

## Key Features

### 1. Distribution from Latest Remote
The script always distributes from the latest remote version of orchestration-tools* branches:
- Pulls latest changes from origin/orchestration-tools before distribution
- Verifies the commit hash is the latest before proceeding
- Warns if local version is outdated
- Provides option to update to latest before distribution

### 2. Orchestration Infrastructure Preservation
- **Scripts directory**: Never removes `scripts/` or contents unless explicitly directed
- **Task Master worktree**: Preserves `.taskmaster/` worktree (git handles isolation)
- **Setup directory**: Always preserves `setup/` and contents
- **Hooks**: Manages hooks through dedicated functions, never deletes arbitrarily

### 3. SOLID Principles Implementation

#### Single Responsibility Principle (SRP)
Each module and function has a single, well-defined responsibility:
- **Distribution module**: Handle file distribution only
- **Validation module**: Handle validation checks only
- **Configuration module**: Handle configuration and settings only
- **Logging module**: Handle logging and tracking only
- **Branch module**: Handle branch-specific logic only

#### Open/Closed Principle (OCP)
The script is open for extension but closed for modification:
- New validation rules can be added without modifying core distribution logic
- New branch types can be supported without changing existing code
- New distribution targets can be added via configuration

#### Liskov Substitution Principle (LSP)
All validation and distribution functions follow consistent interfaces:
- All validation functions return standard success/failure codes
- All distribution functions follow the same parameter pattern
- All branch-specific functions implement the same base interface

#### Interface Segregation Principle (ISP)
Each module has specific, focused interfaces:
- Distribution interface: only distribution methods
- Validation interface: only validation methods
- Configuration interface: only configuration methods

#### Dependency Inversion Principle (DIP)
The script depends on abstractions, not concrete implementations:
- Uses configuration files rather than hardcoded paths
- Interfaces with validation modules rather than specific checks
- Abstracts git operations for flexibility

## Usage

### Command Line Options

```bash
./scripts/distribute-orchestration-files.sh [options]
```

Options:
- `--dry-run`: Preview distribution without making changes
- `--sync-from-remote`: Pull latest from remote before distribution
- `--with-validation`: Run validation after distribution
- `--setup-only`: Distribute only setup files
- `--hooks-only`: Distribute only git hooks
- `--config-only`: Distribute only configuration files
- `--verify`: Run validation without distribution
- `--interactive`: Prompt for confirmation on major actions

### Example Usage

```bash
# Dry run to preview changes
./scripts/distribute-orchestration-files.sh --dry-run

# Sync from remote and distribute with validation
./scripts/distribute-orchestration-files.sh --sync-from-remote --with-validation

# Distribute only setup files
./scripts/distribute-orchestration-files.sh --setup-only

# Verify distribution targets without making changes
./scripts/distribute-orchestration-files.sh --verify
```

## Safety Features

### Orchestration Infrastructure Protection
- Never delete `.taskmaster/` worktree (preserve isolation)
- Never delete `scripts/` directory unless explicitly requested
- Always preserve `setup/` directory and contents
- Protect all orchestration-specific files

### User Confirmation System
- Warn about any potentially destructive operations
- Confirm before major distribution actions
- Allow user to review changes before applying

## Configuration-Driven Design

The system uses configuration files rather than hardcoded values:

```json
{
  "sources": {
    "orchestration-tools": {
      "remote": "origin/orchestration-tools",
      "directories": ["setup/", "scripts/hooks/", "scripts/lib/", "config/"],
      "files": [".flake8", ".pylintrc", ".gitignore", "launch.py"],
      "validation_script": "scripts/validate-orchestration-context.sh"
    }
  },
  "targets": {
    "orchestration-tools-*": {
      "allowed": true,
      "sync_method": "git-worktree-safe",
      "validation_after_sync": true
    },
    "taskmaster-*": {
      "allowed": false,
      "reason": "worktree-isolation-required"
    },
    "other": {
      "allowed": false,
      "reason": "orchestration-not-applicable"
    }
  },
  "validation_rules": {
    "large_file_threshold": 52428800,
    "sensitive_patterns": ["password", "secret", "key", "token"],
    "required_files": ["scripts/install-hooks.sh", "setup/launch.py"]
  }
}
```

## Testing

The system includes comprehensive test suites for each module:
- `tests/modules/test_config_module.sh` - Tests for configuration module
- `tests/modules/test_validate_module.sh` - Tests for validation module
- `tests/modules/test_distribute_module.sh` - Tests for distribution module
- `tests/modules/test_safety_module.sh` - Tests for safety module
- `tests/modules/test_other_modules.sh` - Tests for utils, branch, and logging modules

Run all tests with:
```bash
bash tests/modules/run_all_module_tests.sh
```

## Migration from Previous System

The system migrates from the previous distributed hook-based approach:
- All distribution logic removed from git hooks
- All validation functions preserved and enhanced
- Orchestration infrastructure protection implemented
- Task Master worktree isolation maintained
- User feedback aligned with project goals

## Maintenance

### Updating the System
- Modify individual modules following SRP
- Add new validation rules via configuration (OCP)
- Extend functionality through configuration rather than code changes (DIP)
- Maintain consistent interfaces across modules (LSP, ISP)

### Troubleshooting
- Check configuration files for correct paths and settings
- Verify remote connectivity before distribution
- Review safety warnings before proceeding with destructive operations
- Use `--dry-run` option to preview changes before applying

## Best Practices

1. **Follow SOLID principles** when extending functionality
2. **Use configuration** rather than hardcoded values
3. **Maintain single responsibility** in each module
4. **Preserve orchestration infrastructure** during operations
5. **Validate before distributing** to prevent errors
6. **Test changes** using the comprehensive test suite
7. **Use safety features** to protect critical files