#!/usr/bin/env python3
import json
import argparse
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any

def get_git_status(branch: str, target: str) -> Dict[str, Any]:
    try:
        # Check if branch exists
        result = subprocess.run(
            ['git', 'rev-parse', '--verify', branch],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"status": "missing", "error": "Branch does not exist locally"}
            
        # Check if target exists
        result = subprocess.run(
            ['git', 'rev-parse', '--verify', target],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"status": "error", "error": f"Target branch '{target}' does not exist"}
        
        commits_ahead = 0
        commits_behind = 0
        
        # Check commits ahead/behind relative to target
        result = subprocess.run(
            ['git', 'rev-list', '--left-right', '--count', f'{target}...{branch}'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            counts = result.stdout.strip().split()
            if len(counts) == 2:
                # the first number is target (commits_behind), the second is branch (commits_ahead)
                commits_behind = int(counts[0])
                commits_ahead = int(counts[1])
                    
        return {
            "status": "exists",
            "commits_ahead": commits_ahead,
            "commits_behind": commits_behind
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def process_manifest(manifest_path: str) -> List[Dict[str, Any]]:
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    results = []
    branches = manifest.get('branches', [])
    
    for branch_info in branches:
        branch_name = branch_info.get('name')
        if not branch_name:
            continue
            
        target = branch_info.get('target', 'main')
        status = get_git_status(branch_name, target)
        
        results.append({
            "branch": branch_name,
            "target": target,
            "alignment_status": status
        })
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Check alignment status of branches from a manifest")
    parser.add_argument("manifest", help="Path to the JSON manifest file")
    parser.add_argument("--output", "-o", help="Path to write the output JSON (default: stdout)")
    
    args = parser.parse_args()
    
    if not Path(args.manifest).exists():
        print(f"Error: Manifest file '{args.manifest}' not found.", file=sys.stderr)
        sys.exit(1)
        
    results = process_manifest(args.manifest)
    
    output_data = {
        "summary": {
            "total_branches": len(results),
            "missing_branches": sum(1 for r in results if r["alignment_status"]["status"] == "missing"),
            "aligned_branches": sum(1 for r in results if r["alignment_status"]["status"] == "exists" and r["alignment_status"].get("commits_behind", 0) == 0)
        },
        "results": results
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Results written to {args.output}")
    else:
        print(json.dumps(output_data, indent=2))

if __name__ == "__main__":
    main()
