sed -i 's/if not re.match(r'\''\^\[a-zA-Z0-9.-\]+.*/if not re.match(r"^[a-zA-Z0-9.-]+$", str(host)):/g' setup/services.py
