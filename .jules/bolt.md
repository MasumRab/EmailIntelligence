## 2025-05-23 - DatabaseManager Search Performance
**Learning:** `DatabaseManager.search_emails_with_limit` was performing O(N) disk checks (`os.path.exists` + `gzip.open`) for every search miss, causing severe performance degradation (1.28s for 50k items). Additionally, string lowering in the loop was costly.
**Action:** Implemented `_search_index` (pre-computed lowercase metadata) and `_content_available_index` (set of IDs with content) to avoid disk I/O and repeated string allocations. Also added query result caching. Result: ~100x speedup.
