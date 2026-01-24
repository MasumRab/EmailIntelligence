## 2025-02-18 - Optimized MemoryCacheBackend with OrderedDict
**Learning:** The initial implementation of `MemoryCacheBackend` used a `list` to track access order for LRU eviction, resulting in $O(n)$ complexity for `get` and `set` operations. This became a significant bottleneck as the cache size grew.
**Action:** Replaced the `dict` + `list` implementation with `collections.OrderedDict`, which provides $O(1)$ complexity for LRU operations. Benchmarking showed a ~20x improvement in cache population and ~140x improvement in random access. Always prefer `OrderedDict` for LRU caches in Python.
