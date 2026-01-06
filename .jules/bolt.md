## 2024-05-23 - Database Search Optimization
**Learning:** Python's string manipulation in tight loops is fast but adds up. In `DatabaseManager.search_emails_with_limit`, re-lowercasing subject/sender/email for every record in every search was a bottleneck ($O(N \times 3 \times L)$). Pre-computing a single lowercased "searchable text" string during indexing reduced search time by ~2.4x (26ms -> 11ms for 50k items) and reduced memory allocations during search.

**Action:** When searching across multiple string fields repeatedly, always pre-compute a combined, normalized search index field. Avoid `lower()` inside hot loops.
