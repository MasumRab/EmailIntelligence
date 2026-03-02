with open("setup/services.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == "if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):":
        # Add the body of the if statement
        lines.insert(i + 1, "        logger.error(f'Invalid host format: {host}')\n        return\n")
        break

with open("setup/services.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
