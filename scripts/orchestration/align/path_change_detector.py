#!/usr/bin/env python3
"""
path_change_detector.py - Detect file path changes between branches

Usage:
    python3 path_change_detector.py <local_branch> <remote_branch>

Example:
    python3 path_change_detector.py HEAD origin/BRANCH
"""

import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class PathChange:
    old_path: str
    new_path: str
    change_type: str  # RENAMED, MOVED, DELETED, ADDED
    similar_files: List[str]
    action_required: str

    def __post_init__(self):
        # Ensure old_path and new_path are strings (not None)
        self.old_path = self.old_path or ""
        self.new_path = self.new_path or ""


def run_command(cmd: str) -> str:
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


class PathChangeDetector:
    def __init__(self, local_branch: str, remote_branch: str):
        self.local_branch = local_branch
        self.remote_branch = remote_branch
        self.local_files: Set[str] = set()
        self.remote_files: Set[str] = set()
        self.changes: List[PathChange] = []

    def scan_branches(self):
        """Scan both branches for file paths"""

        # Get local files
        result = run_command(f"git ls-tree -r --name-only {self.local_branch}")
        self.local_files = set(filter(None, result.strip().split("\n")))

        # Get remote files
        result = run_command(f"git ls-tree -r --name-only {self.remote_branch}")
        self.remote_files = set(filter(None, result.strip().split("\n")))

    def detect_changes(self):
        """Detect path changes between branches"""

        # Files only in local (added or renamed from remote)
        local_only = self.local_files - self.remote_files

        # Files only in remote (deleted or renamed to local)
        remote_only = self.remote_files - self.local_files

        # Common files
        common = self.local_files & self.remote_files

        print(f"=== Path Change Analysis ===")
        print(f"Local only:  {len(local_only)} files")
        print(f"Remote only: {len(remote_only)} files")
        print(f"Common:      {len(common)} files")
        print("")

        # Detect renames (files in both with similar names)
        for local_path in local_only:
            similar = self._find_similar_paths(local_path, remote_only)
            if similar:
                # Likely a rename
                change = PathChange(
                    old_path=similar[0],
                    new_path=local_path,
                    change_type="RENAMED",
                    similar_files=similar,
                    action_required=f"Update all references from '{similar[0]}' to '{local_path}'",
                )
                self.changes.append(change)
            else:
                # Likely a new file
                change = PathChange(
                    old_path=None,
                    new_path=local_path,
                    change_type="ADDED",
                    similar_files=[],
                    action_required="Verify file is correctly placed and add to version control",
                )
                self.changes.append(change)

        # Detect deletions
        for remote_path in remote_only:
            similar = self._find_similar_paths(remote_path, local_only)
            if not similar:
                change = PathChange(
                    old_path=remote_path,
                    new_path=None,
                    change_type="DELETED",
                    similar_files=[],
                    action_required="Verify file should be deleted and remove from version control",
                )
                self.changes.append(change)

    def _find_similar_paths(self, path: str, search_set: Set[str]) -> List[str]:
        """Find similar file paths using fuzzy matching"""
        similar = []

        # Simple heuristics
        path_parts = path.split("/")
        path_filename = path_parts[-1] if path_parts else ""

        for candidate in search_set:
            candidate_parts = candidate.split("/")
            candidate_filename = candidate_parts[-1] if candidate_parts else ""

            # Check if same filename
            if path_filename == candidate_filename and path != candidate:
                similar.append(candidate)
                continue

            # Check if similar directory structure
            if len(path_parts) >= 2 and len(candidate_parts) >= 2:
                common_parts = set(path_parts[:-1]) & set(candidate_parts[:-1])
                if (
                    len(common_parts)
                    / max(len(path_parts[:-1]), len(candidate_parts[:-1]))
                    > 0.5
                ):
                    similar.append(candidate)

        return similar[:3]  # Return top 3

    def generate_report(self) -> str:
        """Generate path change report"""
        report = []
        report.append("# Path Change Report")
        report.append(f"")
        report.append(f"Local branch:  {self.local_branch}")
        report.append(f"Remote branch: {self.remote_branch}")
        report.append(f"")
        report.append(f"**Summary:**")
        report.append(
            f"- Local only (added/renamed):  {len([c for c in self.changes if c.change_type in ['ADDED', 'RENAMED']])}"
        )
        report.append(
            f"- Remote only (deleted):       {len([c for c in self.changes if c.change_type == 'DELETED'])}"
        )
        report.append(f"- Total changes:                {len(self.changes)}")
        report.append(f"")

        # Group by change type
        renames = [c for c in self.changes if c.change_type == "RENAMED"]
        additions = [c for c in self.changes if c.change_type == "ADDED"]
        deletions = [c for c in self.changes if c.change_type == "DELETED"]

        if renames:
            report.append("## Renamed Files")
            report.append(f"")
            for change in renames:
                report.append(f"### {change.old_path} → {change.new_path}")
                report.append(f"")
                report.append(f"**Action Required:** {change.action_required}")
                report.append(f"")
                report.append("**Files that may need updating:**")
                # Find files that might reference this
                for py_file in Path(".").rglob("*.py"):
                    if "venv" in str(py_file) or "__pycache__" in str(py_file):
                        continue
                    try:
                        with open(py_file, "r") as f:
                            content = f.read()
                            if (
                                change.old_path in content
                                or change.old_path.replace("/", ".") in content
                            ):
                                report.append(f"- {py_file}")
                    except:
                        pass
                report.append(f"")

        if additions:
            report.append("## Added Files")
            report.append(f"")
            for change in additions:
                report.append(f"- {change.new_path}")
                report.append(f"  **Action:** {change.action_required}")
                report.append(f"")

        if deletions:
            report.append("## Deleted Files")
            report.append(f"")
            for change in deletions:
                report.append(f"- {change.old_path}")
                report.append(f"  **Action:** {change.action_required}")
                report.append(f"")

        return "\n".join(report)

    def generate_sql_updates(self) -> str:
        """Generate SQL statements to update references"""
        report = []
        report.append("-- SQL Updates for Path Changes")
        report.append("-- Run these in your database if you store file references")
        report.append("")

        renames = [c for c in self.changes if c.change_type == "RENAMED"]

        for change in renames:
            report.append(f"-- Update references to {change.old_path}")
            report.append(
                f"UPDATE files SET path = '{change.new_path}' WHERE path = '{change.old_path}';"
            )
            report.append(
                f"UPDATE imports SET module = '{change.new_path}' WHERE module = '{change.old_path}';"
            )
            report.append("")

        return "\n".join(report)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 path_change_detector.py <local_branch> <remote_branch>")
        print("")
        print("Arguments:")
        print("  local_branch  - Git ref for local branch (e.g., HEAD)")
        print("  remote_branch - Git ref for remote branch (e.g., origin/BRANCH)")
        print("")
        print("Example:")
        print("  python3 path_change_detector.py HEAD origin/BRANCH")
        sys.exit(1)

    local_branch = sys.argv[1]
    remote_branch = sys.argv[2]

    # Detect changes
    detector = PathChangeDetector(local_branch, remote_branch)
    detector.scan_branches()
    detector.detect_changes()

    # Generate and print report
    report = detector.generate_report()
    print(report)

    # Save report
    with open("PATH_CHANGE_REPORT.md", "w") as f:
        f.write(report)

    print("")
    print(f"✅ Report saved to: PATH_CHANGE_REPORT.md")

    # Generate SQL updates
    sql = detector.generate_sql_updates()
    with open("PATH_CHANGE_SQL_UPDATES.sql", "w") as f:
        f.write(sql)

    print(f"✅ SQL updates saved to: PATH_CHANGE_SQL_UPDATES.sql")


if __name__ == "__main__":
    main()
