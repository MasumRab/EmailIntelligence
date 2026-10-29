#!/usr/bin/env python3
import subprocess
import json
import argparse
import re
import sys

_SAFE_REF = re.compile(r'[a-zA-Z0-9_./-]+')

def safe_ref(ref: str) -> str:
    """Return the reference, or raise if it is malformed or could be read as an option.

    The allowlist is matched, not merely tested: the matched text is what reaches
    argv, so the value git receives is the value the regex accepted. A boolean
    "reject if unsafe" helper leaves the original string in the taint graph and
    SonarCloud's pythonsecurity:S8705 keeps reporting the sink.
    """
    match = _SAFE_REF.fullmatch(ref)
    if not match or ref.startswith('-'):
        raise ValueError(ref)
    return match.group(0)

def get_reflog_history(branch_name: str, count: int = 5):
    """Gets the recent reflog history for a specific branch."""
    try:
        safe_branch = safe_ref(branch_name)
    except ValueError:
        print(f"Error: invalid branch name {branch_name!r}", file=sys.stderr)
        return []

    try:
        # Use git reflog show to get branch specific reflog
        result = subprocess.run(
            ['git', 'reflog', 'show', safe_branch, '-n', str(count), '--format=%h|%gs'],
            capture_output=True,
            text=True,
            check=True
        )
        entries = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|', 1)
                if len(parts) == 2:
                    entries.append({"hash": parts[0], "message": parts[1]})
        return entries
    except subprocess.CalledProcessError as e:
        print(f"Error accessing reflog for {branch_name}: {e.stderr}", file=sys.stderr)
        return []

def generate_restore_command(branch_name: str, commit_hash: str) -> str:
    """Generates the command to restore a branch to a specific commit."""
    return f"git branch -f {branch_name} {commit_hash}"

def analyze_recovery_options(branch_name: str) -> dict:
    """Analyzes recent changes and suggests recovery points."""
    entries = get_reflog_history(branch_name, 10)
    
    if not entries:
        return {
            "branch": branch_name,
            "status": "error",
            "message": f"No reflog history found for branch '{branch_name}'"
        }
    
    options = []
    for i, entry in enumerate(entries):
        options.append({
            "index": i,
            "commit_hash": entry["hash"],
            "description": entry["message"],
            "restore_command": generate_restore_command(branch_name, entry["hash"])
        })
        
    return {
        "branch": branch_name,
        "status": "success",
        "recovery_options": options
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find previous states of a branch using git reflog")
    parser.add_argument("branch", help="The name of the branch to analyze")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    results = analyze_recovery_options(args.branch)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if results["status"] == "error":
            print(f"Error: {results['message']}")
            sys.exit(1)
            
        print(f"Recovery options for branch: {args.branch}")
        print("-" * 50)
        for opt in results["recovery_options"]:
            print(f"[{opt['index']}] {opt['commit_hash']} - {opt['description']}")
            print(f"    Command: {opt['restore_command']}")
            print()
