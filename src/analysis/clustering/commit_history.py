"""Commit-history metrics for branch clustering (task 002.1).

Five normalized metrics in ``[0, 1]`` per branch, plus the aggregate score the
clusterer consumes. Only commits unique to the branch (``main..branch``) are
measured, so the numbers describe the branch rather than the shared mainline.

``commit_recency``      exponential decay of the newest commit (30-day half-life)
``commit_frequency``    commits per active day, saturating at two per day
``authorship_diversity``unique authors, saturating at five
``merge_readiness``     1 / (1 + commits behind main / 50)
``stability_score``     1 - coefficient of variation of commit intervals

Weights sum to 1.0 (see :data:`WEIGHTS`).
"""

from __future__ import annotations

import asyncio
import itertools
import math
import subprocess
from datetime import UTC, datetime
from typing import Any

from ...git.history import Commit, GitHistory
from ._repo import resolve_rev

WEIGHTS = {
    "commit_recency": 0.25,
    "commit_frequency": 0.20,
    "authorship_diversity": 0.15,
    "merge_readiness": 0.25,
    "stability_score": 0.15,
}

RECENCY_TAU_DAYS = 30.0
FREQUENCY_SATURATION = 2.0
AUTHOR_SATURATION = 5.0
BEHIND_SCALE = 50.0


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _git(repo_path: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", repo_path, *args],
        capture_output=True,
        text=True,
        check=False,
    )


class CommitHistoryAnalyzer:
    """Extract and score commit-history metrics for one branch."""

    def __init__(
        self, repo_path: str, main_branch: str = "main", commit_limit: int = 200
    ):
        self.repo_path = repo_path
        self.main_branch = main_branch
        self.commit_limit = commit_limit

    def commits_behind(self, branch: str) -> int:
        """Return how many commits ``main_branch`` has that ``branch`` lacks."""
        result = _git(
            self.repo_path,
            "rev-list",
            "--count",
            f"{resolve_rev(self.repo_path, branch)}.."
            f"{resolve_rev(self.repo_path, self.main_branch)}",
        )
        if result.returncode != 0:
            raise ValueError(f"cannot compare {branch}: {result.stderr.strip()}")
        return int(result.stdout.strip() or 0)

    def analyze_sync(self, branch_name: str) -> dict[str, Any]:
        """Synchronous wrapper around :meth:`analyze` for non-async callers.

        Raises:
            RuntimeError: if called from inside a running event loop, where
                ``asyncio.run`` cannot be used. Pass precomputed analyzer
                output instead in that case.
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.analyze(branch_name))
        raise RuntimeError(
            "analyze_sync() cannot run inside an active event loop; "
            "await analyze() or pass precomputed analyzer output"
        )

    async def analyze(self, branch_name: str) -> dict[str, Any]:
        """Return the metric block for ``branch_name``.

        Only commits unique to the branch (``main..branch``) are measured. Using
        the branch's whole reachable history would describe the shared mainline
        instead: every branch would report the same author count and the same
        tip recency.
        """
        branch_rev = resolve_rev(self.repo_path, branch_name)
        main_rev = resolve_rev(self.repo_path, self.main_branch)
        history = GitHistory(self.repo_path)
        commits: list[Commit] = await history.get_commits(
            f"{main_rev}..{branch_rev}", limit=self.commit_limit
        )

        behind = self.commits_behind(branch_name)
        now = datetime.now(UTC)

        if not commits:
            return {
                "branch_name": branch_name,
                "metrics": {key: 0.0 for key in WEIGHTS},
                "aggregate_score": 0.0,
                "commit_count": 0,
                "commits_behind_main": behind,
                "days_active": 0.0,
                "unique_authors": 0,
                "no_unique_commits": True,
                "analysis_timestamp": now.isoformat(),
            }

        stamps = sorted(c.timestamp for c in commits if c.timestamp)
        latest = max(stamps) if stamps else 0
        earliest = min(stamps) if stamps else 0

        days_since_latest = (
            max(0.0, (now.timestamp() - latest) / 86400.0) if latest else 365.0
        )
        recency = _clamp(math.exp(-days_since_latest / RECENCY_TAU_DAYS))

        days_active = max(1.0, (latest - earliest) / 86400.0) if latest else 1.0
        per_day = len(commits) / days_active
        frequency = _clamp(per_day / FREQUENCY_SATURATION)

        authors = {
            (c.author or "").strip() for c in commits if (c.author or "").strip()
        }
        diversity = _clamp(len(authors) / AUTHOR_SATURATION)

        readiness = _clamp(1.0 / (1.0 + behind / BEHIND_SCALE))

        ordered = sorted(stamps)
        gaps = [b - a for a, b in itertools.pairwise(ordered) if b >= a]
        if len(gaps) >= 2:
            mean_gap = sum(gaps) / len(gaps)
            if mean_gap > 0:
                var = sum((g - mean_gap) ** 2 for g in gaps) / len(gaps)
                stability = _clamp(1.0 - math.sqrt(var) / mean_gap)
            else:
                stability = 1.0
        else:
            stability = 0.5

        metrics = {
            "commit_recency": round(recency, 4),
            "commit_frequency": round(frequency, 4),
            "authorship_diversity": round(diversity, 4),
            "merge_readiness": round(readiness, 4),
            "stability_score": round(stability, 4),
        }
        aggregate = round(sum(metrics[k] * w for k, w in WEIGHTS.items()), 4)

        return {
            "branch_name": branch_name,
            "metrics": metrics,
            "aggregate_score": aggregate,
            "commit_count": len(commits),
            "commits_behind_main": behind,
            "days_active": round(days_active, 2),
            "unique_authors": len(authors),
            "analysis_timestamp": now.isoformat(),
        }
