import re

with open('setup/launch.py', 'r') as f:
    content = f.read()

# I will replace all calls to `run_command` with inline `subprocess.run` calls to be completely safe against Sourcery.
# No wait, I don't need to replace ALL of them, I can just change the signature of run_command?
# The memory says:
# "Static analysis tools (like Sourcery) cannot trace variables passed to generic wrapper functions (like run_command(cmd)) and will flag them as command injection risks despite # sourcery skip or dummy string conversions. To satisfy these checks, inline subprocess.run calls directly in the code so the executable name is statically analyzable as a literal string (e.g., subprocess.run(["git", ...]))."

# Oh, it EXPLICITLY says "inline subprocess.run calls directly in the code".
# So I should remove `run_command` and inline ALL of its usages.

# Wait, the sourcery errors were ONLY on specific lines!
# setup/launch.py:420 (which is inside `run_command`?)
# Let's check the line numbers again:
# `420`
# `434`
# `336`
# `461-466`
# `487-493`
# `505-507`
