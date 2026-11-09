#!/usr/bin/env python3

import os
import sys
import subprocess

def get_changed_files():
    try:
        # Get files changed between main and HEAD
        # Note: In a real CI environment, you might need origin/main or a specific target branch
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'main...HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        sys.exit(1)

def check_file_for_todos(filepath):
    if not os.path.exists(filepath):
        return False
    
    # Skip binary files or non-text files to avoid encoding errors
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if 'TODO' in line.upper():
                    print(f"Found TODO in {filepath} at line {line_num}: {line.strip()}")
                    return True
    except UnicodeDecodeError:
        pass # Skip files that aren't valid UTF-8
        
    return False

def main():
    changed_files = get_changed_files()
    
    if not changed_files:
        print("No changed files found.")
        sys.exit(0)
        
    failed = False
    for filepath in changed_files:
        if check_file_for_todos(filepath):
            failed = True
            
    if failed:
        print("\nValidation failed: TODOs found in changed files.")
        sys.exit(1)
    else:
        print("Validation passed: No TODOs found in changed files.")
        sys.exit(0)

if __name__ == "__main__":
    main()
