with open('setup/services.py', 'r') as f:
    content = f.read()

content = content.replace("if not re.match(r'^[a-zA-Z0-9.-]+\n", "if not re.match(r'^[a-zA-Z0-9.-]+$', host):\n        logger.error(f'Invalid host parameter: {host}')\n        return\n")

with open('setup/services.py', 'w') as f:
    f.write(content)
