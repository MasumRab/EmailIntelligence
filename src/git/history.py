"""
Git history analysis services for EmailIntelligence CLI

Provides the commit history retrieval and classification primitives that
commands like `plan-rebase` and `analyze-history` depend on. These classes
were declared as dependencies (``GitHistory``, ``CommitClassifier``) but
never implemented, which made the injected dependencies resolve to ``None``
and silently degraded (or crashed) every git-analysis command.
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
            # Use plumbing that works regardless of the DI repository wrapper.
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
        text = (message or subject or "").strip().lower()
        m = self._COMMIT_TYPE_RE.match(text)
        if m:
            category = m.group(1)
            if category not in CATEGORY_ORDER:
                category = "other"
        else:
            category = "other"

        risk = "low"
        if any(k in text for k in ("security", "auth", "token", "cve", "password")):
            risk = "critical"
        elif any(
            k in text
            for k in ("database", "migrat", "schema", "breaking", "refactor")
        ):
            risk = "high"
        elif category in ("fix", "perf"):
            risk = "medium"
        return category, risk

    def analyze_history(self, commits: List[Commit]) -> Dict[str, Any]:
        """Summarize a commit list by category and risk."""
        by_category: Dict[str, int] = {}
        by_risk: Dict[str, int] = {}
        for commit in commits:
            self.classify(commit)
            by_category[commit.category] = by_category.get(commit.category, 0) + 1
            by_risk[commit.risk_level] = by_risk.get(commit.risk_level, 0) + 1
        return {
            "total": len(commits),
            "by_category": dict(sorted(by_category.items())),
            "by_risk": dict(sorted(by_risk.items())),
        }


def timestamp_to_dt(ts: int) -> datetime:
    """Convert a unix timestamp to an aware datetime (fallback 0)."""
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except (ValueError, OverflowError, OSError):
        return datetime(1970, 1, 1, tzinfo=timezone.utc)