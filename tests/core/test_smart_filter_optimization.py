
import asyncio
import sys
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime, timezone

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.smart_filter_manager import SmartFilterManager, EmailFilter
from core.enhanced_caching import EnhancedCachingManager

class TestSmartFilterOptimization(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Initialize manager with in-memory DB
        self.manager = SmartFilterManager(db_path=":memory:")
        await self.manager._ensure_initialized()

        # Create a test filter
        self.test_filter = EmailFilter(
            filter_id="test_filter_1",
            name="Test Filter",
            description="Test",
            criteria={"subject_keywords": ["test"]},
            actions={"add_label": "Test"},
            priority=10,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
            is_active=True
        )

        # Insert into DB
        await self.manager._save_filter_async(self.test_filter)

    async def test_update_filter_usage_avoids_invalidation(self):
        # 1. Populate cache
        filters_1 = await self.manager.get_active_filters_sorted()
        self.assertEqual(len(filters_1), 1)
        self.assertEqual(filters_1[0].usage_count, 0)

        # Spy on caching manager
        with patch.object(self.manager.caching_manager, 'delete', side_effect=self.manager.caching_manager.delete) as mock_delete:

            # 2. Update usage
            await self.manager._update_filter_usage("test_filter_1")

            # 3. Verify 'delete' was NOT called for "active_filters_sorted"
            # It might be called for other keys if logic changes, but we optimized to avoid this one
            calls = [call for call in mock_delete.call_args_list if call[0][0] == "active_filters_sorted"]
            self.assertEqual(len(calls), 0, "Should not invalidate active_filters_sorted cache")

            # 4. Verify cache is updated in-place
            filters_2 = await self.manager.get_active_filters_sorted()
            self.assertEqual(filters_2[0].usage_count, 1)

            # And it should be the same object reference or at least from cache
            # Check stats to ensure we hit the cache
            stats = self.manager.caching_manager.get_cache_statistics()
            # We called get_active_filters_sorted twice.
            # First time: miss (put).
            # Inside _update_filter_usage: get (hit).
            # Second time: get (hit).

            # Note: _save_filter_async might also populate cache or invalidate.
            # But let's check query_cache stats
            # query_result_get count should be > 0
            self.assertGreater(stats['operations']['query_result_get'], 0)

    async def test_update_filter_usage_db_sync(self):
        # Ensure DB is actually updated
        await self.manager._update_filter_usage("test_filter_1")

        # Fetch directly from DB to verify
        row = self.manager._db_fetchone("SELECT usage_count FROM email_filters WHERE filter_id = ?", ("test_filter_1",))
        self.assertEqual(row['usage_count'], 1)

if __name__ == "__main__":
    unittest.main()
