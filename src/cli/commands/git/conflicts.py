"""Compatibility shim for :mod:`src.git.conflicts`.

This file was a byte-for-byte copy of ``src/git/conflicts.py`` (195 lines
each). The canonical implementation lives in ``src.git.conflicts``; this path
re-exports it so an import of the CLI location keeps working.
"""

from ....git.conflicts import ConflictsCommand  # noqa: F401

__all__ = ["ConflictsCommand"]
