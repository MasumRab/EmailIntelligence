import re

with open('setup/launch.py', 'r') as f:
    content = f.read()

# Let's replace `run_command` with inline blocks.
# wait, there are 11 uses of `run_command`.
# I can write a script to just replace all `subprocess.run(cmd, ...)` and `run_command([python_exe, ...], ...)` with literal first elements and `executable=str(...)`.

# Let's see the direct `subprocess.run` calls:
# 120: subprocess.run(["xset", "-q"], ...) -> already literal string! Why did it complain earlier? It didn't. The error lines are 336, 420, 434, 461-466, 487-493, 505-507.
# wait, what's on line 336? Let's check `setup/launch.py` line 336 right now.
