with open("setup/services.py", "r") as f:
    content = f.read()

content = content.replace("if not re.match(r'^[a-zA-Z0-9.-]+\n\n\ndef start_node_service", "if not re.match(r'^[a-zA-Z0-9.-]+$', host):\n        logger.error(f\"Invalid host parameter: {host}\")\n        return\n\n\ndef start_node_service")

with open("setup/services.py", "w") as f:
    f.write(content)
