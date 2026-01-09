# Bolt's Journal

## 2024-05-23 - Pre-computed Search Index
**Learning:** In a read-heavy search loop, repeatedly calling string transformation methods (like `.lower()`) and dictionary lookups (`.get()`) for every item creates a significant bottleneck. Even in Python, "micro-optimizations" like hoisting these operations out of the loop or pre-computing them into a cache can yield double-digit percentage speedups (20%+ in this case).
**Action:** When implementing search over in-memory structures, always look for ways to pre-compute the "searchable representation" of the data during write/update time, rather than computing it at query time. O(N) storage is often a cheap trade for O(1) access inside an O(N) loop.

## 2024-05-23 - Mock Accuracy
**Learning:** Mocks in tests can mask performance issues and even functional drift. The existing tests were mocking `search_emails` on the database manager, but the actual code path used `search_emails_with_limit`. This meant the tests passed even if `search_emails_with_limit` was broken or inefficient.
**Action:** When mocking complex objects, verify that the methods being mocked are actually the ones being called by the system under test, preferably by using `spec=True` or similar strict mocking features, or by auditing the call graph.
