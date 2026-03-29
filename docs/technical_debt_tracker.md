# Technical Debt & Anomaly Tracker

This document tracks recurring technical issues and the established patterns for resolving them.

## Issue: Recurrent `ImportError` and `AttributeError` in `setup/` scripts

### Symptom

When running integration tests or the `launch.py` script, the application crashes with `ImportError` or `AttributeError` for functions and constants that appear to be missing from the codebase.

**Examples:**
- `ImportError: cannot import name 'initialize_all_services' from 'setup.services'`
- `ImportError: cannot import name 'COMMAND_PATTERN_AVAILABLE' from 'setup.commands'`
- `AttributeError: module 'setup.commands.guide_dev_command' has no attribute 'subprocess'`

### Root Cause

The codebase has undergone significant refactoring, especially around the `orchestration-tools` branch and the `setup/` directory. During these refactors, functions were moved or deleted, but the corresponding import statements or function calls were not always updated. This has led to a state of "code rot" where the application's entry points are broken.

### Resolution Strategy

The primary strategy is to **restore, not remove**. Do not comment out the failing code, as this only hides the problem. Instead, treat the Git history as the source of truth and restore the missing pieces.

1.  **Identify the Missing Name:** Look at the `ImportError` or `AttributeError` to identify the exact function, class, or constant name that is missing.

2.  **Search the Git History:** Use `git log -S "<missing_name>"` to find the commits where this name was added, modified, or deleted. The `-S` flag searches for the occurrence of a string in the code.
    ```bash
    # Example
    git log -S "initialize_all_services" --oneline --name-status
    ```

3.  **Analyze the History:** Examine the commit history to understand where the code originally lived and where it was moved or deleted. The `--name-status` flag is useful to see which files were Added (`A`), Modified (`M`), or Deleted (`D`).

4.  **Restore the Code:**
    -   If a function was moved, correct the `import` statement in the calling file to point to the new location.
    -   If a file or function was deleted, use `git show <commit_hash>:<file_path>` to view the content of the file before it was deleted, and restore the necessary code.
    -   If a file like `__init__.py` was deleted, it may need to be recreated to expose package-level constants or functions.

5.  **Verify:** After restoring the code, re-run the tests to confirm the immediate error is resolved and to see if another error appears. Repeat the process until all errors are gone.

### Recovered Functions Log

| Function/Constant | Original Location | Restored To | Notes |
|---|---|---|---|
| `check_critical_files` | `setup/validation.py` (deleted in a commit) | `setup/validation.py` | Restored from `7ce3df7b` |
| `validate_orchestration_environment` | `setup/validation.py` (deleted in a commit) | `setup/validation.py` | Restored from `7ce3df7b` |
| `validate_path_safety` | `src/core/security.py` (file deleted) | `src/core/security.py` | Restored from `e8074f02` |
| `initialize_all_services` | `src/core/container.py` (moved) | `setup/container.py` | Corrected import in `launch.py` |
| `COMMAND_PATTERN_AVAILABLE` | `setup/commands/__init__.py` (file deleted) | `setup/commands/__init__.py` | Recreated the `__init__.py` file |
| `handle_setup` | `setup/environment.py` | `setup/environment.py` | Corrected import in `launch.py` |
