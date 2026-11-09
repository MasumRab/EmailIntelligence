import subprocess
import sys

def check_branch_status(branch):
    try:
        # Try to merge main into branch in memory without modifying working tree
        base = subprocess.run(['git', 'merge-base', 'main', branch], capture_output=True, text=True, check=True).stdout.strip()  # NOSONAR
        result = subprocess.run(['git', 'merge-tree', base, 'main', branch], capture_output=True, text=True, check=True)  # NOSONAR
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
