"""Compatibility shim for :mod:`src.git.branch_health`.

This file was a byte-for-byte copy of ``src/git/branch_health.py`` (228 lines
each). The canonical implementation lives in ``src.git.branch_health``; this
path re-exports it so an import of the CLI location keeps working.
"""

from ....git.branch_health import BranchHealthCommand  # noqa: F401

__all__ = ["BranchHealthCommand"]
