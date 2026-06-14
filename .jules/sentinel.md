## 2025-05-22 - [CRITICAL] Prevent Command Injection via `shell=True`

**Vulnerability:** Several utility and deployment scripts (`scripts/branch_rename_migration.py`, `deployment/setup_env.py`, `deployment/migrate.py`) were passing strings directly to `subprocess.run(..., shell=True)`. This could allow attackers to execute arbitrary shell commands if variables (like branch names) were maliciously crafted.
**Learning:** Legacy utility scripts sometimes bypass strict linting or security reviews initially. `shell=True` was used for convenience with pipeline operators (`|| true`) or complex arguments, but it introduces critical injection risks when accepting untrusted or dynamically generated strings.
**Prevention:** Always use `subprocess.run(..., shell=False)` and parse strings into lists using `shlex.split(command)` or construct the list manually. Replace shell-native error suppression like `|| true` with Python equivalents like `check=False`.
