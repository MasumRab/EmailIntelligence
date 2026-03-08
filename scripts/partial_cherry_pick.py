#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse

def partial_cherry_pick(commit):
    # Detect repository root automatically from CWD
    try:
        repo_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"], 
                                  capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Current directory is not part of a git repository.")
        sys.exit(1)

    os.chdir(repo_dir)

    # Ensure working directory is clean
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if status.stdout.strip():
        print("Working directory is not clean. Stashing changes first...")
        subprocess.run(["git", "stash", "push", "-m", f"pre-partial-cherry-pick {commit}"])

    print(f"Analyzing commit {commit}...")
    result = subprocess.run(["git", "show", "--name-status", "--oneline", commit], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: Could not find commit {commit}")
        sys.exit(1)
        
    lines = result.stdout.strip().split('\n')[1:]

    added_files = []
    modified_files = []

    for line in lines:
        if not line.strip(): continue
        parts = line.split('\t')
        if len(parts) >= 2:
            status_flag = parts[0][0]
            file_path = parts[-1]
            
            if status_flag == 'A':
                added_files.append(file_path)
            elif status_flag == 'M':
                modified_files.append(file_path)

    # 1. Apply Added Files (Always safe)
    if added_files:
        print(f"--- Importing {len(added_files)} New Files ---")
        subprocess.run(["git", "checkout", commit, "--"] + added_files)
        subprocess.run(["git", "add"] + added_files)

    # 2. Attempt to cleanly merge Modified Files
    successful_mods = []
    failed_mods = []

    if modified_files:
        print(f"--- Attempting to Merge {len(modified_files)} Modified Files ---")
        for f in modified_files:
            patch = subprocess.run(["git", "show", commit, "--", f], capture_output=True)
            apply_res = subprocess.run(["git", "apply", "-3", "--whitespace=nowarn"], input=patch.stdout)
            
            if apply_res.returncode == 0:
                # Check for conflict markers
                has_conflicts = False
                if os.path.exists(f):
                    with open(f, 'r', errors='ignore') as file_obj:
                        content = file_obj.read()
                        if "<<<<<<<" in content or "=======" in content or ">>>>>>>" in content:
                            has_conflicts = True
                
                if has_conflicts:
                    print(f"  ✗ {f} (Conflict markers found, skipping)")
                    subprocess.run(["git", "checkout", "HEAD", "--", f], stderr=subprocess.DEVNULL)
                    failed_mods.append(f)
                else:
                    print(f"  ✓ {f} (Merged cleanly)")
                    subprocess.run(["git", "add", f])
                    successful_mods.append(f)
            else:
                print(f"  ✗ {f} (Merge failed structurally, skipping)")
                subprocess.run(["git", "checkout", "HEAD", "--", f], stderr=subprocess.DEVNULL)
                failed_mods.append(f)

    print("\n--- Summary ---")
    print(f"Added: {len(added_files)}")
    print(f"Merged: {len(successful_mods)}")
    print(f"Conflicts: {len(failed_mods)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Selective cherry-pick for EmailIntelligence that skips conflicts.")
    parser.add_argument("commit", help="The commit hash to cherry-pick from")
    args = parser.parse_args()
    partial_cherry_pick(args.commit)
