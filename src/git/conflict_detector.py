"""
Git-based conflict detection for EmailIntelligence CLI

This module implements the IConflictDetector interface using native git commands
to identify conflicts between branches without checking them out.
"""

from typing import List, Optional, Dict
from pathlib import Path
import re
import hashlib
import subprocess

# Local interface definition to avoid circular imports
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ConflictTypeExtended(Enum):
    """Extended types of conflicts"""

    CONTENT = "content"
    MERGE = "merge"
    FILE_DELETE = "file_delete"
    PERMISSION = "permission"
    BINARY = "binary"
    SEMANTIC = "semantic"
    LOGICAL = "logical"
    ARCHITECTURAL = "architectural"


class RiskLevel(Enum):
    """Risk levels for conflicts"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ConflictBlock:
    """Represents a single conflict block in a file"""

    start_line: int
    end_line: int
    conflict_type: "ConflictTypeExtended"
    content_before: List[str]
    content_after: List[str]
    content_common: List[str]
    original_content: Optional[List[str]] = None


@dataclass
class Conflict:
    """Represents a git conflict"""

    file_path: str
    conflict_blocks: List[ConflictBlock]
    conflict_type: "ConflictTypeExtended"
    severity: "RiskLevel"
    description: str = ""
    resolution_strategy: str = ""
    affected_components: List[str] = None
    estimated_resolution_time: int = 0  # in minutes

    def __post_init__(self):
        if self.affected_components is None:
            self.affected_components = []


class IConflictDetector(ABC):
    """
    Interface for conflict detection components.
    Responsible for identifying conflicts between git branches or PRs.
    """

    @abstractmethod
    async def detect_conflicts(self, pr_id: str, target_branch: str) -> List[Conflict]:
        """
        Detect conflicts between a PR and a target branch.

        Args:
            pr_id: The pull request ID to analyze
            target_branch: The target branch to compare against

        Returns:
            List of detected conflicts
        """
        pass


class ConflictDetectionError(Exception):
    """Raised when conflict detection fails."""

    pass


class RiskLevel(Enum):
    """Risk levels for conflicts"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IConflictDetector(ABC):
    """
    Interface for conflict detection components.
    Responsible for identifying conflicts between git branches or PRs.
    """

    @abstractmethod
    async def detect_conflicts(self, pr_id: str, target_branch: str) -> List[Conflict]:
        """
        Detect conflicts between a PR and a target branch.

        Args:
            pr_id: The pull request ID to analyze
            target_branch: The target branch to compare against

        Returns:
            List of detected conflicts
        """
        pass


from typing import List, Optional, Dict, Any
from pathlib import Path
import re
import hashlib
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any

from ..core.exceptions import ConflictDetectionError
from ..utils.logger import get_logger
from .repository import RepositoryOperations


logger = get_logger(__name__)


class GitConflictDetector(IConflictDetector):
    """
    Detects conflicts using git merge-tree operations and file parsing.
    """

    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path.cwd()
        self.repo_ops = RepositoryOperations(self.repo_path)

    def detect_conflicts(self, pr_id: str, target_branch: str) -> List[Conflict]:
        """
        Detect conflicts between a PR and a target branch using git merge-tree.

        Args:
            pr_id: The pull request ID (typically a branch name)
            target_branch: The target branch to compare against

        Returns:
            List of detected conflicts
        """
        try:
            # Get the source branch from PR ID
            source_branch = self._get_source_branch_from_pr(pr_id)

            # Use git merge-tree to detect conflicts without checking out
            conflicts = self._detect_conflicts_with_merge_tree(
                source_branch, target_branch
            )

            logger.info(
                f"Detected {len(conflicts)} conflicts between {source_branch} and {target_branch}"
            )
            return conflicts

        except Exception as e:
            logger.error(f"Error detecting conflicts: {e}")
            raise ConflictDetectionError(f"Failed to detect conflicts: {str(e)}")

    async def detect_conflicts_between_branches(
        self, source_branch: str, target_branch: str
    ) -> List[Conflict]:
        """Async wrapper used by AnalyzeCommand.

        The detector's merge-tree path is synchronous; the command awaits this
        coroutine so the CLI can dispatch it uniformly alongside the other
        async commands.
        """
        return self.detect_conflicts(source_branch, target_branch)

    def _get_source_branch_from_pr(self, pr_id: str) -> str:
        """
        Get the source branch name from a PR ID.
        """
        if pr_id.isdigit():
            return f"pr-{pr_id}"
        else:
            return pr_id

    def _detect_conflicts_with_merge_tree(
        self, source_branch: str, target_branch: str
    ) -> List[Conflict]:
        """
        Use git merge-tree to detect conflicts between branches.
        """
        try:
            # Run git merge-tree to detect conflicts
            def _resolve(ref: str) -> str:
                """merge-tree needs commits, not 'refs/heads/HEAD'."""
                out, _err, rc = self.repo_ops.run_command_sync(
                    ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"]
                )
                if rc != 0:
                    raise ConflictDetectionError(
                        f"cannot resolve ref '{ref}' to a commit"
                    )
                return out.strip()

            cmd = [
                "git",
                "merge-tree",
                _resolve(target_branch),
                _resolve(source_branch),
            ]

            stdout, stderr, return_code = self.repo_ops.run_command_sync(cmd)

            # exit 0 = clean, exit 1 = conflicts found (the normal both-dirty case).
            # Anything else, or a ref that will not resolve, is a failed measurement —
            # parsing stdout then reports "no conflicts" for a comparison that never ran.
            if "not something we can merge" in (stderr or ""):
                raise ConflictDetectionError(
                    f"git merge-tree could not resolve a ref: {stderr.strip()}"
                )
            if return_code not in (0, 1):
                raise ConflictDetectionError(
                    f"git merge-tree failed ({return_code}): {stderr.strip()}"
                )

            # Parse the merge-tree output for conflicts
            conflicts = self._parse_merge_tree_output(
                stdout, source_branch, target_branch
            )
            return conflicts

        except Exception as e:
            logger.error(f"Error running git merge-tree: {e}")
            raise ConflictDetectionError(f"Failed to run git merge-tree: {str(e)}")

    async def detect_conflicts_between_branches(
        self, source_branch: str, target_branch: str
    ) -> List[Conflict]:
        """Async wrapper used by AnalyzeCommand.

        The detector's merge-tree path is synchronous; the command awaits this
        coroutine so the CLI can dispatch it uniformly alongside the other
        async commands.
        """
        return self.detect_conflicts(source_branch, target_branch)

    def _get_source_branch_from_pr(self, pr_id: str) -> str:
        """
        Get the source branch name from a PR ID.
        """
        if pr_id.isdigit():
            return f"pr-{pr_id}"
        else:
            return pr_id

    def _parse_merge_tree_output(
        self, stdout: str, source_branch: str, target_branch: str
    ) -> List[Conflict]:
        """
        Parse git merge-tree output to extract conflicts.
        """
        conflicts = []

        # git merge-tree output format parsing
        # Look for conflict markers and affected files
        lines = stdout.split("\n")
        current_file = None
        in_conflict = False
        conflict_lines = []

        for line in lines:
            # Detect file changes
            if line.startswith("changed in "):
                if current_file and in_conflict:
                    # Process previous conflict
                    conflict = self._parse_conflict_block(
                        current_file, conflict_lines, source_branch
                    )
                    if conflict:
                        conflicts.append(conflict)

                current_file = line.replace("changed in ", "").strip()
                in_conflict = False
                conflict_lines = []
            elif line.startswith("<<<<<<<"):
                in_conflict = True
            elif line.startswith(">>>>>>>"):
                in_conflict = False
                if current_file and conflict_lines:
                    conflict = self._parse_conflict_block(
                        current_file, conflict_lines, source_branch
                    )
                    if conflict:
                        conflicts.append(conflict)
                    conflict_lines = []
                in_conflict = False
            elif in_conflict:
                conflict_lines.append(line)

        # Handle last conflict if any
        if current_file and conflict_lines:
            conflict = self._parse_conflict_block(
                current_file, conflict_lines, source_branch
            )
            if conflict:
                conflicts.append(conflict)

        return conflicts

    def _parse_conflict_block(
        self, file_path: str, conflict_lines: List[str], source_branch: str
    ) -> Conflict:
        """
        Parse a single conflict block into a Conflict object.
        """
        # Determine conflict type based on content
        content = "\n".join(conflict_lines)

        # Simple heuristic: check for merge markers
        if "<<<<<<<" in content and ">>>>>>>" in content:
            conflict_type = ConflictTypeExtended.CONTENT
        else:
            conflict_type = ConflictTypeExtended.MERGE

        # Estimate severity based on file type and conflict size
        severity = RiskLevel.MEDIUM
        if file_path.endswith(".py"):
            severity = RiskLevel.HIGH
        elif file_path.endswith((".js", ".ts", ".jsx", ".tsx")):
            severity = RiskLevel.HIGH

        # Create conflict block
        block = ConflictBlock(
            start_line=0,  # Would need more parsing for exact line numbers
            end_line=len(conflict_lines),
            conflict_type=conflict_type,
            content_before=[],  # Would need more parsing
            content_after=[],
            content_common=[],
        )

        return Conflict(
            file_path=file_path,
            conflict_blocks=[block],
            conflict_type=conflict_type,
            severity=severity,
            description=f"Conflict detected in {file_path} from {source_branch}",
            resolution_strategy="manual_review",
            affected_components=[file_path],
            estimated_resolution_time=30,
        )
