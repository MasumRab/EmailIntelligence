with open("setup/services.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):$', host):", "if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):")

with open("setup/services.py", "w", encoding="utf-8") as f:
    f.write(text)
