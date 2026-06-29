## 2026-05-16 - Fix Command Injection in branch_rename_migration.py

**Vulnerability:** The `run_command` function in `scripts/branch_rename_migration.py` uses `subprocess.run(command, shell=True)` which is vulnerable to command injection if malicious branch names are present or if untrusted arguments are passed.
**Learning:** Python `subprocess.run` wrapper scripts often default to `shell=True` for convenience when passing full string commands, making them vulnerable. Static analysis tools flag them as risks. Using `shell=False` requires passing a list of arguments, but sometimes wrappers expect a string command. Using `shlex.split` enables safe parsing.
**Prevention:** Always use `shell=False` with `subprocess.run` and pass arguments as a list. Use `shlex.split` if you must accept a string command, or refactor to accept a list of arguments directly.
