# Sentinel Notes

## 2024-05-24: Command Injection via Generic Process Wrappers

**Vulnerability Discovered:**
The repository contained multiple utility scripts (`scripts/intelligent_merge_analyzer.py` and `scripts/path_change_detector.py`) that utilized a generic wrapper function `run_command` calling `subprocess.run(shell=True)`. This wrapper abstracted the string formatting away from the process execution.

**Learning:**
Generic wrappers around process execution often defeat static analysis tools like `bandit` or `Sourcery`, as the command inputs are passed as generic variables rather than analyzable string literals. This provides a false sense of security while maintaining the risk of shell/command injection. In this instance, `git diff` and `git ls-tree` commands were executing dynamically formatted strings.

**Prevention:**
Always inline the `subprocess.run` calls directly into the target function using `shell=False` and a list of arguments `[executable, arg1, arg2...]`. This enables tools to statically analyze the executable being called and prevents shell meta-character injection. Generic `run_command` wrappers should be avoided when the commands being run accept dynamic external inputs.
