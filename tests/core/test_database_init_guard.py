"""Initialization guard tests for DatabaseManager.

Two properties are checked here:

1. The load-and-build sequence runs **once**, even when several coroutines
   arrive before it finishes. `_load_data()` awaits, so a second coroutine can
   observe `_initialized is False` while the first is still inside it — a flag
   check alone lets both load the dataset.
2. The public entry points trigger initialization instead of reading an empty
   in-memory dataset. A `DatabaseManager` constructed directly (rather than
   through `get_database_manager()`) starts uninitialized, and a read or write
   before the first load would otherwise see no emails at all.
"""

import asyncio

import pytest

from src.core.database import DatabaseConfig, DatabaseManager


@pytest.fixture
def manager(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseManager(config=DatabaseConfig(data_dir=str(data_dir)))


@pytest.mark.asyncio
async def test_concurrent_initialization_loads_once(manager, monkeypatch):
    """Two concurrent first calls must not both run `_load_data()`."""
    calls = []

    async def counting_load():
        calls.append(1)
        # Yield: this is exactly the window a bare `if not self._initialized`
        # check leaves open for the second coroutine to enter.
        await asyncio.sleep(0)

    monkeypatch.setattr(manager, "_load_data", counting_load)
    monkeypatch.setattr(manager, "_build_indexes", lambda: None)

    await asyncio.gather(
        manager._ensure_initialized(),
        manager._ensure_initialized(),
    )

    assert len(calls) == 1
    assert manager._initialized is True


@pytest.mark.asyncio
async def test_sequential_initialization_is_idempotent(manager, monkeypatch):
    """A second call after the first has completed is a no-op."""
    calls = []

    async def counting_load():
        calls.append(1)

    monkeypatch.setattr(manager, "_load_data", counting_load)
    monkeypatch.setattr(manager, "_build_indexes", lambda: None)

    await manager._ensure_initialized()
    await manager._ensure_initialized()

    assert len(calls) == 1


@pytest.mark.asyncio
async def test_get_email_by_id_initializes_before_reading(manager, monkeypatch):
    """A read on a fresh manager loads the dataset before answering."""
    loaded = []

    async def fake_load():
        loaded.append(1)
        record = {"id": 7, "subject": "loaded from disk"}
        manager.emails_data = [record]

    def fake_build_indexes():
        manager.emails_by_id = {7: manager.emails_data[0]}

    monkeypatch.setattr(manager, "_load_data", fake_load)
    monkeypatch.setattr(manager, "_build_indexes", fake_build_indexes)

    assert manager._initialized is False
    assert manager.emails_by_id == {}

    result = await manager.get_email_by_id(7, include_content=False)

    assert loaded == [1]
    assert result is not None
    assert result["subject"] == "loaded from disk"


@pytest.mark.asyncio
async def test_create_category_initializes_before_writing(manager, monkeypatch):
    """A write on a fresh manager loads first, so it appends to the real data."""
    loaded = []

    async def fake_load():
        loaded.append(1)
        manager.categories_data = [{"id": 1, "name": "existing"}]

    def fake_build_indexes():
        manager.categories_by_id = {1: {"id": 1, "name": "existing"}}
        manager.categories_by_name = {"existing": {"id": 1, "name": "existing"}}

    monkeypatch.setattr(manager, "_load_data", fake_load)
    monkeypatch.setattr(manager, "_build_indexes", fake_build_indexes)

    assert manager._initialized is False

    created = await manager.create_category({"name": "fresh"})

    assert loaded == [1]
    assert created is not None
    # The id is generated from the loaded list, so it must continue after it.
    assert created["id"] == 2
