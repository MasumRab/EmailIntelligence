sed -i '175c\    if not re.match(r"^[a-zA-Z0-9.-]+$", str(host)):\n        logger.error(f"Invalid host parameter: {host}")\n        return' setup/services.py
