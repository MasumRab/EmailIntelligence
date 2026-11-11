import re

with open('emailintelligence_cli.py') as f:
    content = f.read()

# S3457 f-string with no fields:
content = re.sub(r'f"(.*?)"', lambda m: f'"{m.group(1)}"' if '{' not in m.group(1) else m.group(0), content)
content = re.sub(r"f'(.*?)'", lambda m: f"'{m.group(1)}'" if '{' not in m.group(1) else m.group(0), content)

with open('emailintelligence_cli.py', 'w') as f:
    f.write(content)

with open('src/cli/commands/infra/install_tools.py') as f:
    content = f.read()
content = re.sub(r'f"(.*?)"', lambda m: f'"{m.group(1)}"' if '{' not in m.group(1) else m.group(0), content)
with open('src/cli/commands/infra/install_tools.py', 'w') as f:
    f.write(content)

