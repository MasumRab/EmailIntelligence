## 2026-01-18 - [Optimized SmartFilterManager Performance]
**Learning:** `SmartFilterManager.apply_filters_to_email` was suffering from N+1 database update issues, performing a separate DB write and cache invalidation for *every* matched filter.
**Action:** Implemented `_batch_update_filter_usage` to consolidate all filter updates into a single transaction and a single cache invalidation. Also optimized keyword extraction regex by pre-compiling it and moving length checks to the regex engine.
**Result:** ~13x speedup in email filtering (31ms -> 2.4ms per email) in high-match scenarios.
