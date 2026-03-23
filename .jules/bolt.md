## 2026-01-18 - [Optimized Database Search Caching]
**Learning:** `search_emails_with_limit` in `DatabaseManager` was extremely slow (O(N*C)) due to checking disk content for every email on every search. Adding query result caching in `EnhancedCachingManager` and invalidating it on data updates reduced repeated search time from ~0.1s to ~0.00001s (~8000x speedup).
**Action:** When optimizing read-heavy operations with expensive filters (like disk I/O), always consider caching the *result* of the query, not just the individual items, and ensure proper invalidation on writes.

## 2026-01-24 - [Batched Smart Filter Updates]
**Learning:** `SmartFilterManager.apply_filters_to_email` was performing N database updates and N cache invalidations for N matching filters, causing unnecessary overhead. Consolidating updates into a single batch operation reduced DB roundtrips and cache thrashing.
**Action:** Always batch database updates (especially `UPDATE ... WHERE id IN (...)`) and cache invalidations when processing multiple items in a single logical operation.

## 2026-03-23 - [Database Query Result Caching]
**Learning:** `get_emails` in `DatabaseManager` performed a linear scan (`filtered_emails = self.emails_data`) and a full O(N log N) sort (`_sort_and_paginate_emails`) every single time it was called, even when the underlying data hadn't changed.
**Action:** Cached the query results by utilizing `self.caching_manager.get_query_result` and `self.caching_manager.put_query_result`. Note: ensure mutations call `self.caching_manager.clear_query_cache()`.