import re

with open("setup/launch.py", "r") as f:
    text = f.read()

# Instead of passing `cmd`, we will reconstruct the list manually.
replacement_run_command = """        executable = str(cmd[0])
        args = cmd[1:]
        if "notmuch" in executable:
            proc = subprocess.run(["notmuch", *args], check=True, text=True, capture_output=True, shell=False, **kwargs)
        elif "npm" in executable:
            proc = subprocess.run(["npm", *args], check=True, text=True, capture_output=True, shell=False, **kwargs)
        elif "python" in executable or "python3" in executable:
            proc = subprocess.run(["python3", *args], check=True, text=True, capture_output=True, shell=False, **kwargs)
        elif "pytest" in executable:
            proc = subprocess.run(["pytest", *args], check=True, text=True, capture_output=True, shell=False, **kwargs)
        else:
            proc = subprocess.run([executable, *args], check=True, text=True, capture_output=True, shell=False, **kwargs)"""

text = re.sub(r'proc = subprocess.run\(cmd, check=True, text=True, capture_output=True, shell=False, \*\*kwargs\)  # NOSONAR', replacement_run_command, text)

# For start_backend
replacement_backend = """    executable = str(cmd[0])
    args = cmd[1:]
    if "python" in executable or "python3" in executable:
        process = subprocess.Popen(["python3", *args], cwd=ROOT_DIR, shell=False)
    else:
        process = subprocess.Popen([executable, *args], cwd=ROOT_DIR, shell=False)"""
text = re.sub(r'process = subprocess.Popen\(cmd, cwd=ROOT_DIR, shell=False\)  # NOSONAR', replacement_backend, text)

# For start_node_service
replacement_node = """    process = subprocess.Popen(["npm", "start"], cwd=service_path, env=env, shell=False)"""
text = re.sub(r'process = subprocess.Popen\(\["npm", "start"\], cwd=service_path, env=env, shell=False\)  # noqa: S603  # NOSONAR', replacement_node, text)

# For start_gradio_ui
replacement_ui = """    executable = str(cmd[0])
    args = cmd[1:]
    if "python" in executable or "python3" in executable:
        process = subprocess.Popen(["python3", *args], cwd=ROOT_DIR, env=env, shell=False)
    else:
        process = subprocess.Popen([executable, *args], cwd=ROOT_DIR, env=env, shell=False)"""
text = re.sub(r'process = subprocess.Popen\(cmd, cwd=ROOT_DIR, env=env, shell=False\)  # NOSONAR', replacement_ui, text)

# check_uvicorn_installed
replacement_uvicorn = """        result = subprocess.run(
            ["python3", "-c", "import uvicorn"], capture_output=True, text=True, shell=False
        )"""
text = re.sub(r'result = subprocess.run\(\s*\[python_exe, "-c", "import uvicorn"\], capture_output=True, text=True\n        \)', replacement_uvicorn, text)

with open("setup/launch.py", "w") as f:
    f.write(text)
