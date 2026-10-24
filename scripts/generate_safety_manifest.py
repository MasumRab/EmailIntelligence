#!/usr/bin/env python3
import subprocess
import json
import os
import sys

def get_local_branches_and_shas():
    try:
        result = subprocess.run(
            ['git', 'for-each-ref', '--format=%(refname:short) %(objectname)', 'refs/heads/'],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running git: {e}", file=sys.stderr)
        return {}

    branches = {}
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                branch, sha = parts
                branches[branch] = sha
    return branches

def write_manifest(output_path, branches):
    manifest = {
        "branches": branches
    }
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def main():
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = "safety_manifest.json"
    
    branches = get_local_branches_and_shas()
    write_manifest(output_path, branches)
    print(f"Safety manifest written to {output_path}")

if __name__ == '__main__':
    main()
