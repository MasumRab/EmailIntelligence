# Orchestration Distribution System - Modules

This directory contains the modular components of the centralized orchestration distribution system, designed following SOLID principles with each module having approximately 200 lines of code.

## Module Overview

### 1. distribute.sh
Handles the actual distribution of orchestration files from source to target branches.
- Distributes setup files, hooks, configurations, and scripts
- Synchronizes from remote orchestration-tools branch
- Manages the distribution workflow

### 2. validate.sh
Provides validation functions to ensure safe and correct distribution.
- Validates branch types and remote synchronization
- Checks file integrity and permissions
- Scans for large files and sensitive data
- Verifies required files exist

### 3. config.sh
Manages configuration loading and validation.
- Loads distribution configuration from JSON files
- Provides branch-specific configuration
- Validates configuration integrity
- Gets source files and target branches from config

### 4. logging.sh
Handles all logging and reporting functionality.
- Logs distribution events and validation results
- Creates distribution reports
- Provides user feedback and next steps
- Formats log messages consistently

### 5. branch.sh
Manages branch-specific operations and validations.
- Identifies branch types (orchestration-tools, taskmaster, etc.)
- Validates branch safety before operations
- Checks if branches are valid targets for distribution
- Handles branch switching and comparisons

### 6. safety.sh
Implements safety checks and protective measures.
- Checks for uncommitted files that might be lost
- Confirms destructive actions with user
- Preserves critical orchestration infrastructure
- Validates Task Master isolation
- Checks file permissions and disk space

### 7. utils.sh
Provides general utility functions used across modules.
- Gets git repository information
- Checks remote status
- Fixes file permissions
- Creates and restores backups
- Validates JSON files
- Manages temporary files

## Architecture Principles

### SOLID Compliance

1. **Single Responsibility Principle (SRP)**: Each module has a single, well-defined purpose.
2. **Open/Closed Principle (OCP)**: Modules are open for extension but closed for modification.
3. **Liskov Substitution Principle (LSP)**: All validation and distribution functions follow consistent interfaces.
4. **Interface Segregation Principle (ISP)**: Each module has specific, focused interfaces.
5. **Dependency Inversion Principle (DIP)**: Modules depend on abstractions (configuration) rather than concrete implementations.

### Usage

The main entry point `distribute-orchestration-files.sh` loads all modules and coordinates their functions based on command-line arguments. Each module exports its functions using `export -f` to make them available to other modules when sourced.

## Command Line Options

- `--dry-run`: Preview distribution without making changes
- `--sync-from-remote`: Pull latest from remote before distribution
- `--with-validation`: Run validation after distribution
- `--setup-only`: Distribute only setup files
- `--hooks-only`: Distribute only git hooks
- `--config-only`: Distribute only configuration files
- `--verify`: Run validation without distribution
- `--interactive`: Prompt for confirmation on major actions

## Safety Features

- Never removes `scripts/`, `setup/`, or `.taskmaster/` directories unless explicitly directed
- Always preserves orchestration infrastructure
- Warns about uncommitted files that might be lost
- Requires user confirmation for potentially destructive operations
- Validates Task Master worktree isolation