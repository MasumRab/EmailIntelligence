# Sentinel Learnings

## Date: 2024-05-31
## Title: Removed `shell=True` from subprocess calls
## Vulnerability/Condition Discovered: Python subprocess calls in `scripts/` using `shell=True` with string interpolation.
## Learning: Using `shell=True` in python's `subprocess.run` combined with user or dynamic inputs allows for Command Injection attacks. Static analysis tools (e.g. Sourcery) are sensitive to variables being passed to generic wrapper functions (like `run_command(cmd)`), flagging them as command injection risks.
## Prevention Note: Always use `shell=False` combined with a list of arguments for python subprocess.run calls. Avoid generic wrappers passing command strings and prefer inlining `subprocess.run` calls directly so the executable string is statically analyzable.
