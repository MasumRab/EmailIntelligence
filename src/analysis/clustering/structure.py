"""Codebase-structure metrics for branch clustering (task 002.2).

Four normalized metrics in ``[0, 1]`` describing *where* a branch touches the
tree, independent of how many lines it moves:

``directory_similarity`` Jaccard similarity between main's and the branch's
                         directory sets
``file_additions``       1 - new_files / files_in_branch
``core_module_stability`` 1.0 untouched, penalised per five core modifications,
                         0.5 if any core file is deleted
``namespace_isolation``  share of new files landing in the branch's single
                         busiest directory (scattered files score low)

Weights sum to 1.0 (see :data:`WEIGHTS`).
"""

from __future__ import annotations

import math
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import PurePosixPath
from typing import Any

from ._repo import resolve_rev

WEIGHTS = {
    "directory_similarity": 0.30,
    "file_additions": 0.25,
    "core_module_stability": 0.25,
    "namespace_isolation": 0.20,
}

# A "core module" for the stability metric: paths that every import path and
# configuration lookup runs through.
CORE_PREFIXES = ("core/", "src/core/", "config/", "settings/")
CORE_FILENAMES = ("main.py", "__init__.py")

CORE_DELETION_SCORE = 0.5
CORE_MODIFICATION_PENALTY = 0.1
CORE_PENALTY_GROUP = 5


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _parent_dirs(paths: set[str]) -> set[str]:
    return {str(PurePosixPath(p).parent) for p in paths if "/" in p}


def _is_core(path: str) -> bool:
    return path.startswith(CORE_PREFIXES) or PurePosixPath(path).name in CORE_FILENAMES


class CodebaseStructureAnalyzer:
    """Score the shape of a branch's change set relative to main."""

    def __init__(self, repo_path: str, main_branch: str = "main"):
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

    def _file_tree(self, ref: str) -> set[str]:
        return {
            line
            for line in self._run_git("ls-tree", "-r", "--name-only", ref).splitlines()
            if line
        }

    def changed_files(self, branch: str) -> list[str]:
        """Return the files that differ between ``main_branch`` and ``branch``."""
        branch_rev = resolve_rev(self.repo_path, branch)
        main_rev = resolve_rev(self.repo_path, self.main_branch)
        result = subprocess.run(
            [
                "git",
                "-C",
                self.repo_path,
                "diff",
                "--name-only",
                f"{main_rev}...{branch_rev}",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ValueError(f"cannot diff {branch}: {result.stderr.strip()}")
        return [line for line in result.stdout.splitlines() if line.strip()]

    def _changes(self, branch_rev: str, main_rev: str) -> dict[str, list[str]]:
        out = {}
        for label, filt in (("added", "A"), ("modified", "M"), ("deleted", "D")):
            text = self._run_git(
                "diff",
                f"--diff-filter={filt}",
                "--name-only",
                f"{main_rev}...{branch_rev}",
            )
            out[label] = [line for line in text.splitlines() if line.strip()]
        return out

    # ------------------------------------------------------------- metrics

    @staticmethod
    def _directory_similarity(main_dirs: set[str], branch_dirs: set[str]) -> float:
        if not main_dirs and not branch_dirs:
            return 1.0
        union = main_dirs | branch_dirs
        return len(main_dirs & branch_dirs) / len(union) if union else 1.0

    @staticmethod
    def _file_additions(new_files: int, files_in_branch: int) -> float:
        if files_in_branch == 0:
            return 1.0
        return _clamp(1.0 - new_files / files_in_branch)

    @staticmethod
    def _core_module_stability(changes: dict[str, list[str]]) -> float:
        deleted_core = [f for f in changes["deleted"] if _is_core(f)]
        if deleted_core:
            return CORE_DELETION_SCORE
        modified_core = [f for f in changes["modified"] if _is_core(f)]
        if modified_core:
            groups = math.ceil(len(modified_core) / CORE_PENALTY_GROUP)
            return _clamp(1.0 - CORE_MODIFICATION_PENALTY * groups)
        return 1.0

    @staticmethod
    def _namespace_isolation(added: list[str]) -> float:
        """Share of new files in the busiest new-file directory.

        One new file in one directory scores 1.0; new files scattered across a
        dozen directories score low. No new files means nothing to isolate.
        """
        if not added:
            return 1.0
        counts = Counter(str(PurePosixPath(f).parent) for f in added)
        return _clamp(max(counts.values()) / len(added))

    # ---------------------------------------------------------------- entry

    def analyze(self, branch_name: str) -> dict[str, Any]:
        """Return the structure metric block for ``branch_name``."""
        branch_rev = resolve_rev(self.repo_path, branch_name)
        main_rev = resolve_rev(self.repo_path, self.main_branch)

        main_files = self._file_tree(main_rev)
        branch_files = self._file_tree(branch_rev)
        changes = self._changes(branch_rev, main_rev)

        changed = (
            set(changes["added"]) | set(changes["modified"]) | set(changes["deleted"])
        )
        if not changed:
            # Nothing differs from main: no structural signal either way.
            metrics = dict.fromkeys(WEIGHTS, 0.0)
            aggregate = 0.0
        else:
            main_dirs = _parent_dirs(main_files)
            branch_dirs = _parent_dirs(branch_files)
            metrics = {
                "directory_similarity": round(
                    self._directory_similarity(main_dirs, branch_dirs), 4
                ),
                "file_additions": round(
                    self._file_additions(len(changes["added"]), len(branch_files)), 4
                ),
                "core_module_stability": round(self._core_module_stability(changes), 4),
                "namespace_isolation": round(
                    self._namespace_isolation(changes["added"]), 4
                ),
            }
            aggregate = round(sum(metrics[k] * w for k, w in WEIGHTS.items()), 4)

        return {
            "branch_name": branch_name,
            "metrics": metrics,
            "aggregate_score": aggregate,
            "directory_count": len(_parent_dirs(branch_files)),
            "file_count": len(branch_files),
            "new_files": len(changes["added"]),
            "modified_files": len(changes["modified"]),
            "deleted_files": len(changes["deleted"]),
            "changed_files": len(changed),
            "analysis_timestamp": datetime.now(UTC).isoformat(),
        }
