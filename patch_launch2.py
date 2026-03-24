with open("setup/launch.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # It looks like there's an orphaned block from line 582 to 591
    if i >= 581 and i <= 590:
        continue
    new_lines.append(line)

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
