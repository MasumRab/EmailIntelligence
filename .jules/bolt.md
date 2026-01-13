# Bolt's Journal

## 2024-05-23 - N+1 Cache Invalidation in Filter Logic
**Learning:** `SmartFilterManager` was invalidating the global list of active filters every time *any* filter matched an email. This is a classic N+1 problem but applied to cache invalidation. Since usage stats are updated per-match, a batch of 1000 emails matching 3 filters each would trigger 3000 DB writes and 3000 full-list cache invalidations, effectively DDOSing the cache and DB read (for re-filling the cache).
**Action:** Removed the cache invalidation on usage stats update. We accept that the `usage_count` in the cached filter list might be slightly stale, which is a worthy trade-off for the massive reduction in I/O.
