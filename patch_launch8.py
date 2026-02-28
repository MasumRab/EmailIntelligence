with open("setup/launch.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i == 564:  # line 565 which is '            return False\n'
        continue
    if "return sys.executable" in line and lines[i-1].strip() == 'logger.info("Using system Python")':
        new_lines.append(line)
        continue
    new_lines.append(line)

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
