"""Regression tests: project-root constants must resolve to the repository root.

``src/backend/python_nlp/`` modules were moved out of ``backend/python_nlp/``,
and their project roots were derived by counting ``os.path.dirname`` levels
from ``__file__``.  Every constant silently shifted down one level, so they
resolved under ``src/`` instead of the repository root.  ``data/`` is
gitignored and absent from a fresh checkout, which made the production API app
(``src/backend/python_backend/main.py``) unimportable.

These tests assert on observable values and behaviour only.  The pre-fix tree
fails them; a test that passes on both trees would prove nothing.
"""

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import src.backend.python_nlp.gmail_integration as gmail_integration
import src.backend.python_nlp.smart_filters as smart_filters
import src.backend.python_nlp.smart_retrieval as smart_retrieval

# The worktree this file lives in.  Every asserted path must resolve here: if a
# module was imported from the operator clone, grading would be meaningless.
WORKTREE_ROOT = Path(__file__).resolve().parent.parent


def _relative_parts(path):
    return Path(path).resolve().relative_to(WORKTREE_ROOT).parts


def test_modules_under_test_come_from_this_worktree():
    """Guard: the run must not silently grade another checkout."""
    assert (WORKTREE_ROOT / "pyproject.toml").is_file()
    for module in (smart_filters, smart_retrieval, gmail_integration):
        module_file = module.__file__
        assert module_file is not None, module.__name__
        module_path = Path(module_file).resolve()
        assert module_path.is_relative_to(WORKTREE_ROOT), module_path


def test_data_dir_is_repository_root_data():
    """``DATA_DIR`` is ``<repo_root>/data``, not ``<repo_root>/src/data``."""
    assert Path(smart_filters.DATA_DIR) == WORKTREE_ROOT / "data"
    assert "src" not in _relative_parts(smart_filters.DATA_DIR)
    assert Path(smart_filters.DEFAULT_DB_PATH) == WORKTREE_ROOT / "data" / "smart_filters.db"


def test_checkpoint_db_path_is_not_under_src():
    """The checkpoint database lives at the repo root, not inside ``src/``."""
    parent = Path(smart_retrieval.DEFAULT_CHECKPOINT_DB_PATH).parent
    assert parent == WORKTREE_ROOT
    assert "src" not in _relative_parts(parent)


def test_email_cache_path_parent_is_repository_root():
    """The cache is ``<repo_root>/email_cache.db``, not ``<repo_root>/src/backend/...``."""
    parent = Path(gmail_integration.DEFAULT_CACHE_PATH).parent
    assert parent == WORKTREE_ROOT
    assert "src" not in _relative_parts(parent)


def test_smart_filter_manager_creates_missing_data_dir():
    """Constructing the manager in a tree without ``data/`` must still work."""
    from src.backend.python_nlp.smart_filters import SmartFilterManager

    data_dir = WORKTREE_ROOT / "data"
    db_file = Path(smart_filters.DEFAULT_DB_PATH)
    created_dir = not data_dir.exists()
    manager = None
    try:
        manager = SmartFilterManager()
        assert db_file.is_file(), f"{db_file} was not created"
        assert db_file.stat().st_size > 0
        conn = sqlite3.connect(db_file)
        try:
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        finally:
            conn.close()
        assert "email_filters" in tables
    finally:
        if manager is not None:
            manager.close()
        if created_dir:
            shutil.rmtree(data_dir, ignore_errors=True)


def test_python_backend_main_imports():
    """Regression: the production API app must import on a clean checkout.

    ``src/backend/python_backend/main.py`` also calls ``uvicorn.run(...)`` at
    module level (a server start, unrelated to path resolution), so the child
    process stubs ``uvicorn.run`` out.  Everything else -- every import, the
    module-level ``SmartFilterManager()``, and app/route construction -- runs
    for real; reaching ``app`` proves the import completed.
    """
    code = (
        "import uvicorn\n"
        "uvicorn.run = lambda *args, **kwargs: None\n"
        "import src.backend.python_backend.main as main\n"
        "assert hasattr(main, 'app')\n"
        "print(main.__file__, flush=True)\n"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(WORKTREE_ROOT / "src")
    env["SECRET_KEY"] = "test-secret-key"
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(WORKTREE_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, (
        "import src.backend.python_backend.main failed:\n" + result.stderr[-4000:]
    )
    imported_from = Path(result.stdout.strip().splitlines()[-1]).resolve()
    assert imported_from.is_relative_to(WORKTREE_ROOT), imported_from
