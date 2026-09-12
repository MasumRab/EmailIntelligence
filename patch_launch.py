import sys
import re

with open('setup/launch.py', 'r') as f:
    content = f.read()

# For `run_command` (lines 425-435), Sourcery complains about `subprocess.run(cmd, ...)`
# Let's add `# sourcery skip: command-injection` above it, or we can inline the executable if possible?
# But `cmd` can be anything. We can't inline it. Wait, the memory says:
# "To satisfy these checks, inline subprocess.run calls directly in the code so the executable name is statically analyzable as a literal string (e.g., subprocess.run(["git", ...]))."
# This means I need to remove `run_command` entirely, or at least inline its usage where it complains?
# Wait, the sourcery errors say:
# setup/launch.py:420
# setup/launch.py:434
# setup/launch.py:336
# setup/launch.py:461-466
# setup/launch.py:487-493
# setup/launch.py:505-507

# Actually, the line numbers in the PR might be different from the current file because I just did a rebase.
# Let's check where the errors actually are.

# 336:
# 420:
# 434:
# 461-466:
# 487-493:
# 505-507:

# I'll just find all `subprocess.run` calls and make sure the first argument is a static list like `["python", "-m", "pip", ...]` or `["git", ...]`. Wait, `get_python_executable()` returns a Path or string. `[python_exe, "-c", "import poetry"]` isn't statically string.
# Let's use `[str(python_exe), ...]`? No, Sourcery complains because it's not a static string literal.
# "inline subprocess.run calls directly in the code so the executable name is statically analyzable as a literal string (e.g., subprocess.run(["git", ...]))"

# Let's just use `subprocess.run([str(python_exe), ...])` but wait, if it wants `["git"]`...

print("Analyzing lines...")
