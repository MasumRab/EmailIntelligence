with open("src/core/data/__init__.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() in ["Data package for the Email Intelligence Platform.", "Contains repository patterns for data access.", '"""'] and len(new_lines) > 20:
        continue
    new_lines.append(line)

with open("src/core/data/__init__.py", "w") as f:
    f.writelines(new_lines)
