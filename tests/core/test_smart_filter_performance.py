import pytest
import asyncio
import os
import time
from src.core.smart_filter_manager import SmartFilterManager

@pytest.mark.asyncio
async def test_filter_batch_update_performance():
    db_path = "test_smart_filters_perf.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    manager = SmartFilterManager(db_path=db_path)

    # Create filters
    for i in range(50):
        await manager.add_custom_filter(
            name=f"Filter {i}",
            description="Test filter",
            criteria={"subject_keywords": ["performance"]},
            actions={"add_label": f"Label_{i}"},
            priority=5
        )

    email_data = {
        "id": "email_perf_test",
        "subject": "This email should match performance criteria",
        "sender": "test@example.com",
        "content": "Content here"
    }

    start_time = time.perf_counter()
    summary = await manager.apply_filters_to_email(email_data)
    end_time = time.perf_counter()

    duration = end_time - start_time

    await manager.cleanup()
    if os.path.exists(db_path):
        os.remove(db_path)

    # Verify functionality
    assert len(summary["filters_matched"]) == 50

    # Verify performance
    # It should be well under 0.05s on most machines (we got 0.005s)
    # We set a conservative limit to avoid flaky tests on slow CI
    assert duration < 0.1, f"Performance regression: {duration}s > 0.1s"
