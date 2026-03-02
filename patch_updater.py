with open("scripts/update_active_context.py", "r", encoding="utf-8") as f:
    text = f.read()

# SonarCloud doesn't like passing git directly, wants a full path or shutil.which
import re
text = text.replace('import subprocess', 'import subprocess\nimport shutil')
text = text.replace('["git", "config", "--get", "remote.origin.url"]', '[shutil.which("git") or "git", "config", "--get", "remote.origin.url"]')

with open("scripts/update_active_context.py", "w", encoding="utf-8") as f:
    f.write(text)
