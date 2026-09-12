# Centralized Orchestration Distribution System

## Overview
This system replaces the distributed file distribution logic previously scattered across git hooks with a centralized, SOLID-compliant orchestration distribution script. The system follows a modular architecture with a single main entry point and multiple specialized modules.

## Architecture

### Main Components
- **Main Entry Point**: `scripts/distribute-orchestration-files.sh` (~50 lines)
- **Modules Directory**: `modules/` containing 7 specialized modules (~200 lines each)

### Module Breakdown
1. **distribute.sh**: Handles file distribution operations
2. **validate.sh**: Performs validation checks
3. **config.sh**: Manages configuration loading and validation
4. **logging.sh**: Handles logging and reporting
5. **branch.sh**: Manages branch-specific operations
6. **safety.sh**: Implements safety checks and protections
7. **utils.sh**: Provides general utility functions

## SOLID Principles Implementation

### 1. Single Responsibility Principle (SRP)
Each module has a single, well-defined responsibility:
- Distribution module: Handle file distribution only
- Validation module: Handle validation checks only
- Configuration module: Handle configuration and settings only
- Logging module: Handle logging and tracking only
- Branch module: Handle branch-specific logic only
- Safety module: Handle safety checks and protections only
- Utility module: Handle general utility functions only

### 2. Open/Closed Principle (OCP)
The system is open for extension but closed for modification:
- New validation rules can be added via configuration
- New branch types can be supported through configuration
- New distribution targets can be added via configuration

### 3. Liskov Substitution Principle (LSP)
All validation and distribution functions follow consistent interfaces with standard exit codes.

### 4. Interface Segregation Principle (ISP)
Each module has specific, focused interfaces with only necessary functions exported.

### 5. Dependency Inversion Principle (DIP)
The system depends on configuration abstractions rather than hardcoded values.

## Usage

### Command Line Options
- `--dry-run`: Preview distribution without making changes
- `--sync-from-remote`: Pull latest from remote before distribution
- `--with-validation`: Run validation after distribution
- `--setup-only`: Distribute only setup files
- `--hooks-only`: Distribute only git hooks
- `--config-only`: Distribute only configuration files
- `--verify`: Run validation without distribution
- `--interactive`: Prompt for confirmation on major actions

### Examples
```bash
# Full distribution with validation
./scripts/distribute-orchestration-files.sh --sync-from-remote --with-validation

# Preview distribution
./scripts/distribute-orchestration-files.sh --dry-run

# Distribute only setup files
./scripts/distribute-orchestration-files.sh --setup-only
```

## Safety Features

### Orchestration Infrastructure Protection
- Never deletes `scripts/` directory unless explicitly requested
- Never deletes `setup/` directory unless explicitly requested
- Never deletes `.taskmaster/` worktree (preserves isolation)
- Always preserves orchestration-specific files

### User Confirmation System
- Warns about uncommitted files that might be lost
- Confirms potentially destructive operations
- Provides safety checks before major actions

## Configuration

The system uses `config/distribution.json` for configuration-driven behavior:
- Defines source and target branches
- Specifies distribution rules and validation settings
- Configures safety features and logging options

## File Preservation Policy

The system follows strict file preservation rules:
- **Always preserved**: `scripts/`, `setup/`, `.taskmaster/` directories
- **Never removed**: Unless explicitly directed by the user
- **Protected**: From accidental deletion during distribution

## Integration with Existing Workflows

- Aligns with Task Master workflows and documentation
- Maintains branch isolation requirements
- Supports existing orchestration processes
- Provides feedback aligned with project goals