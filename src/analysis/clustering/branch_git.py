"""Full per-branch git profile (task 002, stage 1b).

The three stage-one analyzers reduce a branch to three numbers. That is enough
to rank branches by integration cost, but not enough to say two branches are
*about the same thing*: two branches with identical scores can touch entirely
disjoint parts of the tree. This module keeps the raw git facts so the content
stage can cluster on what a branch actually changes.

One branch costs two git invocations:

``git log --numstat``   commits on ``main..branch`` with author, date, subject
                        and the per-file line counts of every commit
``merge-base``          the fork point, used to bound the diff

Nothing here interprets the data; interpretation happens in :mod:`.content`.
"""

from __future__ import annotations

import subprocess
from collections import Counter
from datetime import UTC, datetime
from typing import Any

from ._repo import resolve_rev

COMMIT_LIMIT = 500
_RS = "\x1e"  # record separator between commits
_FS = "\x1f"  # field separator inside a commit header


def _run(repo_path: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", repo_path, *args],
        capture_output=True,
        text=True,
        check=False,
    )


def merge_base(repo_path: str, main_rev: str, branch_rev: str) -> str:
    """Return the fork point, or raise ValueError when there is none."""
    result = _run(repo_path, "merge-base", main_rev, branch_rev)
    if result.returncode != 0 or not result.stdout.strip():
        raise ValueError(f"no merge base between {main_rev} and {branch_rev}")
    return result.stdout.strip()


def _parse_log(stdout: str) -> list[dict[str, Any]]:
    commits: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    # ``str.splitlines`` treats \x1e as a line break, which would split the
    # record separator out of every header. Only ``\n`` ends a real line here.
    for line in stdout.split("\n"):
        if line.startswith(_RS):
            if current is not None:
                commits.append(current)
            sha, author, date, subject = line[1:].split(_FS, 3)
            current = {
                "sha": sha,
                "author": author,
                "date": date,
                "subject": subject,
                "files": [],
                "added": 0,
                "deleted": 0,
            }
            continue
        if current is None or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, deleted, path = parts
        # Binary files report "-" for both counts; they still count as touched.
        added_n = 0 if added == "-" else int(added)
        deleted_n = 0 if deleted == "-" else int(deleted)
        current["added"] += added_n
        current["deleted"] += deleted_n
        current["files"].append({"path": path, "added": added_n, "deleted": deleted_n})
    if current is not None:
        commits.append(current)
    return commits


def _top_directory(path: str) -> str:
    parts = path.split("/")
    return parts[0] if len(parts) > 1 else "."


class BranchGitProfiler:
    """Collect the raw git history of a branch against its integration base."""

    def __init__(self, repo_path: str, main_branch: str = "main"):
        self.repo_path = repo_path
        self.main_branch = main_branch

    def profile(
        self, branch_name: str, commit_limit: int = COMMIT_LIMIT
    ) -> dict[str, Any]:
        main_rev = resolve_rev(self.repo_path, self.main_branch)
        branch_rev = resolve_rev(self.repo_path, branch_name)
        base = merge_base(self.repo_path, main_rev, branch_rev)

        log = _run(
            self.repo_path,
            "log",
            "--no-merges",
            f"--max-count={commit_limit}",
            "--numstat",
            f"--format={_RS}%H{_FS}%an{_FS}%aI{_FS}%s",
            f"{main_rev}..{branch_rev}",
        )
        if log.returncode != 0:
            raise ValueError(f"git log failed for {branch_name}: {log.stderr.strip()}")

        commits = _parse_log(log.stdout)

        file_stats: dict[str, dict[str, int]] = {}
        for commit in commits:
            for entry in commit["files"]:
                stats = file_stats.setdefault(
                    entry["path"], {"added": 0, "deleted": 0, "touches": 0}
                )
                stats["added"] += entry["added"]
                stats["deleted"] += entry["deleted"]
                stats["touches"] += 1

        authors = Counter(commit["author"] for commit in commits)
        dates = sorted(commit["date"] for commit in commits)
        directories = Counter(_top_directory(path) for path in file_stats)

        return {
            "branch_name": branch_name,
            "main_rev": main_rev,
            "branch_rev": branch_rev,
            "merge_base": base,
            "commit_count": len(commits),
            "commits": commits,
            "authors": dict(authors),
            "first_commit": dates[0] if dates else None,
            "last_commit": dates[-1] if dates else None,
            "files": file_stats,
            "top_directories": dict(directories.most_common(10)),
            "total_added": sum(c["added"] for c in commits),
            "total_deleted": sum(c["deleted"] for c in commits),
            "profiled_at": datetime.now(UTC).isoformat(),
        }
