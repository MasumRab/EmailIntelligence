"""``EmailCache`` must create its database's parent directory.

``PathValidator.validate_and_resolve_db_path`` validates and resolves a path but
deliberately creates nothing, so ``sqlite3.connect`` on a path whose parent
directory does not exist raises ``OperationalError: unable to open database
file``. ``EmailCache`` takes the cache path as a constructor argument, so a
deployment that points it at a fresh directory — a clean container, a new
volume mount — fails while constructing the collector, before a single email is
fetched.

Both sibling PRs (#493 and #527) carry the same six-line fix for this; these
tests pin the behaviour rather than the implementation.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.backend.python_nlp.gmail_integration import EmailCache


def test_a_missing_parent_directory_is_created(tmp_path: Path) -> None:
    """The first run against a fresh directory must succeed, not raise."""
    target = tmp_path / "nested" / "deeper" / "email_cache.db"
    assert not target.parent.exists()

    cache = EmailCache(str(target))
    try:
        assert target.parent.is_dir()
        assert target.exists()
    finally:
        cache.conn.close()


def test_an_existing_directory_still_works(tmp_path: Path) -> None:
    """Creating the directory must not disturb the ordinary path."""
    target = tmp_path / "email_cache.db"

    cache = EmailCache(str(target))
    try:
        assert target.exists()
    finally:
        cache.conn.close()


def test_the_cache_is_usable_after_a_fresh_create(tmp_path: Path) -> None:
    """A created directory must yield a working database, not just an empty file."""
    target = tmp_path / "fresh" / "email_cache.db"

    cache = EmailCache(str(target))
    try:
        cache.conn.execute(
            "INSERT INTO emails (message_id, subject) VALUES (?, ?)",
            ("m1", "hello"),
        )
        cache.conn.commit()
        rows = cache.conn.execute("SELECT message_id FROM emails").fetchall()
        assert rows == [("m1",)]
    finally:
        cache.conn.close()


@pytest.mark.parametrize("segments", [("a",), ("a", "b"), ("a", "b", "c")])
def test_any_number_of_missing_levels_is_created(tmp_path: Path, segments: tuple[str, ...]) -> None:
    """makedirs, not mkdir: the fix has to handle more than one absent level."""
    target = tmp_path.joinpath(*segments) / "email_cache.db"

    cache = EmailCache(str(target))
    try:
        assert target.parent.is_dir()
    finally:
        cache.conn.close()
