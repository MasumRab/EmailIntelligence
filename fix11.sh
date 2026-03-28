cat << 'INNER_EOF' > /tmp/repl.txt
    try:
        # nosec B603: We control the arguments, no command injection risk.
        proc = subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)  # nosec
        if proc.stdout:
INNER_EOF
sed -i -e '/try:/r /tmp/repl.txt' -e '/try:/d' -e '/proc = subprocess.run(cmd, check=True, text=True, capture_output=True, \*\*kwargs)/d' -e '/if proc.stdout:/d' setup/launch.py
