# Critical Files Check for Orchestration Tools

This document describes the critical files check functionality that has been added to the orchestration-tools branch to validate the integrity of essential orchestration files.

## Overview

The critical files check is a validation mechanism that ensures all essential files for the orchestration workflow are present and accessible. This check helps maintain the integrity of the orchestration system by verifying that no critical components are missing.

## Usage

The critical files check can be run using the `launch.py` script with the `check` command:

```bash
# Check all critical files
python launch.py check

# Check only critical files (default behavior)
python launch.py check --critical-files

# Check orchestration environment (includes critical files and merge conflicts)
python launch.py check --env
```

## What Gets Checked

### Critical Files

The following files are considered critical for orchestration and are validated:

1. **Core Orchestration Scripts**
   - `scripts/install-hooks.sh` - Installs Git hooks from orchestration-tools
   - `scripts/cleanup_orchestration.sh` - Cleans up orchestration files when switching branches
   - `scripts/sync_setup_worktrees.sh` - Synchronizes setup files between worktrees
   - `scripts/reverse_sync_orchestration.sh` - Reverse synchronization for orchestration updates

2. **Git Hooks**
   - `scripts/hooks/pre-commit` - Pre-commit validation
   - `scripts/hooks/post-commit` - Post-commit actions
   - `scripts/hooks/post-commit-setup-sync` - Post-commit setup synchronization
   - `scripts/hooks/post-merge` - Post-merge actions
   - `scripts/hooks/post-checkout` - Post-checkout synchronization
   - `scripts/hooks/post-push` - Post-push actions

3. **Shared Libraries**
   - `scripts/lib/common.sh` - Common utility functions
   - `scripts/lib/error_handling.sh` - Error handling utilities
   - `scripts/lib/git_utils.sh` - Git utility functions
   - `scripts/lib/logging.sh` - Logging utilities
   - `scripts/lib/validation.sh` - Validation utilities

4. **Setup Files**
   - `setup/launch.py` - Main launcher script
   - `setup/pyproject.toml` - Python project configuration
   - `setup/requirements.txt` - Runtime dependencies
   - `setup/requirements-dev.txt` - Development dependencies
   - `setup/setup_environment_system.sh` - System environment setup
   - `setup/setup_environment_wsl.sh` - WSL environment setup
   - `setup/setup_python.sh` - Python setup script

5. **Configuration Files**
   - `.flake8` - Python linting configuration
   - `.pylintrc` - Python linting configuration
   - `.gitignore` - Git ignore patterns
   - `.gitattributes` - Git attributes

6. **Root Wrapper**
   - `launch.py` - Root wrapper that forwards to setup/launch.py

7. **Deployment Files**
   - `deployment/deploy.py` - Deployment management script
   - `deployment/test_stages.py` - Test execution stages
   - `deployment/docker-compose.yml` - Docker Compose configuration

### Critical Directories

The following directories are also validated for existence:

- `scripts/` - All orchestration scripts
- `scripts/hooks/` - Git hooks
- `scripts/lib/` - Shared libraries
- `setup/` - Setup files and launcher
- `deployment/` - Deployment-related files
- `docs/` - Documentation

### Orchestration Documentation

The following documentation files are validated:

- `docs/orchestration_summary.md` - Summary of orchestration workflow
- `docs/orchestration_validation_tests.md` - Validation tests for orchestration
- `docs/orchestration_hook_management.md` - Hook management documentation
- `docs/orchestration_branch_scope.md` - Branch scope documentation
- `docs/env_management.md` - Environment management documentation
- `docs/git_workflow_plan.md` - Git workflow planning
- `docs/current_orchestration_docs/` - Current orchestration documentation directory
- `docs/guides/` - Orchestration guides directory

## Validation Process

The validation process performs the following checks:

1. **File Existence** - Verifies that all critical files exist in the file system
2. **Directory Existence** - Verifies that all critical directories exist
3. **Documentation Existence** - Verifies that all orchestration documentation exists

If any critical files are missing, the validation will fail and list all missing files.

## Environment Validation

When running with the `--env` flag, the check also includes:

1. **Merge Conflict Detection** - Checks for unresolved merge conflicts in critical files
2. **Critical Files Check** - All the checks described above

## Integration with Existing Validation

The critical files check integrates with the existing environment validation system:

- `validate_environment()` - Original environment validation (used for application branches)
- `validate_orchestration_environment()` - Orchestration-specific validation that includes critical files check
- `check_critical_files()` - Standalone critical files validation function

## Troubleshooting

If the critical files check fails:

1. **Identify Missing Files** - The error message will list all missing files
2. **Restore Missing Files** - Restore the missing files from a clean orchestration-tools branch:
   ```bash
   git checkout orchestration-tools -- <missing_file_path>
   ```
3. **Verify Fix** - Run the check again to verify all files are present:
   ```bash
   python launch.py check
   ```

## Maintenance

When adding new critical files to the orchestration system:

1. Update the `critical_files` list in the `check_critical_files()` function in `setup/launch.py`
2. Update this documentation to reflect the new critical files
3. Test the validation to ensure it works correctly

## Example Output

Successful check:
```
$ python launch.py check
INFO: Running orchestration checks...
INFO: All critical files are present.
INFO: All orchestration checks passed!
```

Failed check:
```
$ python launch.py check
INFO: Running orchestration checks...
ERROR: Missing critical files:
ERROR:   - scripts/new_critical_script.sh
ERROR:   - docs/new_documentation.md
ERROR: Please restore these critical files for proper orchestration functionality.
ERROR: Orchestration checks failed!
```