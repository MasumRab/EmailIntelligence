cat << 'INNER_EOF' > /tmp/repl.txt
    if not re.match(r"^[a-zA-Z0-9.-]+$", str(host)):
        logger.error(f"Invalid host parameter: {host}")
        return
INNER_EOF
sed -i -e '175r /tmp/repl.txt' -e '175d' setup/services.py
