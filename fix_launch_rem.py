import re

with open('setup/launch.py', 'r') as f:
    content = f.read()

# Replace run_command for poetry install
poetry_call = """        run_command(
            [python_exe, "-m", "poetry", "install", "--with", "dev"],
            "Installing dependencies with Poetry",
            cwd=ROOT_DIR,
        )"""

replacement_poetry = """        logger.info("Installing dependencies with Poetry" + "...")
        try:
            proc = subprocess.run(["python", "-m", "poetry", "install", "--with", "dev"], executable=str(python_exe), check=True, text=True, capture_output=True, cwd=ROOT_DIR)
            if proc.stdout:
                logger.debug(proc.stdout)
            if proc.stderr:
                logger.warning(proc.stderr)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Failed: Installing dependencies with Poetry")
            if isinstance(e, subprocess.CalledProcessError):
                logger.error(f"Stderr: {e.stderr}")"""

content = content.replace(poetry_call, replacement_poetry)

# Replace run_command for uv install
uv_call = """        run_command(
            [python_exe, "-m", "uv", "pip", "install", "-e", ".[dev]", "--exclude", "notmuch"],
            "Installing dependencies with uv (excluding notmuch)",
            cwd=ROOT_DIR,
        )"""

replacement_uv = """        logger.info("Installing dependencies with uv (excluding notmuch)" + "...")
        try:
            proc = subprocess.run(["python", "-m", "uv", "pip", "install", "-e", ".[dev]", "--exclude", "notmuch"], executable=str(python_exe), check=True, text=True, capture_output=True, cwd=ROOT_DIR)
            if proc.stdout:
                logger.debug(proc.stdout)
            if proc.stderr:
                logger.warning(proc.stderr)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Failed: Installing dependencies with uv (excluding notmuch)")
            if isinstance(e, subprocess.CalledProcessError):
                logger.error(f"Stderr: {e.stderr}")"""

content = content.replace(uv_call, replacement_uv)

notmuch_call = """        run_command(
            [python_exe, "-m", "pip", "install", f"notmuch=={major_minor}"],
            f"Installing notmuch {major_minor} to match system",
        )"""

replacement_notmuch = """        logger.info(f"Installing notmuch {major_minor} to match system" + "...")
        try:
            proc = subprocess.run(["python", "-m", "pip", "install", f"notmuch=={major_minor}"], executable=str(python_exe), check=True, text=True, capture_output=True)
            if proc.stdout:
                logger.debug(proc.stdout)
            if proc.stderr:
                logger.warning(proc.stderr)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Failed: Installing notmuch {major_minor} to match system")
            if isinstance(e, subprocess.CalledProcessError):
                logger.error(f"Stderr: {e.stderr}")"""

content = content.replace(notmuch_call, replacement_notmuch)

# Also fix the f-string interpolation issues caused by the previous script
content = content.replace('{Installing Poetry if desc.startswith(\'f\') else desc}', 'Installing Poetry')
content = content.replace('{Installing uv if desc.startswith(\'f\') else desc}', 'Installing uv')
content = content.replace('{Upgrading pip if desc.startswith(\'f\') else desc}', 'Upgrading pip')
content = content.replace('{Installing {manager} if desc.startswith(\'f\') else desc}', '{manager}')


with open('setup/launch.py', 'w') as f:
    f.write(content)
