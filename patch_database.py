
filepath = 'src/backend/python_backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
has_os = False
for line in lines:
    if line.startswith('import os'):
        has_os = True
    new_lines.append(line)
    if 'self.db_path = db_path' in line:
        new_lines.append('        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)\n')

if not has_os:
    new_lines.insert(0, 'import os\n')

with open(filepath, 'w') as f:
    f.writelines(new_lines)

print("Patched successfully")
