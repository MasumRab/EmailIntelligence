
### Date: 2024-03-xx (Current Date)
**Title:** Command Injection Risk in Automation Scripts via shell=True
**Discovered:** Utility scripts (e.g., `scripts/intelligent_merger.py`) used generic shell wrappers like `run_command(cmd)` with `shell=True`, vulnerable to command injection if input parameters (like Git refs) are manipulated.
**Learning:** Migrating `shell=True` to `shell=False` inside a generic wrapper often causes issues with static analysis tools like Sourcery which cannot trace the command execution context. Using `shell=False` requires list arguments.
**Prevention Note:** When refactoring Git script utilities, remove generic `run_command` wrappers and use inline `subprocess.run(["git", ...], shell=False, check=True)` calls. Handle `subprocess.CalledProcessError` specifically for tools like `git diff` that return exit code 1 on valid differences.
