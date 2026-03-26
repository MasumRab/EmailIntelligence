with open("uv.lock", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
count = 0
for i, line in enumerate(lines):
    if line.startswith('[[package]]'):
        pass

    if 'name = "bandit"\n' in line:
        # Look backwards to find the `[[package]]`
        for j in range(len(new_lines)-1, -1, -1):
            if new_lines[j] == '[[package]]\n':
                count += 1
                if count > 1:
                    skip = True
                    # Remove the [[package]] line
                    new_lines = new_lines[:j]
                break

    if skip:
        # Wait until we see an empty line or another `[[package]]`
        if line.startswith('[[package]]'):
            skip = False
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("uv.lock", "w") as f:
    f.writelines(new_lines)
