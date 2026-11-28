import re
with open('emailintelligence_cli.py') as f:
    lines = f.readlines()

validation_code = """
        def _validate_branch(branch: str) -> None:
            if not re.match(r'^[A-Za-z0-9_./][A-Za-z0-9_./-]*$', branch):
                raise ValueError(f"Invalid branch name: {branch}")
        
        _validate_branch(source_branch)
        _validate_branch(target_branch)
        _validate_branch(resolution_branch)
"""

for i, line in enumerate(lines):
    if "resolution_branch = f\"resolution/{source_branch}-into-{target_branch}\"" in line:
        lines.insert(i+1, validation_code)
        break

with open('emailintelligence_cli.py', 'w') as f:
    f.writelines(lines)
