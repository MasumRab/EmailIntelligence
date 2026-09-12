import re

with open('setup/launch.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'def run_command(cmd: List[str], description: str, **kwargs) -> bool:' in line:
        pass # We will modify this

    new_lines.append(line)

# Wait, `run_command` accepts `cmd: List[str]`.
# It runs `subprocess.run(cmd, ...)`
# We can change `run_command` to take `executable: str` and `args: List[str]`.
# But `cmd` is constructed by the caller.
# Let's find all calls to `run_command` and replace them.
