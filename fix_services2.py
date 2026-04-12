with open("setup/services.py", "r") as f:
    content = f.read()

content = content.replace("start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url), host):\n        logger.error(f\"Invalid host parameter: {host}\")\n        return\n\n    cmd = [", "start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url)\n\n    cmd = [")

with open("setup/services.py", "w") as f:
    f.write(content)
