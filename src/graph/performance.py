"""
Performance optimization layer for graph operations
"""

import time
import asyncio
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import structlog
import weakref
from functools import wraps

from ...database.connection import connection_manager

logger = structlog.get_logger()


@dataclass
class QueryMetrics:
    """Metrics for query performance tracking"""

    query: str
    execution_time: float
    rows_returned: int
    cache_hit: bool
    timestamp: datetime
    node_type: str = ""
    relationship_type: str = ""


@dataclass
class OptimizationRule:
    """Optimization rule for query improvement"""

    name: str
    pattern: str
    replacement: str
    priority: int
    enabled: bool = True


class QueryOptimizer:
    """
    Optimizes Cypher queries for better performance
    """

    def __init__(self):
        self.optimization_rules = self._load_optimization_rules()
        self.query_cache = {}
        self.performance_stats = {
            "queries_optimized": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_optimization_time": 0.0,
        }

    def _load_optimization_rules(self) -> List[OptimizationRule]:
        """Load query optimization rules"""
        return [
            # Index usage optimization
            OptimizationRule(
                name="use_index_lookup",
                pattern=r"WHERE n\.(\w+)\s*=\s*\$(\w+)",
                replacement="WHERE n.\\1 = $-1 USING INDEX n:\\2(\\1)",
                priority=10,
            ),
            # Query pattern optimization
            OptimizationRule(
                name="optimize_pattern",
                pattern=r"MATCH\s*\(([^)]+)\)\s*-\s*\[([^]]+)\]\s*-\s*\(([^)]+)\)",
                replacement="MATCH (\\1)-\\2-(\\3)",
                priority=5,
            ),
            # Limit optimization
            OptimizationRule(
                name="add_limit",
                pattern=r"RETURN\s+(.+?)(?!\s*LIMIT)",
                replacement="RETURN \\1 LIMIT 1000",
                priority=3,
            ),
            # Property access optimization
            OptimizationRule(
                name="early_projection",
                pattern=r"RETURN\s+\*",
                replacement="RETURN n.id, n.title, n.status",
                priority=2,
            ),
        ]

    async def optimize_query(
        self, query: str, parameters: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """Optimize a Cypher query"""
        start_time = time.time()

        # Apply optimization rules
        optimized_query = query
        for rule in sorted(self.optimization_rules, key=lambda r: r.priority, reverse=True):
            if rule.enabled:
                import re

                optimized_query = re.sub(
                    rule.pattern, rule.replacement, optimized_query, flags=re.IGNORECASE
                )

        # Add query hints for better planning
        optimized_query = self._add_query_hints(optimized_query)

        optimization_time = time.time() - start_time
        self.performance_stats["queries_optimized"] += 1
        self.performance_stats["avg_optimization_time"] = (
            self.performance_stats["avg_optimization_time"]
            * (self.performance_stats["queries_optimized"] - 1)
            + optimization_time
        ) / self.performance_stats["queries_optimized"]

        logger.debug(
            "Query optimized",
            original_query=query[:100],
            optimized_query=optimized_query[:100],
            optimization_time=optimization_time,
        )

        return optimized_query, parameters

    def _add_query_hints(self, query: str) -> str:
        """Add query hints for better performance"""
        # Add planner hint for better query planning
        if "MATCH" in query.upper() and "USING" not in query.upper():
            # Add cost-based planner hint
            query = f"CYPHER planner=cost {query}"

        return query

    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization performance statistics"""
        return {
            **self.performance_stats,
            "rules_loaded": len(self.optimization_rules),
            "cache_size": len(self.query_cache),
        }


class ParallelProcessor:
    """
    Handles parallel processing of graph operations
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running_tasks = weakref.WeakSet()
        self.performance_stats = {
            "tasks_processed": 0,
            "total_processing_time": 0.0,
            "avg_task_time": 0.0,
        }

    async def process_parallel_queries(
        self, queries: List[Dict[str, Any]], max_concurrent: int = None
    ) -> List[Any]:
        """Process multiple queries in parallel"""
        if max_concurrent is None:
            max_concurrent = self.max_workers

        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_single_query(query_data):
            async with semaphore:
                start_time = time.time()
                try:
                    result = await self._execute_single_query(query_data)
                    execution_time = time.time() - start_time

                    self.performance_stats["tasks_processed"] += 1
                    self.performance_stats["total_processing_time"] += execution_time
                    self.performance_stats["avg_task_time"] = (
                        self.performance_stats["total_processing_time"]
                        / self.performance_stats["tasks_processed"]
                    )

                    return result
                except Exception as e:
                    logger.error(
                        "Parallel query processing failed",
                        error=str(e),
                        query=query_data.get("query", "")[:100],
                    )
                    return None

        # Execute all queries in parallel
        tasks = [process_single_query(query_data) for query_data in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and None results
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]

        logger.info(
            "Parallel query processing completed",
            total_queries=len(queries),
            successful_queries=len(valid_results),
            failed_queries=len(queries) - len(valid_results),
        )

        return valid_results

    async def _execute_single_query(self, query_data: Dict[str, Any]) -> Any:
        """Execute a single query"""
        query = query_data["query"]
        parameters = query_data.get("parameters", {})
        query_type = query_data.get("type", "read")

        if query_type == "write":
            return await connection_manager.execute_write_transaction(
                lambda tx: tx.run(query, parameters)
            )
        else:
            records = await connection_manager.execute_query(query, parameters)
            return records

    def get_parallel_stats(self) -> Dict[str, Any]:
        """Get parallel processing statistics"""
        return {
            **self.performance_stats,
            "max_workers": self.max_workers,
            "active_tasks": len(self.running_tasks),
        }


class MaterializedView:
    """
    Manages materialized views for frequently accessed data
    """

    def __init__(self, name: str, query: str, refresh_interval: int = 300):
        self.name = name
        self.query = query
        self.refresh_interval = refresh_interval
        self.last_refresh = None
        self.data = None
        self.is_refreshing = False
        self.performance_stats = {
            "refreshes": 0,
            "total_refresh_time": 0.0,
            "cache_hits": 0,
            "avg_query_time": 0.0,
        }

    async def refresh(self) -> bool:
        """Refresh the materialized view"""
        if self.is_refreshing:
            logger.warning("Materialized view refresh already in progress", view_name=self.name)
            return False

        self.is_refreshing = True
        start_time = time.time()

        try:
            logger.info("Refreshing materialized view", view_name=self.name)

            # Execute the query
            records = await connection_manager.execute_query(self.query)

            # Process and store the data
            self.data = self._process_view_data(records)
            self.last_refresh = datetime.utcnow()

            refresh_time = time.time() - start_time
            self.performance_stats["refreshes"] += 1
            self.performance_stats["total_refresh_time"] += refresh_time
            self.performance_stats["avg_query_time"] = (
                self.performance_stats["total_refresh_time"] / self.performance_stats["refreshes"]
            )

            logger.info(
                "Materialized view refreshed successfully",
                view_name=self.name,
                refresh_time=refresh_time,
                record_count=len(records) if records else 0,
            )

            return True

        except Exception as e:
            logger.error("Materialized view refresh failed", view_name=self.name, error=str(e))
            return False

        finally:
            self.is_refreshing = False

    def _process_view_data(self, records: List[Dict[str, Any]]) -> Any:
        """Process and structure the view data"""
        # This would be customized based on the specific view
        return records

    def needs_refresh(self) -> bool:
        """Check if the view needs to be refreshed"""
        if self.last_refresh is None:
            return True

        age = (datetime.utcnow() - self.last_refresh).total_seconds()
        return age > self.refresh_interval

    def get_data(self, use_cache: bool = True) -> Optional[Any]:
        """Get data from the materialized view"""
        if use_cache and self.data is not None and not self.needs_refresh():
            self.performance_stats["cache_hits"] += 1
            return self.data

        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get materialized view performance statistics"""
        return {
            **self.performance_stats,
            "name": self.name,
            "last_refresh": (self.last_refresh.isoformat() if self.last_refresh else None),
            "needs_refresh": self.needs_refresh(),
            "is_refreshing": self.is_refreshing,
        }


class GraphCache:
    """
    Specialized caching for graph operations
    """

    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self.query_cache = {}
        self.node_cache = {}
        self.path_cache = {}
        self.performance_stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "entries_evicted": 0,
            "total_cache_size": 0,
        }

    def get_cached_query(self, query_hash: str, parameters_hash: str) -> Optional[Any]:
        """Get cached query result"""
        cache_key = f"{query_hash}:{parameters_hash}"

        if cache_key in self.query_cache:
            entry = self.query_cache[cache_key]

            # Check if entry is still valid
            if datetime.utcnow() < entry["expires_at"]:
                self.performance_stats["cache_hits"] += 1
                return entry["data"]
            else:
                # Remove expired entry
                del self.query_cache[cache_key]
                self.performance_stats["entries_evicted"] += 1

        self.performance_stats["cache_misses"] += 1
        return None

    def cache_query_result(self, query_hash: str, parameters_hash: str, data: Any, ttl: int = None):
        """Cache query result"""
        ttl = ttl or self.default_ttl
        cache_key = f"{query_hash}:{parameters_hash}"

        self.query_cache[cache_key] = {
            "data": data,
            "expires_at": datetime.utcnow() + timedelta(seconds=ttl),
            "created_at": datetime.utcnow(),
        }

        # Clean up old entries if cache gets too large
        if len(self.query_cache) > 1000:
            self._evict_expired_entries()

    def get_cached_node(self, node_id: str, node_type: str) -> Optional[Dict[str, Any]]:
        """Get cached node data"""
        cache_key = f"{node_type}:{node_id}"

        if cache_key in self.node_cache:
            entry = self.node_cache[cache_key]

            if datetime.utcnow() < entry["expires_at"]:
                self.performance_stats["cache_hits"] += 1
                return entry["data"]
            else:
                del self.node_cache[cache_key]
                self.performance_stats["entries_evicted"] += 1

        self.performance_stats["cache_misses"] += 1
        return None

    def cache_node(self, node_id: str, node_type: str, data: Dict[str, Any], ttl: int = None):
        """Cache node data"""
        ttl = ttl or self.default_ttl
        cache_key = f"{node_type}:{node_id}"

        self.node_cache[cache_key] = {
            "data": data,
            "expires_at": datetime.utcnow() + timedelta(seconds=ttl),
            "created_at": datetime.utcnow(),
        }

    def _evict_expired_entries(self):
        """Remove expired entries from all caches"""
        current_time = datetime.utcnow()

        # Clean query cache
        expired_keys = [
            key for key, entry in self.query_cache.items() if current_time >= entry["expires_at"]
        ]
        for key in expired_keys:
            del self.query_cache[key]

        # Clean node cache
        expired_keys = [
            key for key, entry in self.node_cache.items() if current_time >= entry["expires_at"]
        ]
        for key in expired_keys:
            del self.node_cache[key]

        self.performance_stats["entries_evicted"] += len(expired_keys)

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        self.performance_stats["total_cache_size"] = (
            len(self.query_cache) + len(self.node_cache) + len(self.path_cache)
        )

        hit_rate = self.performance_stats["cache_hits"] / max(
            self.performance_stats["cache_hits"] + self.performance_stats["cache_misses"],
            1,
        )

        return {
            **self.performance_stats,
            "hit_rate": hit_rate,
            "query_cache_size": len(self.query_cache),
            "node_cache_size": len(self.node_cache),
            "path_cache_size": len(self.path_cache),
        }

    def clear_all_caches(self):
        """Clear all caches"""
        self.query_cache.clear()
        self.node_cache.clear()
        self.path_cache.clear()

        logger.info("All graph caches cleared")


class PerformanceOptimizationEngine:
    """
    Main performance optimization engine
    """

    def __init__(self, max_workers: int = 4, cache_ttl: int = 300):
        self.query_optimizer = QueryOptimizer()
        self.parallel_processor = ParallelProcessor(max_workers)
        self.graph_cache = GraphCache(cache_ttl)
        self.materialized_views = {}
        self.performance_stats = {
            "optimizations_applied": 0,
            "performance_improvements": 0.0,
            "avg_response_time": 0.0,
        }

    async def initialize(self) -> bool:
        """Initialize the performance optimization engine"""
        logger.info("Initializing performance optimization engine")

        # Initialize materialized views
        await self._initialize_materialized_views()

        logger.info("Performance optimization engine initialized")
        return True

    async def _initialize_materialized_views(self):
        """Initialize materialized views for common queries"""
        views = [
            MaterializedView(
                "active_conflicts",
                """
                MATCH (c:Conflict)-[:AFFECTS]-(pr:PullRequest)
                WHERE c.severity IN ['CRITICAL', 'HIGH']
                RETURN pr.id as pr_id, pr.title, c.type, c.severity, c.detected_at
                ORDER BY c.detected_at DESC
                LIMIT 100
                """,
                refresh_interval=60,
            ),
            MaterializedView(
                "pr_complexity_scores",
                """
                MATCH (pr:PullRequest)
                OPTIONAL MATCH (pr)-[:HAS_CONFLICT]->(c:Conflict)
                WITH pr, count(c) as conflict_count
                RETURN pr.id, pr.title, pr.complexity, conflict_count
                ORDER BY pr.complexity DESC
                """,
                refresh_interval=300,
            ),
        ]

        for view in views:
            self.materialized_views[view.name] = view
            # Initial refresh
            await view.refresh()

    async def execute_optimized_query(
        self, query: str, parameters: Dict[str, Any] = None, use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """Execute an optimized query"""
        start_time = time.time()
        parameters = parameters or {}

        # Check cache
        if use_cache:
            query_hash = str(hash(query))
            parameters_hash = str(hash(str(sorted(parameters.items()))))
            cached_result = self.graph_cache.get_cached_query(query_hash, parameters_hash)

            if cached_result is not None:
                return cached_result

        # Optimize query
        optimized_query, optimized_params = await self.query_optimizer.optimize_query(
            query, parameters
        )

        # Execute query
        try:
            records = await connection_manager.execute_query(optimized_query, optimized_params)

            # Cache result
            if use_cache and records:
                self.graph_cache.cache_query_result(query_hash, parameters_hash, records)

            execution_time = time.time() - start_time

            # Update performance stats
            self._update_performance_stats(execution_time, True)

            logger.debug(
                "Query executed successfully",
                query=query[:100],
                execution_time=execution_time,
                record_count=len(records) if records else 0,
            )

            return records or []

        except Exception as e:
            execution_time = time.time() - start_time
            self._update_performance_stats(execution_time, False)

            logger.error(
                "Query execution failed",
                error=str(e),
                query=query[:100],
                execution_time=execution_time,
            )
            raise

    async def execute_parallel_operations(
        self, operations: List[Dict[str, Any]], max_concurrent: int = None
    ) -> List[Any]:
        """Execute multiple operations in parallel"""
        return await self.parallel_processor.process_parallel_queries(operations, max_concurrent)

    def _update_performance_stats(self, execution_time: float, success: bool):
        """Update performance statistics"""
        if success:
            self.performance_stats["optimizations_applied"] += 1

            # Calculate average response time
            current_avg = self.performance_stats["avg_response_time"]
            total_ops = self.performance_stats["optimizations_applied"]

            self.performance_stats["avg_response_time"] = (
                current_avg * (total_ops - 1) + execution_time
            ) / total_ops

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        return {
            **self.performance_stats,
            "query_optimizer": self.query_optimizer.get_optimization_stats(),
            "parallel_processor": self.parallel_processor.get_parallel_stats(),
            "cache": self.graph_cache.get_cache_stats(),
        }


# Global performance optimization engine instance
performance_engine = PerformanceOptimizationEngine()


def optimize_graph_query(func: Callable) -> Callable:
    """Decorator to automatically optimize graph queries"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This would integrate with the performance engine
        # For now, just pass through
        return await func(*args, **kwargs)

    return wrapper
