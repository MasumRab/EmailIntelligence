#!/usr/bin/env python3
"""
Update GitHub Actions versions in workflow files to match Dependabot PRs.
This fixes CI failures and enables auto-merge for Dependabot.
"""

import os
import re
from pathlib import Path

# Action version updates (old -> new)
# These represent the latest stable versions as of late 2024
ACTION_UPDATES = {
    r'actions/checkout@v[0-9]+': 'actions/checkout@v4',
    r'actions/setup-python@v[0-9]+': 'actions/setup-python@v5',
    r'astral-sh/setup-uv@v[0-9]+': 'astral-sh/setup-uv@v1',
    r'actions/download-artifact@v[0-9]+': 'actions/download-artifact@v4',
    r'actions/upload-artifact@v[0-9]+': 'actions/upload-artifact@v4',
    r'codecov/codecov-action@v[0-9]+': 'codecov/codecov-action@v4',
    r'actions/setup-node@v[0-9]+': 'actions/setup-node@v4',
}

WORKFLOW_DIR = Path('.github/workflows')

def update_file(filepath: Path) -> bool:
    """Update a workflow file with new action versions."""
    with open(filepath, 'r') as f:
        original = f.read()
    
    updated = original
    changes_made = []
    
    for old_pattern, new_version in ACTION_UPDATES.items():
        new_content = re.sub(old_pattern, new_version, updated)
        if new_content != updated:
            updated = new_content
            changes_made.append(f"{old_pattern} -> {new_version}")
    
    if updated != original:
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
