with open("setup/services.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == "start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url), host):":
        lines[i] = "            start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url)\n"
    if line.strip() == "if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):":
        # Check if next line is properly indented, this is line 175
        pass

with open("setup/services.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
