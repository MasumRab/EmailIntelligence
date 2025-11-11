#!/usr/bin/env python3

import os
import subprocess
import sys

def find_files_with_conflicts(root_dir):
    """Find all files with merge conflict markers."""
    files_with_conflicts = []

    # Use grep to find files with conflict markers
    try:
        result = subprocess.run(
            ['grep', '-rl', '<<<<<<< HEAD', '--include=*.py', '--include=*.md', '--include=*.sh',
             '--include=*.txt', '--include=*.toml', '--include=*.ts', '--include=*.json', root_dir],
            capture_output=True, text=True
        )
        if result.stdout:
            files_with_conflicts = result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Error finding files with conflicts: {e}")

    return files_with_conflicts

def resolve_conflicts_in_file(file_path):
    """Resolve merge conflicts by keeping the 'scientific' version (middle section)."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Process the content to resolve conflicts
        resolved_content = resolve_conflicts(content)

        # Write the resolved content back to the file
        with open(file_path, 'w') as f:
            f.write(resolved_content)

        print(f"Resolved conflicts in: {file_path}")
        return True
    except Exception as e:
        print(f"Error resolving conflicts in {file_path}: {e}")
        return False

def resolve_conflicts(content):
    """Resolve merge conflicts by keeping the 'scientific' version."""
    lines = content.split('\n')
    resolved_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is the start of a conflict
        if line.strip() == '<<<<<<< HEAD':
            # Skip until we find the ======= separator
            conflict_start = i
            while i < len(lines) and lines[i].strip() != '=======':
                i += 1

            # Skip the ======= line
            if i < len(lines):
                i += 1

            # Collect the middle section (scientific version)
            middle_section = []
            while i < len(lines) and not lines[i].strip().startswith('>>>>>>>'):
                middle_section.append(lines[i])
                i += 1

            # Skip the >>>>>>> line
            if i < len(lines):
                i += 1

            # Add the middle section to resolved content
            resolved_lines.extend(middle_section)
        else:
            # Regular line, just add it
            resolved_lines.append(line)
            i += 1

    return '\n'.join(resolved_lines)

def main():
    root_dir = '/home/masum/github/EmailIntelligence-corrupted'

    print("Finding files with merge conflicts...")
    files_with_conflicts = find_files_with_conflicts(root_dir)

    if not files_with_conflicts:
        print("No files with merge conflicts found.")
        return

    print(f"Found {len(files_with_conflicts)} files with merge conflicts.")

    resolved_count = 0
    error_count = 0

    for file_path in files_with_conflicts:
        if file_path:  # Skip empty strings
            if resolve_conflicts_in_file(file_path):
                resolved_count += 1
            else:
                error_count += 1

    print(f"\nSummary:")
    print(f"Resolved conflicts in {resolved_count} files")
    print(f"Errors encountered in {error_count} files")

    # Stage all changes
    print("\nStaging all changes...")
    try:
        subprocess.run(['git', 'add', '.'], cwd=root_dir, check=True)
        print("All changes staged successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error staging changes: {e}")

    # Commit the changes
    print("\nCommitting changes...")
    try:
        subprocess.run(['git', 'commit', '-m', 'Automatically resolve remaining merge conflicts'], cwd=root_dir, check=True)
        print("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")

    # Push the changes
    print("\nPushing changes...")
    try:
        subprocess.run(['git', 'push', 'origin', 'feature-notmuch-tagging-1'], cwd=root_dir, check=True)
        print("Changes pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing changes: {e}")

if __name__ == '__main__':
    main()