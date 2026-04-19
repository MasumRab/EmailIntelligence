with open("setup/launch.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_conflict = False
for i, line in enumerate(lines):
    if line.startswith("<<<<<<< HEAD"):
        in_conflict = True
        continue
    elif line.startswith("======="):
        in_conflict = False
        continue
    elif line.startswith(">>>>>>>"):
        continue

    if not in_conflict:
        new_lines.append(line)

with open("setup/launch.py", "w") as f:
    f.writelines(new_lines)
