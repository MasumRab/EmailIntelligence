with open('setup/launch.py', 'r') as f:
    lines = f.readlines()

new_lines = []
in_conflict = False
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('<<<<<<< HEAD'):
        i += 1
        while i < len(lines) and not lines[i].startswith('======='):
            i += 1
        i += 1
        while i < len(lines) and not lines[i].startswith('>>>>>>>'):
            new_lines.append(lines[i])
            i += 1
        i += 1
        continue
    else:
        new_lines.append(line)
        i += 1

with open('setup/launch.py', 'w') as f:
    f.writelines(new_lines)
