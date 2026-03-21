## 2026-01-18 - [Optimized Database Search Caching]
**Learning:** `search_emails_with_limit` in `DatabaseManager` was extremely slow (O(N*C)) due to checking disk content for every email on every search. Adding query result caching in `EnhancedCachingManager` and invalidating it on data updates reduced repeated search time from ~0.1s to ~0.00001s (~8000x speedup).
**Action:** When optimizing read-heavy operations with expensive filters (like disk I/O), always consider caching the *result* of the query, not just the individual items, and ensure proper invalidation on writes.

## 2026-01-24 - [Batched Smart Filter Updates]
**Learning:** `SmartFilterManager.apply_filters_to_email` was performing N database updates and N cache invalidations for N matching filters, causing unnecessary overhead. Consolidating updates into a single batch operation reduced DB roundtrips and cache thrashing.
**Action:** Always batch database updates (especially `UPDATE ... WHERE id IN (...)`) and cache invalidations when processing multiple items in a single logical operation.

## 2026-03-01 - [Reverse Iteration + Early Exit for Search]
**Learning:** `search_emails_with_limit` iterated over the entire email dataset forward, causing unnecessary O(N) disk I/O when falling back to content searches. Because `emails_data` is stored chronologically, iterating backwards and breaking early when `limit` is reached reduced disk I/O to O(limit), yielding a massive performance boost (~115x).
**Action:** When filtering a chronologically sorted dataset with a limit constraint, always iterate backwards to prioritize recent items and exit early once the limit is met.
