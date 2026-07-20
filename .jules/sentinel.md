## 2026-06-16 - Mitigated Command Injection in Setup Scripts

**Vulnerability:** Use of `subprocess.run(..., shell=True)` in Python setup and migration scripts (`scripts/branch_rename_migration.py`, `deployment/setup_env.py`, `deployment/migrate.py`).
**Learning:** While these are internal deployment tools and may not directly handle untrusted user input during production API execution, utilizing `shell=True` is a bad practice that introduces risk if inputs are later parameterized (e.g. branch names or args). Furthermore, relying on bash short-circuiting like `|| true` within string commands bypasses structured exception handling in Python.
**Prevention:** Replaced `shell=True` with `shell=False` by using `shlex.split()` to properly tokenize command arguments. Replaced shell shortcuts (e.g. `|| true`) with Python-native error handling (using the `check=False` parameter in `subprocess.run`).

## 2026-06-16 - CI Python Environment Instability

**Vulnerability:** N/A (CI Flakiness/Debt)
**Learning:** CI for Python suite is highly prone to failing locally and via GH Actions due to pathing issues and lingering technical debt (undeclared dependencies in test files, unresolved import errors like `model_manager`, missing directories for sqlite3 initialization).
**Prevention:** Must ensure tests construct necessary filepaths via `os.makedirs` and all referenced internal modules are properly imported within `__init__.py` or `main.py`.
