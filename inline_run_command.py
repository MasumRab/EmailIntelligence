import re

with open('setup/launch.py', 'r') as f:
    content = f.read()

# I will replace `run_command` with a helper that just generates the inline code
# Actually it's easier to just do it via string replacement.

def replace_call(old, new_args, desc, kwargs=""):
    global content

    # We need to get the exact indentation of `old`
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if old in line:
            indent = line[:len(line) - len(line.lstrip())]

            replacement = f"""logger.info({desc} + "...")
{indent}try:
{indent}    proc = subprocess.run({new_args}, executable=str(python_exe), check=True, text=True, capture_output=True{kwargs})
{indent}    if proc.stdout:
{indent}        logger.debug(proc.stdout)
{indent}    if proc.stderr:
{indent}        logger.warning(proc.stderr)
{indent}except (subprocess.CalledProcessError, FileNotFoundError) as e:
{indent}    logger.error(f"Failed: {{{desc.strip('f"')} if desc.startswith('f') else desc}}")
{indent}    if isinstance(e, subprocess.CalledProcessError):
{indent}        logger.error(f"Stderr: {{e.stderr}}")"""
            lines[i] = indent + replacement
            break

    content = '\n'.join(lines)


# Usages:
replace_call(
    'run_command([python_exe, "-m", "pip", "install", manager], f"Installing {manager}")',
    '["python", "-m", "pip", "install", manager]',
    'f"Installing {manager}"'
)

replace_call(
    'run_command([python_exe, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")',
    '["python", "-m", "pip", "install", "--upgrade", "pip"]',
    '"Upgrading pip"'
)

replace_call(
    'run_command([python_exe, "-m", "pip", "install", "poetry"], "Installing Poetry")',
    '["python", "-m", "pip", "install", "poetry"]',
    '"Installing Poetry"'
)

replace_call(
    'run_command(\n            [python_exe, "-m", "poetry", "install", "--with", "dev"],\n            "Installing dependencies with Poetry",\n            cwd=ROOT_DIR,\n        )',
    '["python", "-m", "poetry", "install", "--with", "dev"]',
    '"Installing dependencies with Poetry"',
    ', cwd=ROOT_DIR'
)

# Replace another Upgrading pip
replace_call(
    'run_command([python_exe, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")',
    '["python", "-m", "pip", "install", "--upgrade", "pip"]',
    '"Upgrading pip"'
)

replace_call(
    'run_command([python_exe, "-m", "pip", "install", "uv"], "Installing uv")',
    '["python", "-m", "pip", "install", "uv"]',
    '"Installing uv"'
)

replace_call(
    'run_command(\n            [python_exe, "-m", "uv", "pip", "install", "-e", ".[dev]", "--exclude", "notmuch"],\n            "Installing dependencies with uv (excluding notmuch)",\n            cwd=ROOT_DIR,\n        )',
    '["python", "-m", "uv", "pip", "install", "-e", ".[dev]", "--exclude", "notmuch"]',
    '"Installing dependencies with uv (excluding notmuch)"',
    ', cwd=ROOT_DIR'
)

replace_call(
    'run_command(\n            [python_exe, "-m", "pip", "install", f"notmuch=={major_minor}"],\n            f"Installing notmuch {major_minor} to match system",\n        )',
    '["python", "-m", "pip", "install", f"notmuch=={major_minor}"]',
    'f"Installing notmuch {major_minor} to match system"'
)

# Now remove the definition of run_command
import re
content = re.sub(r'def run_command\(cmd: List\[str\], description: str, \*\*kwargs\) -> bool:.*?return False\n\n', '', content, flags=re.DOTALL)

with open('setup/launch.py', 'w') as f:
    f.write(content)
