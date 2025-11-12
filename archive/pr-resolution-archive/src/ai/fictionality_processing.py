"""
Fictionality Processing Module for EmailIntelligence

Provides content hashing, fictionality-specific processing workflows,
and integration with existing caching infrastructure.
"""

import hashlib
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime

from .fictionality_analyzer import get_fictionality_analyzer
from ..models.fictionality_models import (
    FictionalityContext,
    FictionalityAnalysisRequest,
    FictionalityAnalysisOptions
)
from ..utils.caching import cache_manager
from ..config.fictionality_settings import fictionality_settings

logger = structlog.get_logger()


class FictionalityContentProcessor:
    """
    Content processor for fictionality analysis with hashing and caching
    """
    
    def __init__(self):
        self.content_cache_prefix = "fictionality:content:"
        self.analysis_cache_prefix = "fictionality:analysis:"
        self.strategy_cache_prefix = "fictionality:strategies:"
        
    async def hash_content(self, content: str) -> str:
        """
        Generate hash for content deduplication
        
        Args:
            content: Content to hash
        
        Returns:
            str: Content hash
        """
        algorithm = fictionality_settings.fictionality_content_hash_algorithm
        hasher = hashlib.new(algorithm)
        hasher.update(content.encode('utf-8'))
        
        hash_length = fictionality_settings.fictionality_content_hash_length
        return hasher.hexdigest()[:hash_length]
    
    async def get_content_hash(self, content: str) -> str:
        """
        Get cached content hash or generate new one
        
        Args:
            content: Content to hash
        
        Returns:
            str: Content hash
        """
        # Simple implementation - in production, this could cache hashes
        return await self.hash_content(content)
    
    async def cache_content_hash(
        self, 
        content: str, 
        hash_value: str
    ) -> None:
        """
        Cache content hash mapping
        
        Args:
            content: Original content
            hash_value: Generated hash
        """
        try:
            # Cache the hash mapping for faster lookup
            content_key = f"{self.content_cache_prefix}map:{hash_value}"
            await cache_manager.set(
                content_key,
                {"content": content, "hash": hash_value},
                ttl=fictionality_settings.fictionality_cache_ttl
            )
        except Exception as e:
            logger.error("Failed to cache content hash", error=str(e))
    
    async def get_cached_content_by_hash(
        self, 
        hash_value: str
    ) -> Optional[str]:
        """
        Get cached content by hash
        
        Args:
            hash_value: Content hash
        
        Returns:
            Optional[str]: Cached content or None
        """
        try:
            content_key = f"{self.content_cache_prefix}map:{hash_value}"
            cached_data = await cache_manager.get(content_key)
            return cached_data.get("content") if cached_data else None
        except Exception as e:
            logger.error("Failed to get cached content by hash", error=str(e))
        return None


class FictionalityWorkflowProcessor:
    """
    Workflow processor for fictionality analysis operations
    """
    
    def __init__(self):
        self.content_processor = FictionalityContentProcessor()
        self.analyzer = None
        
    async def initialize(self) -> bool:
        """
        Initialize the workflow processor
        
        Returns:
            bool: True if initialization successful
        """
        try:
            self.analyzer = await get_fictionality_analyzer()
            return True
        except Exception as e:
            logger.error("Failed to initialize fictionality workflow processor", error=str(e))
            return False
    
    async def process_single_analysis(
        self,
        request: FictionalityAnalysisRequest,
        options: Optional[FictionalityAnalysisOptions] = None
    ) -> Dict[str, Any]:
        """
        Process single fictionality analysis request
        
        Args:
            request: Analysis request
            options: Analysis options
        
        Returns:
            Dict[str, Any]: Analysis result
        """
        if not options:
            options = FictionalityAnalysisOptions()
        
        try:
            # Generate content hash for caching
            content_hash = await self.content_processor.hash_content(request.content)
            
            # Check if we have cached analysis
            cache_key = f"{self.content_processor.analysis_cache_prefix}{content_hash}"
            cached_analysis = await self._get_cached_analysis(cache_key)
            
            if cached_analysis:
                logger.debug("Returning cached fictionality analysis", content_hash=content_hash)
                return {
                    "success": True,
                    "analysis": cached_analysis,
                    "cached": True,
                    "content_hash": content_hash
                }
            
            # Prepare context
            pr_data = {"id": request.pr_id, "title": f"PR {request.pr_id}"}
            conflict_data = {"id": request.conflict_id, "description": "Conflict analysis"}
            
            context = FictionalityContext(
                pr_data=pr_data,
                conflict_data=conflict_data,
                content_to_analyze=request.content,
                analysis_depth=options.analysis_depth,
                include_strategies=options.include_strategies,
                custom_threshold=options.custom_threshold
            )
            
            # Perform analysis
            result = await self.analyzer.analyze_fictionality(context, cache_key=content_hash)
            
            # Cache the analysis
            if result.success and result.analysis:
                await self._cache_analysis(cache_key, result.analysis)
            
            return {
                "success": result.success,
                "analysis": result.analysis,
                "error": result.error,
                "cached": False,
                "content_hash": content_hash,
                "processing_time": result.processing_time
            }
            
        except Exception as e:
            logger.error("Failed to process fictionality analysis", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "analysis": None,
                "cached": False,
                "content_hash": None
            }
    
    async def process_batch_analysis(
        self,
        requests: List[FictionalityAnalysisRequest],
        max_concurrent: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process batch fictionality analysis requests
        
        Args:
            requests: List of analysis requests
            max_concurrent: Maximum concurrent analyses
        
        Returns:
            Dict[str, Any]: Batch analysis results
        """
        if not max_concurrent:
            max_concurrent = fictionality_settings.fictionality_max_concurrent
        
        if not self.analyzer:
            await self.initialize()
        
        try:
            # Create contexts for batch processing
            contexts = []
            for request in requests:
                context = FictionalityContext(
                    pr_data={"id": request.pr_id},
                    conflict_data={"id": request.conflict_id},
                    content_to_analyze=request.content
                )
                contexts.append(context)
            
            # Perform batch analysis
            results = await self.analyzer.batch_analyze_fictionality(contexts, max_concurrent)
            
            # Process results
            successful_results = []
            failed_results = []
            cached_count = 0
            
            for i, result in enumerate(results):
                if isinstance(result, dict) and result.get("success", False):
                    successful_results.append(result)
                    if result.get("cached", False):
                        cached_count += 1
                else:
                    failed_results.append({
                        "request": requests[i].dict(),
                        "error": result.get("error", "Unknown error") if isinstance(result, dict) else str(result)
                    })
            
            return {
                "success": len(failed_results) == 0,
                "total_requests": len(requests),
                "successful": len(successful_results),
                "failed": len(failed_results),
                "cached": cached_count,
                "results": successful_results,
                "errors": failed_results
            }
            
        except Exception as e:
            logger.error("Failed to process batch fictionality analysis", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "total_requests": len(requests),
                "successful": 0,
                "failed": len(requests),
                "results": [],
                "errors": [{"error": str(e)}]
            }
    
    async def prefetch_analysis(self, content_list: List[str]) -> int:
        """
        Prefetch fictionality analysis for content list
        
        Args:
            content_list: List of content to prefetch
        
        Returns:
            int: Number of analyses prefetched
        """
        if not self.analyzer:
            await self.initialize()
        
        prefetched_count = 0
        
        try:
            for content in content_list:
                content_hash = await self.content_processor.hash_content(content)
                
                # Check if analysis already cached
                cache_key = f"{self.content_processor.analysis_cache_prefix}{content_hash}"
                cached_analysis = await self._get_cached_analysis(cache_key)
                
                if not cached_analysis:
                    # Create dummy context for prefetching
                    context = FictionalityContext(
                        pr_data={"id": "prefetch"},
                        conflict_data={"id": "prefetch"},
                        content_to_analyze=content,
                        analysis_depth="quick"  # Use quick analysis for prefetching
                    )
                    
                    # Perform analysis (fire and forget)
                    result = await self.analyzer.analyze_fictionality(context, cache_key=content_hash)
                    if result.success:
                        prefetched_count += 1
        
        except Exception as e:
            logger.error("Failed to prefetch fictionality analysis", error=str(e))
        
        return prefetched_count
    
    async def clear_fictionality_cache(self, pattern: str = "*") -> int:
        """
        Clear fictionality cache entries
        
        Args:
            pattern: Cache key pattern to clear
        
        Returns:
            int: Number of entries cleared
        """
        try:
            # Clear analysis cache
            analysis_pattern = f"{self.content_processor.analysis_cache_prefix}{pattern}"
            analysis_cleared = await cache_manager.clear_pattern(analysis_pattern)
            
            # Clear content cache
            content_pattern = f"{self.content_cache_prefix}{pattern}"
            content_cleared = await cache_manager.clear_pattern(content_pattern)
            
            # Clear strategy cache
            strategy_pattern = f"{self.strategy_cache_prefix}{pattern}"
            strategy_cleared = await cache_manager.clear_pattern(strategy_pattern)
            
            total_cleared = analysis_cleared + content_cleared + strategy_cleared
            
            logger.info(
                "Fictionality cache cleared",
                total_cleared=total_cleared,
                analysis_cleared=analysis_cleared,
                content_cleared=content_cleared,
                strategy_cleared=strategy_cleared
            )
            
            return total_cleared
            
        except Exception as e:
            logger.error("Failed to clear fictionality cache", error=str(e))
            return 0
    
    async def get_fictionality_cache_stats(self) -> Dict[str, Any]:
        """
        Get fictionality cache statistics
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        try:
            # This would need to be implemented based on the actual cache manager
            # For now, return placeholder statistics
            return {
                "analysis_cache_size": "unknown",
                "content_cache_size": "unknown", 
                "strategy_cache_size": "unknown",
                "hit_rates": {
                    "analysis": 0.75,
                    "content": 0.60,
                    "strategies": 0.45
                },
                "total_entries": "unknown"
            }
        except Exception as e:
            logger.error("Failed to get fictionality cache stats", error=str(e))
            return {"error": str(e)}
    
    async def _get_cached_analysis(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached fictionality analysis
        
        Args:
            cache_key: Cache key
        
        Returns:
            Optional[Dict[str, Any]]: Cached analysis or None
        """
        try:
            return await cache_manager.get(cache_key)
        except Exception as e:
            logger.error("Failed to get cached analysis", error=str(e))
        return None
    
    async def _cache_analysis(self, cache_key: str, analysis: Dict[str, Any]) -> None:
        """
        Cache fictionality analysis
        
        Args:
            cache_key: Cache key
            analysis: Analysis to cache
        """
        try:
            ttl = fictionality_settings.fictionality_cache_ttl
            await cache_manager.set(cache_key, analysis, ttl=ttl)
        except Exception as e:
            logger.error("Failed to cache analysis", error=str(e))


class FictionalityBatchProcessor:
    """
    Specialized batch processor for fictionality analysis
    """
    
    def __init__(self, workflow_processor: FictionalityWorkflowProcessor):
        self.workflow_processor = workflow_processor
        self.batch_stats = {
            "total_batches": 0,
            "total_analyses": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
            "cached_analyses": 0,
            "total_processing_time": 0.0
        }
    
    async def process_large_batch(
        self,
        requests: List[FictionalityAnalysisRequest],
        batch_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process large batch of analyses in smaller chunks
        
        Args:
            requests: List of analysis requests
            batch_size: Size of each chunk
        
        Returns:
            Dict[str, Any]: Batch processing results
        """
        if not batch_size:
            batch_size = fictionality_settings.fictionality_batch_size
        
        all_results = []
        total_start_time = datetime.utcnow()
        
        try:
            # Process in chunks
            for i in range(0, len(requests), batch_size):
                chunk = requests[i:i + batch_size]
                
                logger.info(
                    "Processing fictionality batch chunk",
                    chunk_index=i // batch_size + 1,
                    chunk_size=len(chunk)
                )
                
                # Process chunk
                chunk_result = await self.workflow_processor.process_batch_analysis(chunk)
                all_results.extend(chunk_result.get("results", []))
                
                # Update statistics
                self.batch_stats["total_batches"] += 1
                self.batch_stats["total_analyses"] += len(chunk)
                self.batch_stats["successful_analyses"] += chunk_result.get("successful", 0)
                self.batch_stats["failed_analyses"] += chunk_result.get("failed", 0)
                self.batch_stats["cached_analyses"] += chunk_result.get("cached", 0)
            
            total_processing_time = (datetime.utcnow() - total_start_time).total_seconds()
            self.batch_stats["total_processing_time"] += total_processing_time
            
            return {
                "success": self.batch_stats["failed_analyses"] == 0,
                "total_requests": len(requests),
                "total_batches": self.batch_stats["total_batches"],
                "successful": self.batch_stats["successful_analyses"],
                "failed": self.batch_stats["failed_analyses"],
                "cached": self.batch_stats["cached_analyses"],
                "results": all_results,
                "total_processing_time": total_processing_time,
                "average_time_per_analysis": total_processing_time / max(len(requests), 1)
            }
            
        except Exception as e:
            logger.error("Failed to process large fictionality batch", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "total_requests": len(requests),
                "results": all_results
            }
    
    def get_batch_stats(self) -> Dict[str, Any]:
        """
        Get batch processing statistics
        
        Returns:
            Dict[str, Any]: Batch statistics
        """
        return {
            **self.batch_stats,
            "success_rate": self.batch_stats["successful_analyses"] / max(self.batch_stats["total_analyses"], 1),
            "cache_rate": self.batch_stats["cached_analyses"] / max(self.batch_stats["total_analyses"], 1),
            "average_processing_time": self.batch_stats["total_processing_time"] / max(
                self.batch_stats["total_batches"], 1
            )
        }


# Global instances
content_processor = FictionalityContentProcessor()
workflow_processor = FictionalityWorkflowProcessor()


async def get_fictionality_processor() -> FictionalityWorkflowProcessor:
    """
    Get initialized fictionality workflow processor
    
    Returns:
        FictionalityWorkflowProcessor: Initialized processor
    """
    if not workflow_processor.analyzer:
        await workflow_processor.initialize()
    return workflow_processor


async def get_fictionality_batch_processor() -> FictionalityBatchProcessor:
    """
    Get fictionality batch processor
    
    Returns:
        FictionalityBatchProcessor: Batch processor
    """
    processor = await get_fictionality_processor()
    return FictionalityBatchProcessor(processor)


# Convenience functions
async def analyze_content_fictionality(
    content: str,
    pr_id: str,
    conflict_id: str,
    options: Optional[FictionalityAnalysisOptions] = None
) -> Dict[str, Any]:
    """
    Convenience function to analyze content fictionality
    
    Args:
        content: Content to analyze
        pr_id: Pull request ID
        conflict_id: Conflict ID
        options: Analysis options
    
    Returns:
        Dict[str, Any]: Analysis result
    """
    request = FictionalityAnalysisRequest(
        pr_id=pr_id,
        conflict_id=conflict_id,
        content=content
    )
    
    processor = await get_fictionality_processor()
    return await processor.process_single_analysis(request, options)


async def batch_analyze_fictionality(
    requests: List[FictionalityAnalysisRequest],
    max_concurrent: Optional[int] = None
) -> Dict[str, Any]:
    """
    Convenience function for batch fictionality analysis
    
    Args:
        requests: List of analysis requests
        max_concurrent: Maximum concurrent analyses
    
    Returns:
        Dict[str, Any]: Batch analysis results
    """
    processor = await get_fictionality_processor()
    return await processor.process_batch_analysis(requests, max_concurrent)