"""
System integration layer for Graph Traversal and Conflict Detection
Connects all graph components with existing GraphQL API, Neo4j database, and OpenAI integration
"""

import asyncio
import time
from typing import List, Dict, Optional, Any
from datetime import datetime
import structlog
from dataclasses import asdict

from .traversal import traversal_engine
from .analytics import analytics_engine
from .performance import performance_engine
from .scoring import conflict_scoring_engine
from .specialized import (
    specialized_engine,
)
from .cache import graph_cache, graph_monitor
from ...database.data_access import pr_dao, conflict_dao
from ...database.connection import connection_manager

# ARCHIVED: PR Resolution System - AI client moved to archive
# from ...ai.client import openai_client
# Original import commented out - moved to archive/pr-resolution-archive/src/ai/
from ...models.graph_entities import PullRequest, Conflict
from ...utils.monitoring import get_monitor

logger = structlog.get_logger()
monitor = get_monitor()


class GraphTraversalSystem:
    """
    Unified system integration layer for all graph traversal and conflict detection components
    """

    def __init__(self):
        self.traversal_engine = traversal_engine
        self.analytics_engine = analytics_engine
        self.performance_engine = performance_engine
        self.scoring_engine = conflict_scoring_engine
        self.specialized_engine = specialized_engine
        self.cache_manager = graph_cache
        self.performance_monitor = graph_monitor

        # Performance thresholds
        self.performance_thresholds = {
            "conflict_detection": 0.5,  # seconds
            "traversal_query": 1.0,  # seconds
            "scoring_query": 0.1,  # seconds
            "cache_hit_rate": 0.8,  # 80%
        }

        # System health status
        self.system_health = {
            "status": "healthy",
            "components": {
                "traversal": "healthy",
                "analytics": "healthy",
                "performance": "healthy",
                "scoring": "healthy",
                "specialized": "healthy",
                "cache": "healthy",
            },
            "last_check": datetime.utcnow(),
        }

    async def analyze_pull_request(
        self,
        pr_id: str,
        include_ai_analysis: bool = True,
        max_analysis_time: float = 30.0,
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of a single pull request

        Args:
            pr_id: Pull request ID to analyze
            include_ai_analysis: Whether to include AI-powered analysis
            max_analysis_time: Maximum time allowed for analysis

        Returns:
            Comprehensive analysis results
        """
        start_time = time.time()
        logger.info("Starting PR analysis", pr_id=pr_id, include_ai=include_ai_analysis)

        try:
            # Step 1: Get PR data
            pr = await pr_dao.get_pr(pr_id)
            if not pr:
                raise ValueError(f"Pull request {pr_id} not found")

            # Step 2: Perform graph traversal analysis
            traversal_result = await self._analyze_pr_traversal(pr)

            # Step 3: Detect conflicts
            conflicts = await self._detect_pr_conflicts(pr)

            # Step 4: Perform specialized analysis
            specialized_results = await self._perform_specialized_analysis(pr)

            # Step 5: Score conflicts
            conflict_scores = []
            if conflicts:
                conflict_scores = await self._score_conflicts(conflicts, pr)

            # Step 6: Perform analytics
            analytics_result = await self._perform_analytics(pr)

            # Step 7: AI analysis if requested
            ai_analysis = None
            if include_ai_analysis and conflicts:
                ai_analysis = await self._perform_ai_analysis(conflicts, pr)

            # Calculate analysis time
            analysis_time = time.time() - start_time

            # Prepare comprehensive result
            result = {
                "pr_id": pr_id,
                "analysis_timestamp": datetime.utcnow(),
                "analysis_time": analysis_time,
                "within_time_limit": analysis_time <= max_analysis_time,
                "pr_info": {
                    "title": pr.title,
                    "complexity": pr.complexity,
                    "estimated_resolution_time": pr.estimated_resolution_time,
                    "author_id": pr.author_id,
                    "status": pr.status.value,
                },
                "traversal_analysis": (asdict(traversal_result) if traversal_result else None),
                "conflicts": [asdict(c) for c in conflicts],
                "conflict_scores": (
                    [asdict(cs) for cs in conflict_scores] if conflict_scores else []
                ),
                "specialized_analysis": specialized_results,
                "analytics": analytics_result,
                "ai_analysis": ai_analysis,
                "recommendations": await self._generate_recommendations(
                    conflicts, conflict_scores, specialized_results
                ),
            }

            # Record performance metrics
            await self._record_analysis_performance(
                analysis_time, len(conflicts), len(conflict_scores)
            )

            logger.info(
                "PR analysis completed",
                pr_id=pr_id,
                analysis_time=analysis_time,
                conflicts_found=len(conflicts),
                conflicts_scored=len(conflict_scores),
            )

            return result

        except Exception as e:
            logger.error("PR analysis failed", pr_id=pr_id, error=str(e))
            raise

    async def analyze_pull_requests_batch(
        self,
        pr_ids: List[str],
        max_concurrent: int = 5,
        include_ai_analysis: bool = True,
    ) -> Dict[str, Any]:
        """
        Analyze multiple pull requests in batch

        Args:
            pr_ids: List of PR IDs to analyze
            max_concurrent: Maximum concurrent analyses
            include_ai_analysis: Whether to include AI analysis

        Returns:
            Batch analysis results
        """
        start_time = time.time()
        logger.info(
            "Starting batch PR analysis",
            pr_count=len(pr_ids),
            max_concurrent=max_concurrent,
        )

        # Use semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        async def analyze_single_pr(pr_id: str) -> Dict[str, Any]:
            async with semaphore:
                try:
                    return await self.analyze_pull_request(pr_id, include_ai_analysis)
                except Exception as e:
                    logger.error("Batch PR analysis failed for PR", pr_id=pr_id, error=str(e))
                    return {
                        "pr_id": pr_id,
                        "error": str(e),
                        "analysis_timestamp": datetime.utcnow(),
                    }

        # Execute analyses concurrently
        tasks = [analyze_single_pr(pr_id) for pr_id in pr_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        successful_results = []
        failed_results = []

        for result in results:
            if isinstance(result, Exception):
                failed_results.append({"error": str(result)})
            elif "error" in result:
                failed_results.append(result)
            else:
                successful_results.append(result)

        batch_time = time.time() - start_time

        summary = {
            "batch_timestamp": datetime.utcnow(),
            "batch_time": batch_time,
            "total_prs": len(pr_ids),
            "successful_analyses": len(successful_results),
            "failed_analyses": len(failed_results),
            "success_rate": len(successful_results) / len(pr_ids) if pr_ids else 0.0,
            "results": successful_results,
            "failures": failed_results,
        }

        logger.info(
            "Batch PR analysis completed",
            total_prs=len(pr_ids),
            successful=len(successful_results),
            failed=len(failed_results),
            batch_time=batch_time,
        )

        return summary

    async def detect_real_time_conflicts(
        self, pr_id: str, check_interval: float = 10.0, max_checks: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Real-time conflict detection with periodic checking

        Args:
            pr_id: PR ID to monitor
            check_interval: Time between checks in seconds
            max_checks: Maximum number of checks to perform

        Returns:
            List of conflict changes detected
        """
        logger.info(
            "Starting real-time conflict detection",
            pr_id=pr_id,
            check_interval=check_interval,
        )

        conflict_changes = []
        previous_conflicts = set()

        for check in range(max_checks):
            try:
                # Get current conflicts
                pr = await pr_dao.get_pr(pr_id)
                if not pr:
                    break

                current_conflicts = await conflict_dao.get_conflicts(limit=100)
                current_pr_conflicts = [
                    c for c in current_conflicts if pr_id in c.affected_commit_ids
                ]
                current_conflict_ids = {c.id for c in current_pr_conflicts}

                # Compare with previous state
                new_conflicts = current_conflict_ids - previous_conflicts
                resolved_conflicts = previous_conflicts - current_conflict_ids

                # Record changes
                if new_conflicts:
                    conflict_changes.append(
                        {
                            "timestamp": datetime.utcnow(),
                            "type": "new_conflicts",
                            "conflicts": list(new_conflicts),
                        }
                    )

                if resolved_conflicts:
                    conflict_changes.append(
                        {
                            "timestamp": datetime.utcnow(),
                            "type": "resolved_conflicts",
                            "conflicts": list(resolved_conflicts),
                        }
                    )

                previous_conflicts = current_conflict_ids

                # Check if all conflicts are resolved
                if not current_conflict_ids:
                    logger.info("All conflicts resolved", pr_id=pr_id)
                    break

                # Wait before next check
                if check < max_checks - 1:
                    await asyncio.sleep(check_interval)

            except Exception as e:
                logger.error(
                    "Real-time conflict detection error",
                    pr_id=pr_id,
                    check=check,
                    error=str(e),
                )
                break

        return conflict_changes

    async def get_system_health(self) -> Dict[str, Any]:
        """
        Get comprehensive system health status
        """
        health_checks = {}
        overall_status = "healthy"
        critical_issues = []

        # Check cache health
        cache_stats = self.cache_manager.get_cache_stats()
        if cache_stats["hit_rate"] < self.performance_thresholds["cache_hit_rate"]:
            health_checks["cache"] = "degraded"
            if cache_stats["hit_rate"] < 0.5:
                overall_status = "unhealthy"
                critical_issues.append("Very low cache hit rate")
        else:
            health_checks["cache"] = "healthy"

        # Check performance metrics
        performance_summary = self.performance_monitor.get_performance_summary(30)
        if (
            performance_summary.get("metrics", {})
            .get("graph_query_execution_time_general", {})
            .get("avg", 0)
            > self.performance_thresholds["traversal_query"]
        ):
            health_checks["performance"] = "degraded"
            overall_status = "degraded" if overall_status == "healthy" else overall_status
        else:
            health_checks["performance"] = "healthy"

        # Check database connectivity
        try:
            db_healthy = await connection_manager.health_check()
            health_checks["database"] = "healthy" if db_healthy else "unhealthy"
            if not db_healthy:
                overall_status = "unhealthy"
                critical_issues.append("Database connectivity issue")
        except Exception:
            health_checks["database"] = "unhealthy"
            overall_status = "unhealthy"
            critical_issues.append("Database health check failed")

        # Check AI service
        try:
            # ARCHIVED: PR Resolution System - AI client usage commented out
            # ai_health = await openai_client.health_check()
            # # Original usage commented out - moved to archive
            # health_checks["ai_service"] = (
            #     "healthy" if ai_health.get("healthy", False) else "unhealthy"
            # )
            # # Original usage commented out
            # if not ai_health.get("healthy", False):  # Original usage commented out
            #     overall_status = "degraded" if overall_status == "healthy" else overall_status
            #     # Original usage commented out
            health_checks["ai_service"] = "archived"  # Service moved to archive
        except Exception:
            health_checks["ai_service"] = "unhealthy"
            overall_status = "degraded" if overall_status == "healthy" else overall_status

        return {
            "overall_status": overall_status,
            "timestamp": datetime.utcnow(),
            "component_health": health_checks,
            "critical_issues": critical_issues,
            "performance_summary": performance_summary,
            "cache_stats": cache_stats,
            "active_alerts": len(self.performance_monitor.get_active_alerts()),
        }

    async def optimize_system_performance(self) -> Dict[str, Any]:
        """
        Analyze and optimize system performance
        """
        logger.info("Starting system performance optimization")

        optimizations_performed = []

        # Analyze cache performance
        cache_stats = self.cache_manager.get_cache_stats()
        if cache_stats["hit_rate"] < 0.7:
            # Clear expired entries
            await self.cache_manager.cleanup_expired()
            optimizations_performed.append("Cleaned up expired cache entries")

        # Check for slow queries
        performance_summary = self.performance_monitor.get_performance_summary(60)
        slow_queries = []
        for metric, data in performance_summary.get("metrics", {}).items():
            if "execution_time" in metric and data.get("avg", 0) > 1.0:
                slow_queries.append(metric)

        if slow_queries:
            optimizations_performed.append(f"Identified slow queries: {', '.join(slow_queries)}")

        # Update thresholds based on current performance
        avg_query_time = (
            performance_summary.get("metrics", {})
            .get("graph_query_execution_time_general", {})
            .get("avg", 1.0)
        )
        if avg_query_time < 0.5:
            # Lower threshold for faster systems
            self.performance_thresholds["traversal_query"] = 0.5
            optimizations_performed.append("Updated query performance threshold to 0.5s")
        elif avg_query_time > 2.0:
            # Raise threshold for slower systems
            self.performance_thresholds["traversal_query"] = 2.0
            optimizations_performed.append("Updated query performance threshold to 2.0s")

        optimization_result = {
            "timestamp": datetime.utcnow(),
            "optimizations_performed": optimizations_performed,
            "current_thresholds": self.performance_thresholds,
            "cache_performance": cache_stats,
        }

        logger.info(
            "System performance optimization completed",
            optimizations=len(optimizations_performed),
        )

        return optimization_result

    # Helper methods

    async def _analyze_pr_traversal(self, pr: PullRequest) -> Optional[Any]:
        """Analyze PR using graph traversal"""
        try:
            cached_result = await self.cache_manager.get_traversal_result(
                "pr_analysis", {"pr_id": pr.id}
            )

            if cached_result:
                return cached_result

            # Perform traversal analysis
            result = await self.traversal_engine.breadth_first_search(
                start_node_id=pr.id, start_node_type="PullRequest", max_depth=5
            )

            # Cache result
            await self.cache_manager.cache_traversal_result("pr_analysis", {"pr_id": pr.id}, result)

            return result

        except Exception as e:
            logger.error("PR traversal analysis failed", pr_id=pr.id, error=str(e))
            return None

    async def _detect_pr_conflicts(self, pr: PullRequest) -> List[Conflict]:
        """Detect conflicts for a PR"""
        try:
            # Get conflicts from database
            conflicts = await conflict_dao.get_conflicts(limit=100)
            pr_conflicts = []

            for conflict in conflicts:
                # Check if conflict affects this PR
                if pr.id in conflict.affected_commit_ids or any(
                    f in pr.file_ids for f in conflict.affected_file_ids
                ):
                    pr_conflicts.append(conflict)

            return pr_conflicts

        except Exception as e:
            logger.error("Conflict detection failed", pr_id=pr.id, error=str(e))
            return []

    async def _score_conflicts(self, conflicts: List[Conflict], pr: PullRequest) -> List[Any]:
        """Score conflicts for prioritization"""
        try:
            scored_conflicts = await self.scoring_engine.prioritize_conflicts(
                conflicts, {conflict.id: pr for conflict in conflicts}
            )
            return scored_conflicts

        except Exception as e:
            logger.error("Conflict scoring failed", pr_id=pr.id, error=str(e))
            return []

    async def _perform_specialized_analysis(self, pr: PullRequest) -> Dict[str, Any]:
        """Perform specialized analysis for PR"""
        try:
            # File change analysis
            file_patterns = await self.specialized_engine.analyze_file_change_patterns(pr)

            # Dependency analysis
            dependency_analysis = await self.specialized_engine.analyze_dependency_graph(pr)

            # Architecture compliance
            architecture_compliance = (
                await self.specialized_engine.validate_architecture_compliance(pr)
            )

            return {
                "file_patterns": file_patterns,
                "dependency_analysis": dependency_analysis,
                "architecture_compliance": architecture_compliance,
            }

        except Exception as e:
            logger.error("Specialized analysis failed", pr_id=pr.id, error=str(e))
            return {}

    async def _perform_analytics(self, pr: PullRequest) -> Dict[str, Any]:
        """Perform graph analytics"""
        try:
            # Calculate centrality
            centrality = await self.analytics_engine.calculate_centrality(
                node_ids=[pr.id], metrics=["degree_centrality"]
            )

            # Get similar PRs
            similar_prs = await self.analytics_engine.find_similar_nodes(
                target_node_id=pr.id, similarity_threshold=0.6
            )

            return {"centrality": centrality, "similar_prs": similar_prs}

        except Exception as e:
            logger.error("Analytics failed", pr_id=pr.id, error=str(e))
            return {}

    async def _perform_ai_analysis(
        self, conflicts: List[Conflict], pr: PullRequest
    ) -> Optional[Dict[str, Any]]:
        """Perform AI-powered analysis"""
        try:
            if not conflicts:
                return None

            # Use OpenAI for analysis
            # messages = [
            #     {
            #         "role": "system",
            #         "content": "You are a senior software architect analyzing PR conflicts.",
            #     },
            #     {
            #         "role": "user",
            #         "content": (
            #             f"Analyze the following PR conflicts:\n\n"
            #             f"PR: {conflict_context['pr_title']}\n"
            #             f"Conflicts: {', '.join(conflict_context['conflicts'])}\n"
            #             f"Complexity: {conflict_context['complexity']}\n\n"
            #             "Provide analysis and resolution suggestions."
            #         ),
            #     },
            # ]

            # ARCHIVED: PR Resolution System - AI client usage commented out
            # response = await openai_client.chat_completion(messages, max_tokens=1000)
            # # Original usage commented out - moved to archive
            #
            # if response and "choices" in response:  # Original usage commented out
            #     return {  # Original usage commented out
            #         "ai_analysis": response["choices"][0]["message"]["content"],
            #         # Original usage commented out
            #         "confidence": 0.8,  # Default confidence  # Original usage commented out
            #         "model": response.get("model", "unknown")  # Original usage commented out
            #     }  # Original usage commented out
            return {
                "ai_analysis": "AI analysis service moved to archive - functionality disabled",
                "confidence": 0.0,
                "model": "archived",
            }

        except Exception as e:
            logger.error("AI analysis failed", pr_id=pr.id, error=str(e))

        return None

    async def _generate_recommendations(
        self,
        conflicts: List[Conflict],
        scored_conflicts: List[Any],
        specialized_results: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []

        # High priority conflicts
        high_priority_conflicts = [
            sc for sc in scored_conflicts if sc.priority.value in ["urgent", "high"]
        ]
        if high_priority_conflicts:
            recommendations.append(
                {
                    "type": "high_priority_conflicts",
                    "description": (
                        f"Address {len(high_priority_conflicts)} high-priority conflicts first"
                    ),
                    "conflicts": [c.conflict_id for c in high_priority_conflicts],
                    "priority": "urgent",
                }
            )

        # Architecture violations
        if specialized_results.get("architecture_compliance", {}).get("violations"):
            recommendations.append(
                {
                    "type": "architecture_violations",
                    "description": "Address architecture pattern violations",
                    "priority": "medium",
                }
            )

        # Performance recommendations
        if specialized_results.get("dependency_analysis", {}).get("risks"):
            recommendations.append(
                {
                    "type": "dependency_risks",
                    "description": "Review and resolve dependency risks",
                    "priority": "high",
                }
            )

        return recommendations

    async def _record_analysis_performance(
        self, analysis_time: float, conflict_count: int, scored_count: int
    ):
        """Record analysis performance metrics"""
        self.performance_monitor.record_conflict_detection_time(analysis_time, "pr_analysis")

        if conflict_count > 0:
            self.performance_monitor.record_scoring_time(analysis_time, conflict_count)


# Global system instance
graph_system = GraphTraversalSystem()


# Convenience functions for external use


async def analyze_pr(pr_id: str, include_ai: bool = True) -> Dict[str, Any]:
    """Analyze a single pull request"""
    return await graph_system.analyze_pull_request(pr_id, include_ai)


async def analyze_prs_batch(pr_ids: List[str], max_concurrent: int = 5) -> Dict[str, Any]:
    """Analyze multiple pull requests in batch"""
    return await graph_system.analyze_pull_requests_batch(pr_ids, max_concurrent)


async def detect_conflicts_realtime(pr_id: str) -> List[Dict[str, Any]]:
    """Detect conflicts in real-time"""
    return await graph_system.detect_real_time_conflicts(pr_id)


def get_system_status() -> Dict[str, Any]:
    """Get system health and status"""
    return asyncio.run(graph_system.get_system_health())


async def optimize_performance() -> Dict[str, Any]:
    """Optimize system performance"""
    return await graph_system.optimize_system_performance()
