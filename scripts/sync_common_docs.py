#!/usr/bin/env python3
"""
Worktree Documentation Inheritance Sync Script (Python version)

Synchronizes common documentation across worktrees with cross-platform support.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


class DocumentationSync:
    """Handles synchronization of common documentation across worktrees."""

    def __init__(self, project_root: Path, conflict_strategy: str = "overwrite"):
        self.project_root = project_root
        self.worktrees_dir = project_root / "worktrees"
        self.inheritance_base = project_root / "docs"
        self.conflict_strategy = conflict_strategy

    def print_status(self, message: str):
        print(f"[INFO] {message}")

    def print_success(self, message: str):
        print(f"[SUCCESS] {message}")

    def print_warning(self, message: str):
        print(f"[WARNING] {message}")

    def print_error(self, message: str):
        print(f"[ERROR] {message}")

    def sync_from_inheritance_base(self) -> bool:
        """Sync common docs from inheritance base to all worktrees."""
        self.print_status("Syncing from inheritance base to all worktrees")

        if not self.inheritance_base.exists():
            self.print_error(f"Inheritance base not found: {self.inheritance_base}")
            return False

        success = True

        # Sync to main worktree
        main_worktree = self.worktrees_dir / "docs-main"
        if main_worktree.exists():
            self.print_status("Syncing to docs-main worktree")
            target_dir = main_worktree / "docs" / "common" / "docs"
            target_dir.mkdir(parents=True, exist_ok=True)

            try:
                self._sync_directory(
                    self.inheritance_base, target_dir, self.conflict_strategy
                )
                self.print_success("Synced to docs-main worktree")
            except Exception as e:
                self.print_error(f"Failed to sync to docs-main: {e}")
                success = False
        else:
            self.print_warning("docs-main worktree not found, skipping")

        # Sync to scientific worktree
        scientific_worktree = self.worktrees_dir / "docs-scientific"
        if scientific_worktree.exists():
            self.print_status("Syncing to docs-scientific worktree")
            target_dir = scientific_worktree / "docs" / "common" / "docs"
            target_dir.mkdir(parents=True, exist_ok=True)

            try:
                self._sync_directory(
                    self.inheritance_base, target_dir, self.conflict_strategy
                )
                self.print_success("Synced to docs-scientific worktree")
            except Exception as e:
                self.print_error(f"Failed to sync to docs-scientific: {e}")
                success = False
        else:
            self.print_warning("docs-scientific worktree not found, skipping")

        return success

    def sync_between_worktrees(self, source: str, target: str) -> bool:
        """Sync common docs between specific worktrees."""
        self.print_status(f"Syncing common docs from {source} to {target}")

        source_worktree = self.worktrees_dir / source
        target_worktree = self.worktrees_dir / target

        if not source_worktree.exists():
            self.print_error(f"Source worktree {source} does not exist")
            return False

        if not target_worktree.exists():
            self.print_error(f"Target worktree {target} does not exist")
            return False

        source_common = source_worktree / "docs" / "common" / "docs"
        target_common = target_worktree / "docs" / "common" / "docs"

        if not source_common.exists():
            self.print_error(f"Source common docs not found: {source_common}")
            return False

        target_common.mkdir(parents=True, exist_ok=True)

        try:
            self._sync_directory(source_common, target_common, self.conflict_strategy)
            self.print_success(f"Synced common docs from {source} to {target}")
            return True
        except Exception as e:
            self.print_error(f"Failed to sync between worktrees: {e}")
            return False

    def check_worktree_status(self):
        """Check the status of all worktrees."""
        self.print_status("Checking worktree status")

        print("\nWorktrees found:")
        os.system("git worktree list")

        print("\nWorktree documentation status:")

        # Check main worktree
        main_worktree = self.worktrees_dir / "docs-main"
        if main_worktree.exists():
            common_count = len(list((main_worktree / "docs" / "common").rglob("*.md")))
            branch_count = len(list((main_worktree / "docs" / "main").rglob("*.md")))
            print(
                f"docs-main: {common_count} common docs, {branch_count} branch-specific docs"
            )
        else:
            print("docs-main: NOT FOUND")

        # Check scientific worktree
        scientific_worktree = self.worktrees_dir / "docs-scientific"
        if scientific_worktree.exists():
            common_count = len(
                list((scientific_worktree / "docs" / "common").rglob("*.md"))
            )
            branch_count = len(
                list((scientific_worktree / "docs" / "scientific").rglob("*.md"))
            )
            print(
                f"docs-scientific: {common_count} common docs, {branch_count} branch-specific docs"
            )
        else:
            print("docs-scientific: NOT FOUND")

    def _sync_directory(
        self, source: Path, target: Path, conflict_strategy: str = "overwrite"
    ):
        """Sync contents of source directory to target directory with conflict resolution."""
        import filecmp

        conflicts = []
        updates = []

        # Walk through source directory
        for source_path in source.rglob("*"):
            if source_path.is_file():
                # Calculate relative path from source
                relative_path = source_path.relative_to(source)
                target_path = target / relative_path

                # Create target directory if needed
                target_path.parent.mkdir(parents=True, exist_ok=True)

                if target_path.exists():
                    # File exists in target - check for conflicts
                    if not filecmp.cmp(source_path, target_path, shallow=False):
                        # Files differ - handle conflict
                        conflict_handled = self._handle_conflict(
                            source_path, target_path, relative_path, conflict_strategy
                        )
                        if conflict_handled:
                            conflicts.append(str(relative_path))
                        else:
                            updates.append(str(relative_path))
                    # If files are identical, do nothing
                else:
                    # File doesn't exist in target - copy it
                    shutil.copy2(source_path, target_path)
                    updates.append(str(relative_path))

        # Report results
        if updates:
            print(f"  Updated {len(updates)} files")
        if conflicts:
            print(f"  Resolved {len(conflicts)} conflicts")

    def _handle_conflict(
        self, source_path: Path, target_path: Path, relative_path: Path, strategy: str
    ) -> bool:
        """Handle file conflicts based on the specified strategy.

        Returns True if conflict was detected and handled, False if file was updated normally.
        """
        from datetime import datetime

        if strategy == "overwrite":
            # Always overwrite target with source
            shutil.copy2(source_path, target_path)
            return False  # Not really a conflict, just an update

        elif strategy == "backup":
            # Create backup of target before overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = target_path.with_suffix(
                f"{target_path.suffix}.backup_{timestamp}"
            )
            shutil.copy2(target_path, backup_path)
            print(f"    Backed up conflicting file: {backup_path.name}")
            shutil.copy2(source_path, target_path)
            return True

        elif strategy == "skip":
            # Skip conflicting files
            print(f"    Skipped conflicting file: {relative_path}")
            return True

        elif strategy == "newer":
            # Overwrite only if source is newer
            source_mtime = source_path.stat().st_mtime
            target_mtime = target_path.stat().st_mtime

            if source_mtime > target_mtime:
                shutil.copy2(source_path, target_path)
                print(f"    Updated newer file: {relative_path}")
            else:
                print(f"    Kept existing newer file: {relative_path}")
            return True

        else:
            # Unknown strategy - default to overwrite
            self.print_warning(
                f"Unknown conflict strategy '{strategy}', using 'overwrite'"
            )
            shutil.copy2(source_path, target_path)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Worktree Documentation Inheritance Sync Script"
    )
    parser.add_argument(
        "--sync-from-base",
        "-b",
        action="store_true",
        help="Sync from inheritance base to all worktrees",
    )
    parser.add_argument(
        "--sync-between",
        "-s",
        nargs=2,
        metavar=("SOURCE", "TARGET"),
        help="Sync common docs between specific worktrees",
    )
    parser.add_argument(
        "--status",
        "-t",
        action="store_true",
        help="Check worktree documentation status",
    )
    parser.add_argument(
        "--conflict-strategy",
        "-c",
        choices=["overwrite", "backup", "skip", "newer"],
        default="overwrite",
        help="Strategy for handling file conflicts (default: overwrite)",
    )

    args = parser.parse_args()

    # Find project root
    current = Path(__file__).resolve().parent.parent
    if (current / "docs").exists() and (current / ".git").exists():
        project_root = current
    else:
        print("[ERROR] Could not find project root")
        sys.exit(1)

    sync = DocumentationSync(project_root, args.conflict_strategy)

    if args.sync_from_base:
        success = sync.sync_from_inheritance_base()
        sys.exit(0 if success else 1)
    elif args.sync_between:
        source, target = args.sync_between
        success = sync.sync_between_worktrees(source, target)
        sys.exit(0 if success else 1)
    elif args.status:
        sync.check_worktree_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
