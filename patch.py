with open("setup/launch.py", "r") as f:
    lines = f.readlines()

out = []
for i, line in enumerate(lines):
    if "<<<<<<< HEAD" in line or "=======" in line or ">>>>>>>" in line:
        continue
    out.append(line)
with open("setup/launch.py", "w") as f:
    f.writelines(out)
