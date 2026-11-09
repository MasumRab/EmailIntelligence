"""
Git history analysis services for EmailIntelligence CLI

Provides the commit history retrieval and classification primitives that
commands like `plan-rebase` and `analyze-history` depend on.
"""

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

CATEGORY_ORDER = ["feat", "fix", "chore", "build", "ci", "docs", "style"]


@dataclass
class Commit:
    """A single commit summarized for analysis and rebase planning."""

    hash: str
    message: str
    author: str = ""
    timestamp: int = 0
    category: str = "other"
    risk_level: str = "low"
    subject: str = ""


class GitHistory:
    """Retrieves commits from a git repository via git log."""

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = repo_path

    async def get_commits(self, branch: str = "HEAD", limit: int = 500) -> List[Commit]:
        """Return up to ``limit`` commits reachable from ``branch``."""
        try:
            cwd = self.repo_path or "."
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    cwd,
                    "log",
                    "-n",
                    str(limit),
                    "--format=%H|%an|%ct|%s",
                    branch,
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 or not result.stdout.strip():
                return []
        except Exception:
            return []

        commits = []
        for line in result.stdout.splitlines():
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            oid, author, timestamp, subject = parts[0], parts[1], parts[2], parts[3]
            message = subject
            try:
                ts = int(timestamp) or 0
            except ValueError:
                ts = 0
            commits.append(
                Commit(
                    hash=oid,
                    message=message,
                    author=author,
                    timestamp=ts,
                    subject=subject,
                )
            )
        return commits


class CommitClassifier:
    """Classifies commits into categories and risk levels for planning."""

    _COMMIT_TYPE_RE = re.compile(
        r"^(fix|feat|chore|build|ci|docs|style|refactor|perf|test|revert)(?:\(|:|\s)"
    )

    def classify(self, commit: Commit) -> Commit:
        """Assign ``category`` and ``risk_level`` to a commit in place."""
        category, risk = self._classify(commit.message, commit.subject)
        commit.category = category
        commit.risk_level = risk
        return commit

    def _classify(self, message: str, subject: str = "") -> tuple:
        """Return ``(category, risk_level)`` for a commit message."""
        # Determine category from conventional commit prefix
        match = self._COMMIT_TYPE_RE.match(message)
        if match:
            category = match.group(1)
        else:
            category = "other"

        # Determine risk level based on category and content
        risk_keywords = ["fix", "security", "vuln", "exploit", "crash", "leak", "auth"]
        if any(kw in message.lower() for k in risk_keywords):
            risk = "high"
        elif category in ("feat", "refactor"):
            risk = "medium"
        else:
            risk = "low"

        return category, risk
