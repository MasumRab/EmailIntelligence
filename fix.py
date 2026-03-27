with open("setup/launch.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith("<<<<<<< HEAD"):
        skip = True
    elif line.startswith("======="):
        skip = False
    elif line.startswith(">>>>>>>"):
        pass
    else:
        if not skip:
            new_lines.append(line)

with open("setup/launch.py", "w") as f:
    f.writelines(new_lines)
