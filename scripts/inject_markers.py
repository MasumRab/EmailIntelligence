#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse

def inject_markers(commit):
    # Detect repository root automatically from CWD
    try:
        repo_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"], 
                                  capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Current directory is not part of a git repository.")
        sys.exit(1)

    os.chdir(repo_dir)

    base = subprocess.run(["git", "merge-base", "HEAD", commit], capture_output=True, text=True).stdout.strip()
    if not base:
        print(f"Error: Could not find merge base for {commit}")
        sys.exit(1)

    result = subprocess.run(["git", "show", "--name-status", commit], capture_output=True, text=True)
    files = [line.split('\t')[1] for line in result.stdout.split('\n') if line.startswith('M\t')]

    count = 0
    for f in files:
        if not os.path.exists(f): continue
        
        with open(f"{f}.theirs", "w", encoding='utf-8') as theirs_f:
            subprocess.run(["git", "show", f"{commit}:{f}"], stdout=theirs_f)
        with open(f"{f}.base", "w", encoding='utf-8') as base_f:
            subprocess.run(["git", "show", f"{base}:{f}"], stdout=base_f)
        
        subprocess.run([
            "git", "merge-file",
            "-L", "Local Branch",
            "-L", "Merge Base",
            "-L", "Remote Change",
            f, f"{f}.base", f"{f}.theirs"
        ])
        
        if os.path.exists(f"{f}.theirs"): os.remove(f"{f}.theirs")
        if os.path.exists(f"{f}.base"): os.remove(f"{f}.base")
        count += 1
        print(f"  ✓ Conflict markers injected into {f}")

    print(f"\nSuccessfully processed {count} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject 3-way conflict markers for EmailIntelligence.")
    parser.add_argument("commit", help="Commit to compare against")
    args = parser.parse_args()
    inject_markers(args.commit)
