#!/usr/bin/env python3
"""
Documentation Branch Versioning Engine

Creates and manages branch-specific versions of documentation files.
Automatically generates branch-specific copies when documentation is modified.
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional


class DocsBranchVersioning:
    def __init__(self):
        self.main_branch = "main"
        self.scientific_branch = "scientific"
        self.docs_dir = Path("docs")
        self.supported_branches = [self.main_branch, self.scientific_branch]

    def get_current_branch(self) -> str:
        """Get the current git branch name."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    def get_modified_docs(self) -> List[str]:
        """Get list of modified documentation files in staging area."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            files = result.stdout.strip().split("\n")
            return [f for f in files if f.startswith("docs/") and f.endswith(".md")]
        except subprocess.CalledProcessError:
            return []

    def create_branch_version(self, file_path: str, branch: str) -> bool:
        """Create a branch-specific version of the documentation file."""
        if branch not in self.supported_branches:
            print(f"Warning: Branch '{branch}' not supported for versioning")
            return False

        source_path = Path(file_path)
        if not source_path.exists():
            print(f"Warning: Source file {file_path} does not exist")
            return False

        # Create branch-specific filename
        stem = source_path.stem
        suffix = source_path.suffix
        branch_specific_name = f"{stem}-{branch}{suffix}"
        branch_specific_path = source_path.parent / branch_specific_name

        try:
            # Copy the file
            import shutil

            shutil.copy2(source_path, branch_specific_path)

            # Add to git staging
            subprocess.run(["git", "add", str(branch_specific_path)], check=True)

            print(f"Created branch-specific version: {branch_specific_path}")
            return True

        except Exception as e:
            print(f"Error creating branch version for {file_path}: {e}")
            return False

    def process_changes(
        self, branch: Optional[str] = None, files: Optional[List[str]] = None
    ) -> bool:
        """Process documentation changes and create branch versions."""
        if branch is None:
            branch = self.get_current_branch()

        if branch not in self.supported_branches:
            print(f"Branch '{branch}' not supported for documentation versioning")
            return True  # Not an error, just not applicable

        if files is None:
            files = self.get_modified_docs()

        if not files:
            return True

        print(f"Processing {len(files)} documentation changes on branch '{branch}'")

        success_count = 0
        for file_path in files:
            if self.create_branch_version(file_path, branch):
                success_count += 1

        print(
            f"Successfully created {success_count}/{len(files)} branch-specific versions"
        )
        return success_count == len(files)

    def cleanup_versions(self, branch: str) -> None:
        """Clean up old branch-specific versions that are no longer needed."""
        if branch not in self.supported_branches:
            return

        pattern = f"*-{branch}.md"
        for file_path in self.docs_dir.rglob(pattern):
            # Check if the base file still exists
            base_name = file_path.name.replace(f"-{branch}", "")
            base_path = file_path.parent / base_name

            if not base_path.exists():
                print(f"Removing orphaned branch version: {file_path}")
                file_path.unlink()


def main():
    parser = argparse.ArgumentParser(description="Documentation Branch Versioning")
    parser.add_argument("--branch", help="Specify branch (default: current)")
    parser.add_argument("--files", nargs="*", help="Specific files to process")
    parser.add_argument(
        "--cleanup", action="store_true", help="Clean up orphaned versions"
    )

    args = parser.parse_args()

    versioning = DocsBranchVersioning()

    if args.cleanup:
        branch = args.branch or versioning.get_current_branch()
        versioning.cleanup_versions(branch)
        print("Cleanup completed")
        return

    success = versioning.process_changes(branch=args.branch, files=args.files)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
