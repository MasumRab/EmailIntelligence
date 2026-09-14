# Sentinel Security Journal

## 2024-04-02: Memory Exhaustion DoS in Rate Limiter

**Condition Discovered**: The rate limiter implementation in `src/utils/rate_limit.py` used a standard `collections.defaultdict(list)` to store access timestamps keyed by IP address. The collection had no bound on the number of keys it could store.

**The Learning**: If an attacker spams requests from randomly generated, spoofed, or heavily distributed IP addresses, the dictionary will grow without bounds, continuously consuming memory until the application crashes (Memory Exhaustion Denial of Service).

**Prevention Note**: When implementing structures that track data keyed by untrusted external identifiers (like IP addresses, session tokens, or user IDs), always apply a strict capacity limit. Utilizing `collections.OrderedDict` alongside an LRU eviction strategy (e.g. `if len(cache) >= max: cache.popitem(last=False)`) prevents unbounded growth and mitigates memory exhaustion DoS vectors.
