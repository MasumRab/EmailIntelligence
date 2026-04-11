# Sentinel Learnings
## 2025-04-11: Git Diff Subprocess Command Injection Refactoring

* **Vulnerability Discovered:** Command injection risk using `subprocess.run(..., shell=True)` with string interpolation for `git diff` and other git commands in `scripts/intelligent_merger.py`.
* **Learning:** When replacing `shell=True` with explicit `List[str]` arguments and `check=True` for security, commands like `git diff` will intentionally return a non-zero exit code (1) when differences exist. With `check=True`, this raises a `subprocess.CalledProcessError`.
* **Prevention:** Always wrap `subprocess.run` calls for commands that use non-zero exit codes (like `diff` or `grep`) in a `try...except subprocess.CalledProcessError as e:` block. The expected output must then be extracted from `e.stdout` rather than incorrectly discarding it or failing the script.
