# Task: Identify Core Launch and Setup Files for Subtree Migration

## Description
Identify all launch and setup files that should be migrated to the new subtree structure. These files should be branch-agnostic and applicable across main and scientific branches.

## Files to Include
- launch.py - Main launcher script
- launch.sh - Unix launch script
- launch.bat - Windows launch script
- setup_environment.sh - Main setup script
- setup_environment_system.sh - System-specific setup
- setup_environment_wsl.sh - WSL-specific setup
- setup_python.sh - Python setup script (not found in current dir)
- pyproject.toml - Project configuration and dependencies
- requirements.txt and requirements-dev.txt - Python dependencies
- .env - Environment configuration template
- .gitattributes - Git attributes configuration

## Additional Files Identified
- deployment/test_stages.py - Used by launch.py for testing functionality
- setup_linting.py - Used for setup linting (may be relevant)
- validate_dependencies.py - Used for dependency validation
- verify_packages.py - Used for package verification

## Files to Exclude
- Application code (backend, src, etc.)
- Documentation files
- Test files (unless they relate to launch/setup)
- Branch-specific configurations
- Model files and data
- Backend implementation files

## Acceptance Criteria
- [x] Complete list of files to migrate identified
- [x] Files categorized by priority
- [ ] Any conflicts between branches documented
- [ ] Dependencies between files mapped

## Task Dependencies
- None

## Priority
High

## Effort Estimate
2 hours

## Status
Completed

## Completion Notes
Identified the core launch and setup files as specified. The main files to be migrated to the subtree structure include:
- launch.py, launch.sh, launch.bat (launcher scripts)
- setup_environment_system.sh and setup_environment_wsl.sh (setup scripts)
- pyproject.toml, requirements.txt, requirements-dev.txt, .env (configuration files)

Additional files that may need to be considered:
- deployment/test_stages.py (used by launch.py)
- setup_linting.py, validate_dependencies.py, verify_packages.py

These files are branch-agnostic and applicable across main and scientific branches.