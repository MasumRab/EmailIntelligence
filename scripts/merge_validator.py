import argparse
import subprocess
import sys
import re
from typing import Set

def is_safe_ref(ref: str) -> bool:
    """Validate that a git reference contains only safe characters."""
    return bool(re.match(r'^[a-zA-Z0-9_./-]+$', ref)) and not ref.startswith('-')

def get_changed_files(base: str, head: str) -> Set[str]:
    """Get the set of changed files between two commits."""
    if not is_safe_ref(base) or not is_safe_ref(head):
        print(f"Error: Invalid reference provided ({base} or {head})", file=sys.stderr)
        sys.exit(1)
        
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--", f"{base}..{head}"], # NOSONAR
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return set(output.split('\n')) if output else set()
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def check_concurrent_changes(source_branch: str, target_branch: str) -> bool:
    """
    Check if there are any files changed in both the source and target branches
    since their common merge base. Returns True if conflicting files exist.
    """
    if not is_safe_ref(source_branch) or not is_safe_ref(target_branch):
        print("Error: Branch names contain invalid characters.", file=sys.stderr)
        sys.exit(1)
        
    # 1. Find the merge base
    try:
        result = subprocess.run(
            ["git", "merge-base", "--", target_branch, source_branch], # NOSONAR
            capture_output=True,
            text=True,
            check=True
        )
        merge_base = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error finding merge base: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    if not merge_base:
         print("Error: Could not determine merge base.", file=sys.stderr)
         sys.exit(1)

    print(f"Merge base: {merge_base}")

    # 2. Get files changed in target branch since merge base
    target_changed = get_changed_files(merge_base, target_branch)
    
    # 3. Get files changed in source branch since merge base
    source_changed = get_changed_files(merge_base, source_branch)

    # 4. Find intersection
    conflicting_files = target_changed.intersection(source_changed)

    if conflicting_files:
        print("\nERROR: Concurrent File Changes Detected!", file=sys.stderr)
        print(f"The following files have been changed in both '{source_branch}' and '{target_branch}' since their common merge base:", file=sys.stderr)
        for f in sorted(conflicting_files):
            print(f"  - {f}", file=sys.stderr)
        print("\nPlease rebase or merge the target branch and resolve any conflicts before proceeding.", file=sys.stderr)
        return True
    
    print("Success: No concurrently modified files detected.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Validate merge by checking for concurrently modified files.")
    parser.add_argument("source_branch", help="The branch to be merged (e.g., HEAD or feature-branch)")
    parser.add_argument("target_branch", help="The branch being merged into (e.g., main)")
    
    args = parser.parse_args()

    has_conflicts = check_concurrent_changes(args.source_branch, args.target_branch)
    if has_conflicts:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
