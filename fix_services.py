with open("setup/services.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.startswith("    if not re.match(r'^[a-zA-Z0-9.-]+"):
        new_lines.append("    if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):\n")
        new_lines.append("        logger.error(f\"Invalid host format: {host}\")\n")
        new_lines.append("        return\n\n")
        new_lines.append("    # Create the command with list formulation to prevent injection\n")
        new_lines.append("    cmd = [\n")
        new_lines.append("        str(python_exe), \"-m\", \"uvicorn\", \"src.main:app\",\n")
        new_lines.append("        \"--host\", str(host), \"--port\", str(port), \"--reload\"\n")
        new_lines.append("    ]\n\n")
        new_lines.append("    # We deliberately use list command format here since it prevents shell injection\n")
        new_lines.append("    process = process_manager.start_process(cmd, \"Python API\", cwd=ROOT_DIR)\n\n")
        new_lines.append("    if process:\n")
        new_lines.append("        # Save process info to run directory\n")
        new_lines.append("        from setup.utils import create_run_info\n")
        new_lines.append("        create_run_info(\n")
        new_lines.append("            \"backend\", {\"pid\": process.pid, \"port\": port, \"host\": host}\n")
        new_lines.append("        )\n")
    else:
        new_lines.append(line)

with open("setup/services.py", "w") as f:
    f.writelines(new_lines)
