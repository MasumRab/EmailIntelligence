with open('setup/services.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line == "            start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url), host):\n":
        new_lines.append("            start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url)\n")
    elif line == "        logger.error(f\"Invalid host parameter: {host}\")\n" and "frontend_path" in "".join(lines[lines.index(line)-3:lines.index(line)]):
        pass # skip this and the next return line
    elif line == "        return\n" and "frontend_path" in "".join(lines[lines.index(line)-4:lines.index(line)]):
        pass # skip this line
    else:
        new_lines.append(line)

with open('setup/services.py', 'w') as f:
    f.writelines(new_lines)
