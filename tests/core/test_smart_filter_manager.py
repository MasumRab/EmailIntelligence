
import pytest
import pytest_asyncio
import asyncio
import os
from datetime import datetime
from src.core.smart_filter_manager import SmartFilterManager

@pytest_asyncio.fixture
async def smart_filter_manager():
    db_path = "test_smart_filters_unit.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    manager = SmartFilterManager(db_path=db_path)
    await manager._ensure_initialized()
    yield manager

    await manager.cleanup()
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.mark.asyncio
async def test_apply_filters_updates_usage_batch(smart_filter_manager):
    # Create multiple filters that match "urgent"
    filter1 = await smart_filter_manager.add_custom_filter(
        name="Urgent 1", description="desc",
        criteria={"subject_keywords": ["urgent"]},
        actions={"add_label": "Urgent1"}
    )
    filter2 = await smart_filter_manager.add_custom_filter(
        name="Urgent 2", description="desc",
        criteria={"subject_keywords": ["urgent"]},
        actions={"add_label": "Urgent2"}
    )

    initial_usage1 = filter1.usage_count
    initial_usage2 = filter2.usage_count

    email_data = {
        "id": "1",
        "subject": "This is urgent",
        "content": "content"
    }

    await smart_filter_manager.apply_filters_to_email(email_data)

    # Reload filters
    updated_filter1 = await smart_filter_manager.get_filter_by_id(filter1.filter_id)
    updated_filter2 = await smart_filter_manager.get_filter_by_id(filter2.filter_id)

    assert updated_filter1.usage_count == initial_usage1 + 1
    assert updated_filter2.usage_count == initial_usage2 + 1

    # Check that cache is working (fetching again should be fast/correct)
    cached_filter1 = await smart_filter_manager.get_filter_by_id(filter1.filter_id)
    assert cached_filter1.usage_count == updated_filter1.usage_count

@pytest.mark.asyncio
async def test_batch_update_filter_usage(smart_filter_manager):
    filter1 = await smart_filter_manager.add_custom_filter(
        name="Test 1", description="desc", criteria={"subject_keywords": ["test"]}, actions={}
    )
    filter2 = await smart_filter_manager.add_custom_filter(
        name="Test 2", description="desc", criteria={"subject_keywords": ["test"]}, actions={}
    )

    await smart_filter_manager._batch_update_filter_usage([filter1.filter_id, filter2.filter_id])

    updated_filter1 = await smart_filter_manager.get_filter_by_id(filter1.filter_id)
    updated_filter2 = await smart_filter_manager.get_filter_by_id(filter2.filter_id)

    assert updated_filter1.usage_count == 1
    assert updated_filter2.usage_count == 1
