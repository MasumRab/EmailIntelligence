#!/usr/bin/env python3
"""
Atomic Commit Groups
Group related changes into atomic commits across worktrees.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess


@dataclass
class CommitGroup:
    group_id: str
    name: str
    description: str
    files: List[str]
    worktrees: List[str]
    created_at: str
    status: str = "pending"  # pending, in_progress, completed, failed
    commit_hashes: Dict[str, str] = None  # worktree -> commit_hash

    def __post_init__(self):
        if self.commit_hashes is None:
            self.commit_hashes = {}


class AtomicCommitManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.commit_groups_file = project_root / ".commit_groups.json"
        self.commit_groups: Dict[str, CommitGroup] = {}
        self.load_commit_groups()

    def load_commit_groups(self):
        """Load commit groups from file."""
        if self.commit_groups_file.exists():
            try:
                with open(self.commit_groups_file, "r") as f:
                    data = json.load(f)
                    for group_id, group_data in data.items():
                        # Convert dict to CommitGroup object
                        commit_hashes = group_data.pop("commit_hashes", {})
                        group = CommitGroup(**group_data)
                        group.commit_hashes = commit_hashes
                        self.commit_groups[group_id] = group
            except Exception as e:
                print(f"Error loading commit groups: {e}")

    def save_commit_groups(self):
        """Save commit groups to file."""
        try:
            data = {}
            for group_id, group in self.commit_groups.items():
                data[group_id] = asdict(group)
            with open(self.commit_groups_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving commit groups: {e}")

    def create_commit_group(
        self, name: str, description: str, files: List[str], worktrees: List[str]
    ) -> str:
        """Create a new atomic commit group."""
        # Generate unique group ID
        group_id = hashlib.sha256(
            f"{name}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        group = CommitGroup(
            group_id=group_id,
            name=name,
            description=description,
            files=files,
            worktrees=worktrees,
            created_at=datetime.now().isoformat(),
        )

        self.commit_groups[group_id] = group
        self.save_commit_groups()

        return group_id

    def get_commit_group(self, group_id: str) -> Optional[CommitGroup]:
        """Get a commit group by ID."""
        return self.commit_groups.get(group_id)

    def list_commit_groups(self, status: Optional[str] = None) -> List[CommitGroup]:
        """List commit groups, optionally filtered by status."""
        groups = list(self.commit_groups.values())
        if status:
            groups = [g for g in groups if g.status == status]
        return groups

    def execute_commit_group(self, group_id: str, commit_message: str) -> bool:
        """Execute an atomic commit group across all worktrees."""
        group = self.get_commit_group(group_id)
        if not group:
            print(f"Commit group {group_id} not found")
            return False

        if group.status != "pending":
            print(f"Commit group {group_id} is not in pending status")
            return False

        group.status = "in_progress"
        self.save_commit_groups()

        try:
            # Commit to each worktree
            success_count = 0
            for worktree in group.worktrees:
                worktree_path = self.project_root / "worktrees" / worktree
                if worktree_path.exists():
                    commit_hash = self._commit_to_worktree(
                        worktree_path, group.files, commit_message
                    )
                    if commit_hash:
                        group.commit_hashes[worktree] = commit_hash
                        success_count += 1
                    else:
                        print(f"Failed to commit to worktree {worktree}")
                else:
                    print(f"Worktree {worktree} not found")

            # Check if all commits were successful
            if success_count == len(group.worktrees):
                group.status = "completed"
                result = True
            else:
                group.status = "failed"
                result = False

            self.save_commit_groups()
            return result

        except Exception as e:
            group.status = "failed"
            self.save_commit_groups()
            print(f"Error executing commit group: {e}")
            return False

    def _commit_to_worktree(
        self, worktree_path: Path, files: List[str], commit_message: str
    ) -> Optional[str]:
        """Commit files to a specific worktree."""
        try:
            # Add files to git
            for file_path in files:
                full_path = worktree_path / file_path
                if full_path.exists():
                    subprocess.run(
                        ["git", "add", str(full_path)],
                        cwd=worktree_path,
                        check=True,
                        capture_output=True,
                    )

            # Create commit
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=worktree_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                # Get commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=worktree_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return hash_result.stdout.strip()
            else:
                # Check if it's because there's nothing to commit
                if "nothing to commit" in result.stderr:
                    # Get current HEAD hash
                    hash_result = subprocess.run(
                        ["git", "rev-parse", "HEAD"],
                        cwd=worktree_path,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    return hash_result.stdout.strip()
                else:
                    print(f"Git commit failed: {result.stderr}")
                    return None

        except subprocess.CalledProcessError as e:
            print(f"Git operation failed in {worktree_path}: {e}")
            return None
        except Exception as e:
            print(f"Error committing to {worktree_path}: {e}")
            return None

    def rollback_commit_group(self, group_id: str) -> bool:
        """Rollback a failed commit group."""
        group = self.get_commit_group(group_id)
        if not group:
            print(f"Commit group {group_id} not found")
            return False

        if group.status != "failed":
            print(f"Commit group {group_id} is not in failed status")
            return False

        try:
            # Rollback each worktree that had a successful commit
            for worktree, commit_hash in group.commit_hashes.items():
                worktree_path = self.project_root / "worktrees" / worktree
                if worktree_path.exists() and commit_hash:
                    # Reset to previous commit
                    subprocess.run(
                        ["git", "reset", "--hard", f"{commit_hash}~1"],
                        cwd=worktree_path,
                        check=True,
                        capture_output=True,
                    )

            group.status = "rolled_back"
            self.save_commit_groups()
            return True

        except Exception as e:
            print(f"Error rolling back commit group: {e}")
            return False

    def get_group_status(self, group_id: str) -> Dict:
        """Get detailed status of a commit group."""
        group = self.get_commit_group(group_id)
        if not group:
            return {"error": "Group not found"}

        return {
            "group_id": group.group_id,
            "name": group.name,
            "status": group.status,
            "files_count": len(group.files),
            "worktrees_count": len(group.worktrees),
            "successful_commits": len(group.commit_hashes),
            "created_at": group.created_at,
        }

    def get_statistics(self) -> Dict:
        """Get statistics about commit groups."""
        total_groups = len(self.commit_groups)
        pending_groups = len(
            [g for g in self.commit_groups.values() if g.status == "pending"]
        )
        completed_groups = len(
            [g for g in self.commit_groups.values() if g.status == "completed"]
        )
        failed_groups = len(
            [g for g in self.commit_groups.values() if g.status == "failed"]
        )
        rolled_back_groups = len(
            [g for g in self.commit_groups.values() if g.status == "rolled_back"]
        )

        return {
            "total_groups": total_groups,
            "pending_groups": pending_groups,
            "completed_groups": completed_groups,
            "failed_groups": failed_groups,
            "rolled_back_groups": rolled_back_groups,
            "success_rate": (completed_groups / total_groups * 100)
            if total_groups > 0
            else 0,
        }


def main():
    # Example usage
    print("Atomic Commit Groups System")
    print("=" * 30)

    # This would typically be initialized with the project root
    # manager = AtomicCommitManager(Path("."))

    print("Atomic commit manager initialized")
    print("System ready to group related changes into atomic commits across worktrees")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Create commit group for related documentation updates")
    print("  2. Execute atomic commit across all worktrees")
    print("  3. Rollback if any commit fails")
    print("  4. Ensure consistency across worktrees")


if __name__ == "__main__":
    main()
