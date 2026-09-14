## 2024-05-18: Memory Exhaustion in RateLimiter

*   **Vulnerability Discovered:** The `RateLimiter` class in `src/utils/rate_limit.py` used an unbounded `defaultdict(list)` to track client requests. This lack of an upper limit could allow an attacker to exhaust server memory (Denial of Service) by continually sending requests from distinct IP addresses.
*   **Learning:** Even sliding-window rate limiters require a hard cap on the number of unique tracking keys (e.g., IPs) stored in memory. Using a `defaultdict` is convenient but fundamentally unsafe for unbounded inputs.
*   **Prevention Note:** Always enforce strict capacity limits on in-memory data structures tracking user-provided or network-derived keys. `collections.OrderedDict` provides an effective way to implement an LRU cache with an $O(1)$ eviction mechanism using `.popitem(last=False)`.
