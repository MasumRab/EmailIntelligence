#!/usr/bin/env python3
"""
Update GitHub Actions versions in workflow files to match Dependabot PRs.
This fixes CI failures and enables auto-merge for Dependabot.
"""

import os
import re
from pathlib import Path

# Action version updates (old -> new)
ACTION_UPDATES = {
    r'actions/checkout@v4': 'actions/checkout@v6',
    r'actions/checkout@v5': 'actions/checkout@v6',
    r'actions/setup-python@v4': 'actions/setup-python@v6',
    r'actions/setup-python@v5': 'actions/setup-python@v6',
    r'astral-sh/setup-uv@v4': 'astral-sh/setup-uv@v7',
    r'astral-sh/setup-uv@v5': 'astral-sh/setup-uv@v7',
    r'astral-sh/setup-uv@v6': 'astral-sh/setup-uv@v7',
    r'actions/download-artifact@v4': 'actions/download-artifact@v8',
    r'actions/download-artifact@v5': 'actions/download-artifact@v8',
    r'actions/upload-artifact@v4': 'actions/upload-artifact@v5',
    r'codecov/codecov-action@v4': 'codecov/codecov-action@v5',
}

WORKFLOW_DIR = Path('.github/workflows')

def update_file(filepath: Path) -> bool:
    """Update a workflow file with new action versions."""
    with open(filepath, 'r') as f:
        original = f.read()
    
    updated = original
    changes_made = []
    
    for old_pattern, new_version in ACTION_UPDATES.items():
        if re.search(old_pattern, updated):
            updated = re.sub(old_pattern, new_version, updated)
            changes_made.append(f"{old_pattern} -> {new_version}")
    
    if changes_made:
        with open(filepath, 'w') as f:
            f.write(updated)
        print(f"\n✓ Updated: {filepath}")
        for change in changes_made:
            print(f"    {change}")
        return True
    else:
        print(f"\n- No changes: {filepath}")
        return False

def main():
    print("=== GitHub Actions Version Updater ===")
    print(f"Scanning: {WORKFLOW_DIR.absolute()}")
    print()
    
    if not WORKFLOW_DIR.exists():
        print(f"Error: {WORKFLOW_DIR} not found!")
        return 1
    
    updated_count = 0
    for yml_file in WORKFLOW_DIR.glob('*.yml'):
        if update_file(yml_file):
            updated_count += 1
    
    print()
    print(f"=== Summary ===")
    print(f"Files updated: {updated_count}")
    print()
    print("Next steps:")
    print("1. Review changes: git diff")
    print("2. Commit: git add .github/workflows/*.yml && git commit -m 'ci: update action versions for Dependabot compatibility'")
    print("3. Push: git push origin main")
    print("4. Re-run CI on Dependabot PRs")
    print("5. Merge Dependabot PRs: gh pr merge --auto --merge <PR_NUMBER>")
    
    return 0

if __name__ == '__main__':
    exit(main())
