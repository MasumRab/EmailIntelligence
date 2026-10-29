import subprocess
import argparse
import sys
import json
import datetime
import re
from typing import Any, Dict, List

_SAFE_REF = re.compile(r"[a-zA-Z0-9_./-]+")


def safe_ref(ref: str) -> str:
    """Return the reference, or raise if it is malformed or could be read as an option.

    The allowlist is matched, not merely tested: the matched text is what reaches
    argv, so the value git receives is the value the regex accepted. A boolean
    "reject if unsafe" helper leaves the original string in the taint graph and
    SonarCloud's pythonsecurity:S8705 keeps reporting the sink. The `--` separator
    below is belt and braces for the same concern.
    """
    match = _SAFE_REF.fullmatch(ref)
    if not match or ref.startswith("-"):
        raise ValueError(ref)
    return match.group(0)


def _conflict_type(line: str) -> str:
    """Classify one `CONFLICT` line from `git merge-tree --write-tree` output."""
    return "modify/delete" if "(modify/delete)" in line else "merge"


def collect_conflicts(stdout: str) -> Dict[str, Any]:
    """Parse `git merge-tree --write-tree` output into the summary fields."""
    conflict_files: List[Dict[str, Any]] = []
    total = 0
    for line in stdout.splitlines():
        if not line.startswith("CONFLICT "):
            continue
        total += 1
        # Example format: CONFLICT (content): Merge conflict in file.txt
        parts = line.split(" in ")
        if len(parts) > 1:
            conflict_files.append({
                "file_path": parts[-1],
                "conflict_type": _conflict_type(line),
                "severity": "high",
                "complexity_score": 0.5,  # default
                "resolution_status": "pending",
            })
    return {
        "conflict_files": conflict_files,
        "total_conflicts": total,
    }


def check_conflicts(target_branch: str, source_branch: str = "HEAD") -> Dict[str, Any]:
    result = {
        "conflict_detected": False,
        "conflict_files": [],
        "total_conflicts": 0,
        "automated_resolution_attempts": 0,
        "manual_resolution_required": 0,
        "resolution_guidance": "",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    }
    
    try:
        safe_target = safe_ref(target_branch)
        safe_source = safe_ref(source_branch)
    except ValueError as rejected:
        print(f"Error: invalid branch name {rejected.args[0]!r}", file=sys.stderr)
        result["conflict_detected"] = True
        return result

    try:
        # Run git merge-tree
        # exit code 0 means clean merge, 1 means conflicts
        proc = subprocess.run(
            ["git", "merge-tree", "--write-tree", "--", safe_target, safe_source],
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as e:
        print(f"Error checking conflicts: {e}", file=sys.stderr)
        result["conflict_detected"] = True
        return result

    if proc.returncode == 0:
        return result
    if proc.returncode != 1:
        print(f"Error running git merge-tree: {proc.stderr}", file=sys.stderr)
        result["conflict_detected"] = True
        return result

    result["conflict_detected"] = True

    # The output of git merge-tree --write-tree includes the tree hash on the first
    # line, followed by the conflict details.
    summary = collect_conflicts(proc.stdout)
    result["conflict_files"] = summary["conflict_files"]
    result["total_conflicts"] = summary["total_conflicts"]
    result["manual_resolution_required"] = summary["total_conflicts"]

    if result["total_conflicts"] > 0:
        result["resolution_guidance"] = f"Manual resolution required for {result['total_conflicts']} files."

    return result

def main():
    parser = argparse.ArgumentParser(description="Check for merge conflicts between branches.")
    parser.add_argument("target_branch", help="The branch to merge into.")
    parser.add_argument("--source", default="HEAD", help="The source branch (default: HEAD).")
    parser.add_argument("--json", action="store_true", help="Output in JSON format.")
    
    args = parser.parse_args()
    
    result = check_conflicts(args.target_branch, args.source)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["conflict_detected"]:
            print("Conflicts detected:")
            for cf in result["conflict_files"]:
                print(f"  - {cf['file_path']} ({cf['conflict_type']})")
        else:
            print("No conflicts detected.")
            
    sys.exit(1 if result["conflict_detected"] else 0)

if __name__ == "__main__":
    main()
