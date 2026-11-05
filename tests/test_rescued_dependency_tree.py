"""The dependency tree rescued from #325 must actually import.

``emailintelligence_cli.py`` — the repository's shipped root entry point — imports
``src.git.conflict_detector``, ``src.core.conflict_models``,
``src.analysis.constitutional.analyzer`` and ``src.validation.validator``. None of
those modules existed on ``main``, so the CLI was import-dead. The rescue branch
brings them back from #325, and these tests pin the property that makes the rescue
worth taking: the modules import, and the two exception classes their callers
construct are defined.

The rescue also brought the ``src/git`` package, whose modules raise
``GitOperationError`` and ``ConflictDetectionError``. Both names appear in #325 only
as a code snippet in ``INTEGRATION_DECISIONS.md`` — never in a ``.py`` file — so
without a definition in ``src.core.exceptions`` the whole package is unimportable.

Seven rescued modules import ``structlog``, which no manifest declared. That cannot
be asserted by importing in a test, because whether it is installed depends on the
environment the test runs in; it is asserted against the manifests instead.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pytest

from src.core.exceptions import BaseAppException, ConflictDetectionError, GitOperationError

REPO_ROOT = Path(__file__).resolve().parents[1]

CLI_IMPORTS = [
    "src.core.conflict_models",
    "src.analysis.constitutional.analyzer",
    "src.validation.validator",
    "src.resolution.auto_resolver",
    "src.resolution.semantic_merger",
    "src.strategy.generator",
    "src.strategy.risk_assessor",
]

GIT_PACKAGE = [
    "src.git",
    "src.git.conflict_detector",
    "src.git.history",
    "src.git.merger",
    "src.git.reordering",
    "src.git.repository",
    "src.git.worktree",
]

STRUCTLOG_CONSUMERS = [
    "src.analysis.dependency",
    "src.utils.caching",
    "src.utils.monitoring",
    "src.utils.rate_limit",
    "src.strategy.multi_phase_generator",
]


def test_the_shipped_cli_imports() -> None:
    """``emailintelligence_cli`` is the root entry point; it must be importable."""
    importlib.import_module("emailintelligence_cli")


@pytest.mark.parametrize("module", CLI_IMPORTS)
def test_every_module_the_cli_imports_resolves(module: str) -> None:
    importlib.import_module(module)


@pytest.mark.parametrize("module", GIT_PACKAGE)
def test_the_rescued_git_package_imports(module: str) -> None:
    """Importing any ``src.git`` module goes through ``__init__``, so all of them fail together."""
    importlib.import_module(module)


def test_the_exceptions_the_git_package_raises_are_defined() -> None:
    """Both are constructed with a single message, never a ``(status_code, detail)`` pair."""
    for exc in (GitOperationError, ConflictDetectionError):
        assert issubclass(exc, BaseAppException)
        raised = exc("boom")
        assert raised.detail == "boom"
        assert str(raised) == "boom"


@pytest.mark.parametrize("consumer", STRUCTLOG_CONSUMERS)
def test_every_structlog_consumer_imports(consumer: str) -> None:
    """Import-or-skip: the dependency is declared below, so a missing install is an env fault.

    Skipped rather than passed, so the skip shows up in the run summary instead of
    being read as coverage.
    """
    pytest.importorskip("structlog", reason="structlog is declared in requirements; install it to run this")
    importlib.import_module(consumer)


def _declares_structlog(path: Path) -> bool:
    if not path.exists():
        return False
    return re.search(r'^\s*"?structlog', path.read_text(), re.MULTILINE) is not None


@pytest.mark.parametrize("manifest", ["setup/requirements.txt", "pyproject.toml"])
def test_structlog_is_declared_where_the_project_lists_its_dependencies(manifest: str) -> None:
    """Nothing declared it, so every module importing it was import-dead on a clean install."""
    assert _declares_structlog(REPO_ROOT / manifest), f"{manifest} does not declare structlog"
