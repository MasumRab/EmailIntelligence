import re
import subprocess
import sys

_SAFE_REF = re.compile(r'^[A-Za-z0-9][A-Za-z0-9/_.-]*$')

def _safe_ref(name: str) -> str:
    """Return the regex-matched branch name. A bool check leaves the raw argv value tainted."""
    match = _SAFE_REF.match(name or "")
    if not match:
        raise ValueError(name)
    return match.group(0)

def check_branch_status(branch):
    try:
        branch = _safe_ref(branch)
    except ValueError:
        return "error"
    try:
        # Try to merge main into branch in memory without modifying working tree
        base = subprocess.run(['git', 'merge-base', 'main', '--', branch], capture_output=True, text=True, check=True).stdout.strip()
        result = subprocess.run(['git', 'merge-tree', base, 'main', '--', branch], capture_output=True, text=True, check=True)
        if '<<<<<<<' in result.stdout:
            return "conflicting"
        return "clean"
    except subprocess.CalledProcessError:
        return "error"

def process_branches(branches):
    results = {}
    for branch in branches:
        results[branch] = check_branch_status(branch)
        print(f"{branch}: {results[branch]}")
    return results

if __name__ == '__main__':
    process_branches(sys.argv[1:])
