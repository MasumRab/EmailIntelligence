with open("src/main.py", "r") as f:
    lines = f.readlines()

for i in range(3, 20):
    if lines[i].startswith("import ") or lines[i].startswith("from "):
        if "# noqa: E402" not in lines[i]:
            lines[i] = lines[i].rstrip() + "  # noqa: E402\n"

with open("src/main.py", "w") as f:
    f.writelines(lines)
