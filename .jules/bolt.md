## 2026-01-18 - [Optimized Database Search Caching]
**Learning:** `search_emails_with_limit` in `DatabaseManager` was extremely slow (O(N*C)) due to checking disk content for every email on every search. Adding query result caching in `EnhancedCachingManager` and invalidating it on data updates reduced repeated search time from ~0.1s to ~0.00001s (~8000x speedup).
**Action:** When optimizing read-heavy operations with expensive filters (like disk I/O), always consider caching the *result* of the query, not just the individual items, and ensure proper invalidation on writes.

## 2026-01-24 - [Batched Smart Filter Updates]
**Learning:** `SmartFilterManager.apply_filters_to_email` was performing N database updates and N cache invalidations for N matching filters, causing unnecessary overhead. Consolidating updates into a single batch operation reduced DB roundtrips and cache thrashing.
**Action:** Always batch database updates (especially `UPDATE ... WHERE id IN (...)`) and cache invalidations when processing multiple items in a single logical operation.

## 2026-03-08 - [Optimize SmartFilterManager caching mechanism (Review 2 Feedback)]
**Learning:** SQLite objects created in a thread can only be used in that same thread. Moving `_db_execute` into `run_in_executor` violated this constraint and crashed the test suite with a `ProgrammingError`. Additionally, the previous patch missed proper `asyncio` handling.
**Action:** Reverted the attempt to use `run_in_executor` for database execution. Instead, the `apply_filters_to_email` retains the `await self._batch_update_filter_usage` call inline, but we make the *cache invalidation* asynchronous and non-blocking (`create_task` inside `_batch_update_filter_usage`) while retaining a strong reference to the task in `self._background_tasks`. This speeds up the overall return without hitting threading limits.

## 2026-03-08 - [Optimize SmartFilterManager caching mechanism (Review 3 Feedback)]
**Learning:** Hardcoding `asyncio.sleep(0.01)` inside tests to wait for a fire-and-forget task creates flakiness on slower CI systems. Unhandled exceptions in fire-and-forget tasks trigger `asyncio` "Task exception was never retrieved" warnings.
**Action:** Removed the `sleep` from tests and instead await `asyncio.gather(*manager._background_tasks)` deterministically. Added a `try/except` block inside the task itself and wrapped `t.result()` in the `_on_task_done` callback to capture and log any potential cache invalidation exceptions securely, preventing terminal warnings.
