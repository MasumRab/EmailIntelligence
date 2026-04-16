import sys
# Given `test_launcher` tests were completely broken by some major recent PR on main,
# and it's throwing AttributeErrors from `test_launcher.py` itself,
# I will quickly fix just the immediate `SyntaxError: unterminated string literal (detected at line 175)` in `setup/services.py` so the tests *run* (even if they fail due to main being broken) or just skip testing `tests/test_launcher.py`.
# Wait, the CI runs `pytest tests/ src/ modules/`. We can't let it crash at collection.

with open("setup/services.py", "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

lines = text.split("\n")
for i, line in enumerate(lines):
    if line.strip().startswith("if not re.match(r'^[a-zA-Z0-9.-]+"):
        lines[i] = "    if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):"
    elif line.strip().startswith("start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url), host):"):
        lines[i] = "            start_node_service(frontend_path, \"Frontend Client\", args.frontend_port, api_url)"
    elif line.strip().startswith("logger.error(f\"Invalid host parameter: {host}\")") and "host" not in lines[i-1]:
        # Actually this is from the bad merge. We need to delete lines 347, 348 if they are the broken parts
        pass

# Let's fix line 348:
if "logger.error(f\"Invalid host parameter: {host}\")" in lines[348]:
    lines[348] = ""
if "return" in lines[349] and lines[348] == "":
    lines[349] = ""

with open("setup/services.py", "w") as f:
    f.write("\n".join(lines))
