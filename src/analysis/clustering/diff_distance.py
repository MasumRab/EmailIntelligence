"""Diff-distance metrics for branch clustering (task 002.3).

Four normalized metrics in ``[0, 1]`` computed from ``git diff --numstat``
between ``main_branch`` and a branch. All four are *inverted* so that a higher
score means a cheaper, safer integration:

``code_churn``          1 - total_change / 5000 (saturating)
``change_concentration``1 - files_affected / 50 (saturating)
``diff_complexity``     min(largest / average / 3, 1)
``integration_risk``    1 - weighted risk per affected file

Weights sum to 1.0 (see :data:`WEIGHTS`).
"""

from __future__ import annotations

import fnmatch
import subprocess
from datetime import UTC, datetime
from typing import Any

from ._repo import resolve_rev

WEIGHTS = {
    "code_churn": 0.30,
    "change_concentration": 0.25,
    "diff_complexity": 0.25,
    "integration_risk": 0.20,
}

ESTIMATED_CODEBASE_SIZE = 5000
MAX_EXPECTED_FILES = 50

RISK_WEIGHTS = {"critical": 0.8, "high": 0.5, "medium": 0.2, "low": 0.05}

RISKY_FILE_PATTERNS = {
    "critical": [
        "config/",
        "settings/",
        ".env",
        "secrets",
        "core/",
        "main.py",
        "__init__.py",
    ],
    "high": [
        "tests/",
        "test_*.py",
        "*_test.py",
        "setup.py",
        "requirements.txt",
        "pyproject.toml",
    ],
    "medium": [
        "src/",
        "lib/",
        "utils/",
    ],
    "low": [
        "docs/",
        "README",
        "examples/",
    ],
}

# Most-specific category wins for a file that matches more than one list.
_PRECEDENCE = ("critical", "high", "medium", "low")


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


class DiffDistanceCalculator:
    """Measure how far a branch's diff is from main, in integration terms."""

    def __init__(self, repo_path: str, main_branch: str = "main"):
        probe = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=False,
        )
        if probe.returncode != 0:
            raise ValueError(f"Not a git repository: {repo_path}")
        self.repo_path = repo_path
        self.main_branch = main_branch

    def _run_git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", self.repo_path, *args],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout

    def _parse_numstat(self, branch_name: str) -> list[dict[str, Any]]:
        output = self._run_git(
            "diff",
            "--numstat",
            f"{resolve_rev(self.repo_path, self.main_branch)}..."
            f"{resolve_rev(self.repo_path, branch_name)}",
        )
        results = []
        for line in output.splitlines():
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            added, deleted, filepath = parts
            if added == "-" or deleted == "-":
                # Binary file: no line counts, but it is still an affected file.
                results.append(
                    {"added": 0, "deleted": 0, "filepath": filepath, "binary": True}
                )
                continue
            results.append(
                {
                    "added": int(added),
                    "deleted": int(deleted),
                    "filepath": filepath,
                    "binary": False,
                }
            )
        return results

    def _classify_risk(self, filepath: str) -> str:
        for category in _PRECEDENCE:
            for pattern in RISKY_FILE_PATTERNS[category]:
                if pattern.endswith("/") and filepath.startswith(pattern):
                    return category
                if fnmatch.fnmatch(filepath, pattern) or filepath == pattern:
                    return category
        return "low"

    def analyze(self, branch_name: str) -> dict[str, Any]:
        """Return the metric block for ``branch_name``."""
        entries = self._parse_numstat(branch_name)

        total_added = sum(e["added"] for e in entries)
        total_deleted = sum(e["deleted"] for e in entries)
        total_changed = total_added + total_deleted
        files_affected = len(entries)

        if files_affected == 0:
            metrics = dict.fromkeys(WEIGHTS, 0.0)
            largest = 0
        else:
            churn_ratio = total_changed / ESTIMATED_CODEBASE_SIZE
            code_churn = max(0.0, 1.0 - min(churn_ratio, 1.0))

            concentration = min(files_affected / MAX_EXPECTED_FILES, 1.0)
            change_concentration = 1.0 - concentration

            per_file = [e["added"] + e["deleted"] for e in entries]
            largest = max(per_file)
            avg = total_changed / files_affected
            # A one-file diff has no concentration ratio to speak of; treat it
            # as maximally concentrated only if it is large, otherwise 0.
            complexity = min((largest / avg) / 3.0, 1.0) if avg > 0 else 0.0

            risk_score = sum(
                RISK_WEIGHTS[self._classify_risk(e["filepath"])] for e in entries
            )
            integration_risk = _clamp(1.0 - risk_score / files_affected)

            metrics = {
                "code_churn": round(_clamp(code_churn), 4),
                "change_concentration": round(_clamp(change_concentration), 4),
                "diff_complexity": round(_clamp(complexity), 4),
                "integration_risk": round(integration_risk, 4),
            }

        aggregate = round(sum(metrics[k] * w for k, w in WEIGHTS.items()), 4)

        return {
            "branch_name": branch_name,
            "metrics": metrics,
            "aggregate_score": aggregate,
            "total_lines_added": total_added,
            "total_lines_deleted": total_deleted,
            "total_lines_changed": total_changed,
            "files_affected": files_affected,
            "largest_file_change": largest,
            "analysis_timestamp": datetime.now(UTC).isoformat(),
        }
