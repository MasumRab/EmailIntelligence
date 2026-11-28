"""Compatibility shim for :mod:`src.git.history`.

This module was a near-copy of ``src/git/history.py`` (114 of 141 lines, 63.4%
duplicated according to SonarCloud). The copies had already drifted: this one
lacked ``timestamp_to_dt`` and ``analyze_history``, and its ``_classify``
returned a different category/risk pair for the same message.

The canonical implementation is ``src.git.history``; this path re-exports it.
Nothing outside ``src.analysis.commits`` imports this module, so the richer
classification is adopted without changing a reachable caller.
"""

from ...git.history import (  # noqa: F401
    Commit,
    CommitClassifier,
    GitHistory,
    timestamp_to_dt,
)

__all__ = [
    "Commit",
    "CommitClassifier",
    "GitHistory",
    "timestamp_to_dt",
]
