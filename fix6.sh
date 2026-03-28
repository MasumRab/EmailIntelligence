cat << 'INNER_EOF' > /tmp/repl.txt
    if not re.match(r"^[a-zA-Z0-9.-]+$", str(host)):
        logger.error(f"Invalid host parameter: {host}")
        return
INNER_EOF
sed -i -e '/if not re.match(r"^[a-zA-Z0-9.-]+$", str(host)):/r /tmp/repl.txt' -e '/if not re.match(r"^[a-zA-Z0-9.-]+$", str(host)):/d' setup/services.py
