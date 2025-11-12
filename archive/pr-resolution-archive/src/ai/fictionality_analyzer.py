"""
Fictionality Analyzer Service for EmailIntelligence

Implements comprehensive fictionality detection using OpenAI with
integrated rate limiting, caching, and circuit breaker patterns.
"""

import asyncio
import json
import time
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from .interfaces import RateLimiter, CircuitBreaker
from ..ai.client import get_openai_client
from ..config.settings import settings
from ..models.fictionality_models import (
    FictionalityAnalysis,
    FictionalityContext,
    FictionalityScore,
    FictionalityAnalysisResult
)
from ..utils.caching import cache_manager

logger = structlog.get_logger()


@dataclass
class FictionalityAnalysisContext:
    """Context for fictionality analysis operations"""
    pr_data: Dict[str, Any]
    conflict_data: Dict[str, Any]
    content_to_analyze: str
    analysis_depth: str = "standard"
    include_strategies: bool = True
    custom_threshold: Optional[float] = None


class FictionalityAnalyzer:
    """
    Fictionality Detection Service
    
    Provides comprehensive fictionality analysis for conflicts and PRs
    using OpenAI with integrated rate limiting, caching, and error handling.
    """
    
    def __init__(self):
        self.client: Optional[Any] = None
        self.rate_limiter = RateLimiter(rate_per_minute=settings.fictionality_rate_limit_rpm)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=settings.fictionality_circuit_breaker_threshold,
            timeout=settings.fictionality_circuit_breaker_timeout
        )
        self.initialized = False
        self.analysis_stats = {
            "analyses_completed": 0,
            "total_processing_time": 0.0,
            "average_confidence": 0.0,
            "cache_hit_rate": 0.0,
            "errors": 0
        }
        self.cache_hits = 0
        self.cache_misses = 0
        self.start_time = datetime.utcnow()
        
    async def initialize(self) -> bool:
        """
        Initialize the fictionality analyzer
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.client = await get_openai_client()
            if not self.client or not self.client.initialized:
                logger.error("Failed to initialize OpenAI client for fictionality analysis")
                return False
                
            self.initialized = True
            logger.info("Fictionality analyzer initialized successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to initialize fictionality analyzer", error=str(e))
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check fictionality analyzer health and status
        
        Returns:
            Dict[str, Any]: Health status information
        """
        try:
            if not self.initialized or not self.client:
                return {
                    "status": "not_initialized",
                    "healthy": False,
                    "error": "Fictionality analyzer not initialized"
                }
            
            # Test with a simple fictionality analysis
            start_time = time.time()
            test_context = FictionalityAnalysisContext(
                pr_data={"id": "health_check", "title": "Test"},
                conflict_data={"id": "health_check", "description": "Test"},
                content_to_analyze="Test content",
                analysis_depth="quick"
            )
            
            test_result = await self._perform_analysis(test_context, force_test=True)
            response_time = time.time() - start_time
            
            healthy = test_result and test_result.get("success", False)
            
            return {
                "status": "healthy" if healthy else "unhealthy",
                "healthy": healthy,
                "response_time": response_time,
                "initialized": self.initialized,
                "request_count": self.analysis_stats["analyses_completed"],
                "error_count": self.analysis_stats["errors"],
                "circuit_breaker_state": self.circuit_breaker.state,
                "cache_hit_rate": self._get_cache_hit_rate(),
                "uptime": (datetime.utcnow() - self.start_time).total_seconds()
            }
            
        except Exception as e:
            logger.error("Fictionality analyzer health check failed", error=str(e))
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "initialized": self.initialized
            }
    
    async def analyze_fictionality(
        self,
        context: FictionalityContext,
        cache_key: Optional[str] = None
    ) -> FictionalityAnalysisResult:
        """
        Perform comprehensive fictionality analysis
        
        Args:
            context: Analysis context with PR, conflict, and content data
            cache_key: Optional cache key for request deduplication
        
        Returns:
            FictionalityAnalysisResult: Analysis result with metadata
        """
        start_time = time.time()
        
        try:
            # Check cache first if cache key provided
            cached_result = None
            if cache_key:
                cached_result = await self._get_cached_analysis(cache_key)
                if cached_result:
                    logger.debug("Returning cached fictionality analysis", cache_key=cache_key)
                    self.cache_hits += 1
                    return FictionalityAnalysisResult(
                        success=True,
                        analysis=cached_result,
                        processing_time=time.time() - start_time,
                        cached=True
                    )
                self.cache_misses += 1
            
            if not self.initialized:
                raise Exception("Fictionality analyzer not initialized")
            
            # Apply circuit breaker check
            if not await self.circuit_breaker.can_attempt():
                logger.warning("Circuit breaker open, skipping fictionality analysis")
                raise Exception("Circuit breaker is open - fictionality analysis unavailable")
            
            # Apply rate limiting
            if not await self.rate_limiter.wait_for_token():
                logger.error("Rate limit exceeded for fictionality analysis")
                raise Exception("Rate limit exceeded for fictionality analysis")
            
            # Convert context to internal format
            internal_context = FictionalityAnalysisContext(
                pr_data=context.pr_data,
                conflict_data=context.conflict_data,
                content_to_analyze=context.content_to_analyze,
                analysis_depth=context.analysis_depth,
                include_strategies=context.include_strategies,
                custom_threshold=context.custom_threshold
            )
            
            # Perform the analysis
            analysis = await self._perform_analysis(internal_context)
            
            # Cache the result if cache key provided
            if cache_key and analysis:
                await self._cache_analysis(cache_key, analysis)
            
            # Update statistics
            self._update_stats(analysis, time.time() - start_time)
            
            # Record success
            await self.circuit_breaker.record_success()
            
            logger.info(
                "Fictionality analysis completed",
                pr_id=context.pr_data.get("id"),
                conflict_id=context.conflict_data.get("id"),
                fictionality_score=analysis.fictionality_score if analysis else 0,
                confidence_level=analysis.confidence_level.value if analysis else "UNKNOWN",
                cached=cached_result is not None
            )
            
            return FictionalityAnalysisResult(
                success=True,
                analysis=analysis,
                processing_time=time.time() - start_time,
                cached=False
            )
            
        except Exception as e:
            self.analysis_stats["errors"] += 1
            await self.circuit_breaker.record_failure()
            
            logger.error(
                "Fictionality analysis failed",
                pr_id=context.pr_data.get("id"),
                error=str(e)
            )
            
            return FictionalityAnalysisResult(
                success=False,
                analysis=None,
                error=str(e),
                processing_time=time.time() - start_time,
                cached=False
            )
    
    async def _perform_analysis(
        self, 
        context: FictionalityAnalysisContext, 
        force_test: bool = False
    ) -> Optional[FictionalityAnalysis]:
        """
        Internal method to perform the actual fictionality analysis
        
        Args:
            context: Analysis context
            force_test: Force test mode (skip cache, etc.)
        
        Returns:
            Optional[FictionalityAnalysis]: Analysis result or None if failed
        """
        try:
            # Generate analysis prompt
            messages = self._create_fictionality_prompt(context)
            
            # Make AI request with existing OpenAI client
            response = await self.client.chat_completion(
                messages=messages,
                temperature=0.1,  # Low temperature for consistent analysis
                max_tokens=1500,
                model="gpt-4"  # Use the most capable model for fictionality detection
            )
            
            # Parse AI response
            analysis_data = self._parse_fictionality_response(response)
            
            # Create FictionalityAnalysis object
            fictionality_analysis = FictionalityAnalysis(
                id=f"fictionality_{int(time.time())}_{hash(context.content_to_analyze) % 10000}",
                conflict_id=context.conflict_data.get("id"),
                pr_id=context.pr_data.get("id"),
                fictionality_score=analysis_data.get("fictionality_score", 0.0),
                confidence_level=self._categorize_confidence(analysis_data.get("fictionality_score", 0.0)),
                text_content=context.content_to_analyze,
                analysis_features=analysis_data.get("features", {}),
                fictionality_indicators=analysis_data.get("fictionality_indicators", []),
                realism_indicators=analysis_data.get("realism_indicators", []),
                model=response.get("model", "unknown"),
                processing_time=response.get("response_time", 0),
                tokens_used=response.get("usage", {}).get("total_tokens", 0),
                reasoning=analysis_data.get("reasoning"),
                resolution_impact=self._assess_resolution_impact(analysis_data),
                strategy_adjustments=self._generate_strategy_adjustments(analysis_data),
                analysis_depth=context.analysis_depth,
                custom_threshold=context.custom_threshold
            )
            
            return fictionality_analysis
            
        except Exception as e:
            if not force_test:  # Only log errors for non-test requests
                logger.error("Failed to perform fictionality analysis", error=str(e))
            
            # Create fallback analysis
            return self._create_fallback_analysis(context, str(e))
    
    def _create_fictionality_prompt(self, context: FictionalityAnalysisContext) -> List[Dict[str, str]]:
        """
        Create fictionality analysis prompt for OpenAI
        
        Args:
            context: Analysis context
        
        Returns:
            List[Dict[str, str]]: OpenAI messages format
        """
        system_prompt = (
            "You are an expert fictionality detection system. Analyze the provided "
            "content to determine how likely it contains fictional or fabricated information.\n\n"
            "Fictionality Indicators:\n"
            "- Inconsistent technical details\n"
            "- Unrealistic timelines or requirements\n"
            "- Overly perfect or idealized scenarios\n"
            "- Generic or template-like language\n"
            "- Lack of specific technical implementation details\n"
            "- Unrealistic performance claims\n"
            "- Vague or ambiguous requirements\n"
            "- Unlikely user behavior or system responses\n\n"
            "Realism Indicators:\n"
            "- Specific technical details and constraints\n"
            "- Real-world implementation challenges mentioned\n"
            "- Realistic timeline estimates\n"
            "- Industry-standard practices referenced\n"
            "- Specific file paths, function names, or technical terms\n"
            "- Acknowledged limitations and trade-offs\n"
            "- Realistic complexity assessments\n"
            "- Evidence of actual testing or usage\n\n"
            "Provide your analysis in JSON format:\n"
            "{\n"
            '  "fictionality_score": 0.0-1.0,  // 0.0 = highly real, 1.0 = highly fictional\n'
            '  "confidence": 0.0-1.0,         // Your confidence in the analysis\n'
            '  "features": {\n'
            '    "technical_consistency": 0.0-1.0,\n'
            '    "realism_of_requirements": 0.0-1.0,\n'
            '    "complexity_appropriateness": 0.0-1.0,\n'
            '    "detail_specificity": 0.0-1.0\n'
            '  },\n'
            '  "fictionality_indicators": ["indicator1", "indicator2"],\n'
            '  "realism_indicators": ["indicator1", "indicator2"],\n'
            '  "reasoning": "Detailed explanation of your analysis",\n'
            '  "resolution_impact": "How this fictionality level affects conflict resolution",\n'
            '  "recommended_strategies": ["strategy1", "strategy2"]\n'
            "}"
        )

        user_prompt = f"""Analyze this content for fictionality:

PR Context: {json.dumps(context.pr_data, indent=2, default=str)}

Conflict Context: {json.dumps(context.conflict_data, indent=2, default=str)}

Content to Analyze: {context.content_to_analyze}

Analysis Depth: {context.analysis_depth}
Include Strategies: {context.include_strategies}
Custom Threshold: {context.custom_threshold}

Focus on identifying whether this content appears to be fictional, speculative, or based on real-world scenarios."""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def _parse_fictionality_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse AI response for fictionality analysis
        
        Args:
            response: OpenAI response
        
        Returns:
            Dict[str, Any]: Parsed analysis data
        """
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract JSON from response
            if content.strip().startswith("{"):
                return json.loads(content)
            else:
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_content = content[start_idx:end_idx]
                    return json.loads(json_content)
                else:
                    raise Exception("No JSON found in fictionality response")
                    
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            logger.error("Failed to parse fictionality response", error=str(e))
            return self._create_default_analysis()
    
    def _categorize_confidence(self, score: float) -> FictionalityScore:
        """
        Categorize fictionality score into confidence levels
        
        Args:
            score: Fictionality score (0.0-1.0)
        
        Returns:
            FictionalityScore: Confidence level
        """
        if score >= 0.8:
            return FictionalityScore.HIGHLY_FICTIONAL
        elif score >= 0.6:
            return FictionalityScore.PROBABLY_FICTIONAL
        elif score >= 0.4:
            return FictionalityScore.UNCERTAIN
        elif score >= 0.2:
            return FictionalityScore.PROBABLY_REAL
        else:
            return FictionalityScore.HIGHLY_REAL
    
    def _assess_resolution_impact(self, analysis_data: Dict[str, Any]) -> str:
        """
        Assess how fictionality affects conflict resolution
        
        Args:
            analysis_data: Analysis data from AI
        
        Returns:
            str: Impact assessment
        """
        score = analysis_data.get("fictionality_score", 0.5)
        
        if score >= 0.8:
            return "HIGH_IMPACT: Require manual validation and more conservative strategies"
        elif score >= 0.6:
            return "MEDIUM_IMPACT: Increase validation steps and reduce automation confidence"
        elif score >= 0.4:
            return "LOW_IMPACT: Standard resolution with enhanced monitoring"
        else:
            return "MINIMAL_IMPACT: Proceed with normal automated resolution"
    
    def _generate_strategy_adjustments(self, analysis_data: Dict[str, Any]) -> List[str]:
        """
        Generate strategy adjustments based on fictionality analysis
        
        Args:
            analysis_data: Analysis data from AI
        
        Returns:
            List[str]: Strategy adjustments
        """
        score = analysis_data.get("fictionality_score", 0.5)
        recommendations = analysis_data.get("recommended_strategies", [])
        
        adjustments = []
        
        if score >= 0.6:
            adjustments.extend([
                "Increase manual review requirements",
                "Reduce confidence threshold by 0.1",
                "Add additional validation steps",
                "Consider more conservative resolution approach"
            ])
        elif score >= 0.4:
            adjustments.extend([
                "Add monitoring for resolution effectiveness",
                "Consider additional testing requirements"
            ])
        
        if recommendations:
            adjustments.extend(recommendations)
        
        return adjustments
    
    def _create_default_analysis(self) -> Dict[str, Any]:
        """
        Create default analysis structure for failed parsing
        
        Returns:
            Dict[str, Any]: Default analysis data
        """
        return {
            "fictionality_score": 0.5,
            "confidence": 0.3,
            "features": {
                "technical_consistency": 0.5,
                "realism_of_requirements": 0.5,
                "complexity_appropriateness": 0.5,
                "detail_specificity": 0.5
            },
            "fictionality_indicators": ["Response parsing failed"],
            "realism_indicators": [],
            "reasoning": "Analysis failed - using default neutral values",
            "resolution_impact": "Unable to assess - requires manual review",
            "recommended_strategies": ["Manual validation required"]
        }
    
    def _create_fallback_analysis(
        self, 
        context: FictionalityAnalysisContext, 
        error: str
    ) -> FictionalityAnalysis:
        """
        Create fallback analysis when AI analysis fails
        
        Args:
            context: Analysis context
            error: Error message
        
        Returns:
            FictionalityAnalysis: Fallback analysis
        """
        return FictionalityAnalysis(
            id=f"fallback_fictionality_{int(time.time())}",
            conflict_id=context.conflict_data.get("id"),
            pr_id=context.pr_data.get("id"),
            fictionality_score=0.5,  # Neutral score for fallback
            confidence_level=FictionalityScore.UNCERTAIN,
            text_content=context.content_to_analyze,
            analysis_features={"fallback": True},
            fictionality_indicators=["Analysis failed - manual review required"],
            realism_indicators=["Fallback analysis"],
            model="fallback",
            processing_time=0.0,
            tokens_used=0,
            reasoning=f"Analysis failed: {error}",
            resolution_impact="Unable to assess due to analysis failure",
            strategy_adjustments=["Manual validation required", "Extended testing recommended"]
        )
    
    async def _get_cached_analysis(self, cache_key: str) -> Optional[FictionalityAnalysis]:
        """
        Get cached fictionality analysis
        
        Args:
            cache_key: Cache key
        
        Returns:
            Optional[FictionalityAnalysis]: Cached analysis or None
        """
        try:
            cached_data = await cache_manager.get(f"fictionality:{cache_key}")
            if cached_data:
                return FictionalityAnalysis(**cached_data)
        except Exception as e:
            logger.error("Failed to get cached fictionality analysis", error=str(e))
        
        return None
    
    async def _cache_analysis(self, cache_key: str, analysis: FictionalityAnalysis) -> None:
        """
        Cache fictionality analysis
        
        Args:
            cache_key: Cache key
            analysis: Analysis to cache
        """
        try:
            await cache_manager.set(
                f"fictionality:{cache_key}",
                analysis.dict(),
                ttl=settings.fictionality_cache_ttl
            )
        except Exception as e:
            logger.error("Failed to cache fictionality analysis", error=str(e))
    
    def _update_stats(self, analysis: FictionalityAnalysis, processing_time: float) -> None:
        """
        Update analysis statistics
        
        Args:
            analysis: Completed analysis
            processing_time: Processing time
        """
        self.analysis_stats["analyses_completed"] += 1
        self.analysis_stats["total_processing_time"] += processing_time
        
        # Update average confidence
        total = self.analysis_stats["analyses_completed"]
        current_avg = self.analysis_stats["average_confidence"]
        self.analysis_stats["average_confidence"] = (
            (current_avg * (total - 1) + analysis.fictionality_score) / total
        )
    
    def _get_cache_hit_rate(self) -> float:
        """
        Calculate cache hit rate
        
        Returns:
            float: Cache hit rate (0.0-1.0)
        """
        total_requests = self.cache_hits + self.cache_misses
        return self.cache_hits / max(total_requests, 1)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get fictionality analysis statistics
        
        Returns:
            Dict[str, Any]: Statistics
        """
        return {
            **self.analysis_stats,
            "cache_hit_rate": self._get_cache_hit_rate(),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "uptime": (datetime.utcnow() - self.start_time).total_seconds(),
            "average_processing_time": (
                self.analysis_stats["total_processing_time"] / 
                max(self.analysis_stats["analyses_completed"], 1)
            )
        }
    
    async def batch_analyze_fictionality(
        self,
        contexts: List[FictionalityContext],
        max_concurrent: int = 3
    ) -> List[FictionalityAnalysisResult]:
        """
        Perform batch fictionality analysis
        
        Args:
            contexts: List of analysis contexts
            max_concurrent: Maximum concurrent analyses
        
        Returns:
            List[FictionalityAnalysisResult]: Analysis results
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_context(context: FictionalityContext) -> FictionalityAnalysisResult:
            async with semaphore:
                return await self.analyze_fictionality(context)
        
        # Process all contexts
        tasks = [process_context(ctx) for ctx in contexts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log batch statistics
        successful = sum(1 for r in results if isinstance(r, FictionalityAnalysisResult) and r.success)
        failed = len(results) - successful
        
        logger.info(
            "Batch fictionality analysis completed",
            total=len(contexts),
            successful=successful,
            failed=failed
        )
        
        return results


# Global fictionality analyzer instance
fictionality_analyzer = FictionalityAnalyzer()


async def get_fictionality_analyzer() -> FictionalityAnalyzer:
    """
    Get initialized fictionality analyzer
    
    Returns:
        FictionalityAnalyzer: Initialized analyzer
    """
    if not fictionality_analyzer.initialized:
        await fictionality_analyzer.initialize()
    return fictionality_analyzer