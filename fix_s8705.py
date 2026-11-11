import re

with open("emailintelligence_cli.py", "r") as f:
    content = f.read()

# Fix 1: git checkout -b
content = re.sub(
    r'subprocess\.run\(\["git", "checkout", "-b", (.*?)\]\)',
    r'subprocess.run(["git", "checkout", "-b", \1, "--"])',
    content
)

content = re.sub(
    r'subprocess\.run\(\["git", "worktree", "add", (.*?)\]\)',
    r'subprocess.run(["git", "worktree", "add", \1, "--"])',
    content
)

with open("emailintelligence_cli.py", "w") as f:
    f.write(content)

