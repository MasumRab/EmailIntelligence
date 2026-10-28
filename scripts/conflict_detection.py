import subprocess
import argparse
import sys
import json
import datetime
from typing import Dict, Any

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
        # Run git merge-tree
        # exit code 0 means clean merge, 1 means conflicts
        proc = subprocess.run(
            ["git", "merge-tree", "--write-tree", "--", target_branch, source_branch],
            capture_output=True,
            text=True,
            check=False
        )
        
        if proc.returncode == 0:
            return result
        elif proc.returncode == 1:
            result["conflict_detected"] = True
            
            lines = proc.stdout.splitlines()
            # The output of git merge-tree --write-tree includes the tree hash on the first line
            # followed by the conflict details.
            
            # Simple parsing for conflict files
            for line in lines:
                if line.startswith("CONFLICT "):
                    result["total_conflicts"] += 1
                    result["manual_resolution_required"] += 1
                    
                    # Example format: CONFLICT (content): Merge conflict in file.txt
                    parts = line.split(" in ")
                    if len(parts) > 1:
                        file_path = parts[-1]
                        
                        # simplistic parsing for type
                        conflict_type = "merge"
                        if "(modify/delete)" in line:
                            conflict_type = "modify/delete"
                            
                        result["conflict_files"].append({
                            "file_path": file_path,
                            "conflict_type": conflict_type,
                            "severity": "high",
                            "complexity_score": 0.5, # default
                            "resolution_status": "pending"
                        })
            
            if result["total_conflicts"] > 0:
                result["resolution_guidance"] = f"Manual resolution required for {result['total_conflicts']} files."
            
            return result
        else:
            print(f"Error running git merge-tree: {proc.stderr}", file=sys.stderr)
            result["conflict_detected"] = True
            return result
    except Exception as e:
        print(f"Error checking conflicts: {e}", file=sys.stderr)
        result["conflict_detected"] = True
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
