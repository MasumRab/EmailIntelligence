#!/usr/bin/env python3
"""
intelligent_merger.py - Intelligently merge two versions of a file

Usage:
    python3 intelligent_merger.py <file> <local_ref> <remote_ref>

Example:
    python3 intelligent_merger.py src/core/security.py HEAD origin/BRANCH
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def run_command(cmd: str) -> str:
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def get_file_content(file_path: str, ref: str = "HEAD") -> str:
    """Get file content at specific ref"""
    try:
        return run_command(f"git show {ref}:{file_path}")
    except Exception as e:
        print(f"Error getting {file_path} at {ref}: {e}")
        return ""


def get_changed_lines(file_path: str, base_ref: str, target_ref: str) -> List[int]:
    """Get line numbers changed between base and target"""
    try:
        diff = run_command(f"git diff {base_ref}..{target_ref} -- {file_path}")
        changed_lines = set()

        for line in diff.split("\n"):
            if line.startswith("@@"):
                parts = line.split("+")
                if len(parts) > 1:
                    location = parts[1].split(" ")[0]
                    if "," in location:
                        start = int(location.split(",")[0])
                        count = int(location.split(",")[1])
                    else:
                        start = int(location)
                        count = 1

                    for i in range(start, start + count):
                        changed_lines.add(i)

        return sorted(list(changed_lines))
    except Exception as e:
        print(f"Error getting changed lines: {e}")
        return []


def intelligent_merge(
    file_path: str, local_ref: str, remote_ref: str
) -> Tuple[str, int]:
    """
    Intelligently merge local and remote versions.

    Strategy:
    1. Find common ancestor (base)
    2. Get content from base, local, and remote
    3. Apply changes from both versions where they don't conflict
    4. Mark conflicting areas with conflict markers

    Returns:
        Tuple of (merged_content, conflict_count)
    """

    # Get the merge base
    base_ref = run_command(f"git merge-base {local_ref} {remote_ref}").strip()

    if not base_ref:
        print("❌ Error: Could not find merge base")
        return "", -1

    # Get content from all three versions
    base_content = get_file_content(file_path, base_ref)
    local_content = get_file_content(file_path, local_ref)
    remote_content = get_file_content(file_path, remote_ref)

    if not base_content:
        print(f"❌ Error: Could not get base content for {file_path}")
        return "", -1

    base_lines = base_content.split("\n")
    local_lines = local_content.split("\n") if local_content else base_lines
    remote_lines = remote_content.split("\n") if remote_content else base_lines

    # Get changed lines from each version
    local_changes = get_changed_lines(file_path, base_ref, local_ref)
    remote_changes = get_changed_lines(file_path, base_ref, remote_ref)

    local_change_set = set(local_changes)
    remote_change_set = set(remote_changes)

    # Perform intelligent merge
    merged_lines = []
    conflict_count = 0

    max_lines = max(len(base_lines), len(local_lines), len(remote_lines))

    for i in range(max_lines):
        base_line = base_lines[i] if i < len(base_lines) else ""
        local_line = local_lines[i] if i < len(local_lines) else base_line
        remote_line = remote_lines[i] if i < len(remote_lines) else base_line

        line_num = i + 1  # 1-based for human readability

        local_changed = line_num in local_change_set
        remote_changed = line_num in remote_change_set

        if local_changed and remote_changed:
            # Both changed - conflict!
            merged_lines.append(f"<<<<<<< LOCAL ({local_ref})")
            merged_lines.append(local_line)
            merged_lines.append(f"=======")
            merged_lines.append(remote_line)
            merged_lines.append(f">>>>>>> REMOTE ({remote_ref})")
            conflict_count += 1
        elif local_changed:
            # Only local changed - use local
            merged_lines.append(local_line)
        elif remote_changed:
            # Only remote changed - use remote
            merged_lines.append(remote_line)
        else:
            # Neither changed - use base
            merged_lines.append(base_line)

    return "\n".join(merged_lines), conflict_count


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 intelligent_merger.py <file> <local_ref> <remote_ref>")
        print("")
        print("Arguments:")
        print("  file      - Path to file to merge")
        print("  local_ref - Git ref for local version (e.g., HEAD)")
        print("  remote_ref - Git ref for remote version (e.g., origin/BRANCH)")
        print("")
        print("Example:")
        print("  python3 intelligent_merger.py src/core/security.py HEAD origin/BRANCH")
        print("")
        print(
            "This will create a .merged file with intelligent combination of changes."
        )
        sys.exit(1)

    file_path = sys.argv[1]
    local_ref = sys.argv[2]
    remote_ref = sys.argv[3]

    # Verify file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    print("=" * 60)
    print("Intelligent Merger")
    print("=" * 60)
    print(f"File: {file_path}")
    print(f"Local ref: {local_ref}")
    print(f"Remote ref: {remote_ref}")
    print("")

    # Perform intelligent merge
    merged_content, conflict_count = intelligent_merge(file_path, local_ref, remote_ref)

    if conflict_count < 0:
        print("❌ Merge failed")
        sys.exit(1)

    # Write merged file
    output_file = file_path + ".merged"
    with open(output_file, "w") as f:
        f.write(merged_content)

    print(f"✅ Merged content written to: {output_file}")
    print(f"   Conflicts found: {conflict_count}")
    print("")

    if conflict_count == 0:
        print("✅ No conflicts - can use this file directly")
        print(f"   mv {output_file} {file_path}")
    else:
        print(f"⚠️ {conflict_count} conflicts found - manual resolution required")
        print(f"   1. Review {output_file}")
        print(f"   2. Resolve conflicts (remove <<<<<<< ======= >>>>>>> markers)")
        print(f"   3. Replace original: mv {output_file} {file_path}")
        print(f"   4. git add {file_path}")

    print("")
    print("=" * 60)

    return output_file, conflict_count


if __name__ == "__main__":
    main()
