from src.core.enhanced_caching import QueryResultCache
import time

c = QueryResultCache(ttl_seconds=10)
c.put("a", 1)
print(c.get("a"))
