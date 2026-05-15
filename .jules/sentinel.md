# Sentinel Journal

### 2025-05-15: Command Injection Risks in Wrapper Functions
- **Vulnerability Discovered**: Multiple utility scripts (`scripts/intelligent_merger.py`, `scripts/intelligent_merge_analyzer.py`, `scripts/path_change_detector.py`, `scripts/branch_rename_migration.py`) use generic `run_command(cmd: str)` wrappers with `subprocess.run(cmd, shell=True)`. This creates command injection vulnerabilities and prevents static analyzers from detecting safe hardcoded base commands.
- **Learning**: Wrapping `subprocess.run` into a generic string-based function prevents tools like Sourcery from verifying the safety of the executable.
- **Prevention Note**: Always inline `subprocess.run` calls directly where needed using list arguments (`shell=False`), ensuring the base command (e.g., `["git", ...]`) is a static string literal. Avoid `shell=True` entirely.
