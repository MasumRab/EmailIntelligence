"""Shared committish resolution for the clustering analyzers.

The analyzers are handed branch *names* (``aligned-pr-471``), but a read-only
mirror often holds them only as ``refs/remotes/origin/*``. Resolving once here
keeps every analyzer from silently reading an unresolvable name as "no work".
"""

from __future__ import annotations

import subprocess
from collections.abc import Iterable

_CANDIDATE_FORMS = (
    "{name}",
    "refs/remotes/origin/{name}",
    "origin/{name}",
    "refs/heads/{name}",
)


def resolve_rev(repo_path: str, name: str) -> str:
    """Return a committish for ``name`` or raise ``ValueError``.

    Ambiguous names are not special-cased: the first form that resolves wins,
    which for a name present both locally and on origin is the local one.
    """
    for template in _CANDIDATE_FORMS:
        candidate = template.format(name=name)
        result = subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "rev-parse",
                "--verify",
                "--quiet",
                f"{candidate}^{{commit}}",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return candidate
    raise ValueError(f"cannot resolve {name!r} to a commit in {repo_path}")


def resolve_all(repo_path: str, names: Iterable[str]) -> tuple[list[str], list[str]]:
    """Split ``names`` into (resolvable, unresolvable)."""
    ok, bad = [], []
    for name in names:
        try:
            resolve_rev(repo_path, name)
        except ValueError:
            bad.append(name)
        else:
            ok.append(name)
    return ok, bad
