import re

with open('emailintelligence_cli.py') as f:
    content = f.read()

# Lines 826, 1145, 1519 are file open calls.
# We will create a helper method `_secure_open` on CommandDispatcher or globally, and use it.
helper = """
    def _secure_open(self, filepath: str, mode: str = 'r'):
        import os
        base_dir = os.path.realpath(self.repo_root) if hasattr(self, 'repo_root') else os.path.realpath('.')
        target = os.path.realpath(filepath)
        if os.path.commonpath([base_dir, target]) != base_dir:
            raise ValueError("Path traversal detected")
        flags = os.O_RDONLY if mode == 'r' else (os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        fd = os.open(target, flags | os.O_NOFOLLOW)
        return open(fd, mode)
"""

content = content.replace("class CommandDispatcher:", "class CommandDispatcher:\n" + helper)

content = re.sub(r"open\((args\.alignment_rules), 'r'\)", r"self._secure_open(\1, 'r')", content)
content = re.sub(r"open\((args\.strategy_file), 'r'\)", r"self._secure_open(\1, 'r')", content)
content = re.sub(r"open\(os\.path\.join\(self\.state_dir, f\"{session_id}\.json\"\), 'w'\)", r"self._secure_open(os.path.join(self.state_dir, f\"{session_id}.json\"), 'w')", content)

with open('emailintelligence_cli.py', 'w') as f:
    f.write(content)

with open('src/cli/state.py') as f:
    content = f.read()

helper2 = """
def secure_open(filepath: str, mode: str = 'r', base_dir: str = None):
    import os
    if base_dir is None:
        base_dir = os.path.realpath('.')
    else:
        base_dir = os.path.realpath(base_dir)
    target = os.path.realpath(filepath)
    if os.path.commonpath([base_dir, target]) != base_dir:
        raise ValueError("Path traversal detected")
    flags = os.O_RDONLY if mode == 'r' else (os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    fd = os.open(target, flags | os.O_NOFOLLOW)
    return open(fd, mode)
"""

content = content.replace("import json", "import json\n" + helper2)
content = content.replace("with open(state_file, 'w') as f:", "with secure_open(state_file, 'w', self.state_dir) as f:")
content = content.replace("with open(state_file, 'r') as f:", "with secure_open(state_file, 'r', self.state_dir) as f:")

with open('src/cli/state.py', 'w') as f:
    f.write(content)
