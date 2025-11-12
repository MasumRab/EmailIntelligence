"""
Fictionality Resolvers for GraphQL API
Implements comprehensive fictionality analysis resolvers with batch processing,
filtering, and analytics capabilities.
"""

import asyncio
import time
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

from .schema import (
    FictionalityAnalysisType,
    FictionalityMetricsType,
    FictionalitySummaryType,
    FictionalityHealthReportType,
    FictionalityAnalysisRequestType,
    FictionalityAnalysisOptionsType,
    FictionalityFilterType,
    FictionalityAnalyticsType,
    FictionalityTrendType,
    FictionalityFilterResultType
)

# ARCHIVED: PR Resolution System - AI service imports moved to archive
# from ..ai.fictionality_analyzer import get_fictionality_analyzer  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/
from ..database.data_access import fictionality_dao, pr_dao, conflict_dao
from ..models.fictionality_models import (
    FictionalityContext,
    FictionalityScore,
    FictionalityAnalysis,
    FictionalityMetrics,
    FictionalitySummary,
    FictionalityHealthReport,
    BatchFictionalityAnalysisRequest
)

logger = structlog.get_logger()


class FictionalityResolvers:
    """Fictionality-related GraphQL resolvers"""
    
    # Query Resolvers
    
    @staticmethod
    async def resolve_fictionality_analysis(root, info, id):
        """Resolver for getting a single fictionality analysis by ID"""
        start_time = time.time()
        try:
            # Get from database
            analysis = await fictionality_dao.get_analysis(id)
            
            if not analysis:
                logger.warning("Fictionality analysis not found", analysis_id=id)
                return None
            
            logger.info(
                "Fictionality analysis resolved", 
                analysis_id=id,
                fictionality_score=analysis.fictionality_score,
                confidence_level=analysis.confidence_level.value,
                duration=time.time() - start_time
            )
            
            # Convert to GraphQL type
            return FictionalityAnalysisType(
                id=analysis.id,
                conflict_id=analysis.conflict_id,
                pr_id=analysis.pr_id,
                fictionality_score=analysis.fictionality_score,
                confidence_level=analysis.confidence_level,
                text_content=analysis.text_content,
                analysis_features=json.dumps(analysis.analysis_features),
                fictionality_indicators=analysis.fictionality_indicators,
                realism_indicators=analysis.realism_indicators,
                model=analysis.model,
                processing_time=analysis.processing_time,
                tokens_used=analysis.tokens_used,
                reasoning=analysis.reasoning,
                resolution_impact=analysis.resolution_impact,
                strategy_adjustments=analysis.strategy_adjustments,
                analysis_depth=analysis.analysis_depth,
                custom_threshold=analysis.custom_threshold,
                created_at=analysis.created_at,
                updated_at=analysis.updated_at
            )
            
        except Exception as e:
            logger.error("Failed to resolve fictionality analysis", analysis_id=id, error=str(e))
            return None
    
    @staticmethod
    async def resolve_fictionality_analyses(
        root, info, 
        conflict_id=None, pr_id=None, min_score=None, max_score=None, 
        confidence=None, limit=50, offset=0
    ):
        """Resolver for getting fictionality analyses with filtering"""
        start_time = time.time()
        try:
            # Build filters
            filters = {}
            if conflict_id:
                filters['conflict_id'] = conflict_id
            if pr_id:
                filters['pr_id'] = pr_id
            if min_score is not None:
                filters['min_score'] = min_score
            if max_score is not None:
                filters['max_score'] = max_score
            if confidence:
                filters['confidence'] = confidence
            
            # Get from database
            analyses = await fictionality_dao.get_analyses(
                filters=filters,
                limit=limit,
                offset=offset
            )
            
            # Convert to GraphQL types
            result = []
            for analysis in analyses:
                result.append(FictionalityAnalysisType(
                    id=analysis.id,
                    conflict_id=analysis.conflict_id,
                    pr_id=analysis.pr_id,
                    fictionality_score=analysis.fictionality_score,
                    confidence_level=analysis.confidence_level,
                    text_content=analysis.text_content,
                    analysis_features=json.dumps(analysis.analysis_features),
                    fictionality_indicators=analysis.fictionality_indicators,
                    realism_indicators=analysis.realism_indicators,
                    model=analysis.model,
                    processing_time=analysis.processing_time,
                    tokens_used=analysis.tokens_used,
                    reasoning=analysis.reasoning,
                    resolution_impact=analysis.resolution_impact,
                    strategy_adjustments=analysis.strategy_adjustments,
                    analysis_depth=analysis.analysis_depth,
                    custom_threshold=analysis.custom_threshold,
                    created_at=analysis.created_at,
                    updated_at=analysis.updated_at
                ))
            
            logger.info(
                "Fictionality analyses resolved", 
                count=len(result),
                filters=filters,
                duration=time.time() - start_time
            )
            
            return result
            
        except Exception as e:
            logger.error("Failed to resolve fictionality analyses", filters=locals(), error=str(e))
            return []
    
    @staticmethod
    async def resolve_fictionality_metrics(root, info, pr_id=None, period="7d"):
        """Resolver for getting fictionality metrics"""
        start_time = time.time()
        try:
            # Calculate period
            end_time = datetime.utcnow()
            if period == "1d":
                start_time = end_time - timedelta(days=1)
            elif period == "7d":
                start_time = end_time - timedelta(days=7)
            elif period == "30d":
                start_time = end_time - timedelta(days=30)
            else:
                start_time = end_time - timedelta(days=7)  # Default to 7 days
            
            # Get metrics from database
            metrics = await fictionality_dao.get_metrics(
                start_time=start_time,
                end_time=end_time,
                pr_id=pr_id
            )
            
            logger.info(
                "Fictionality metrics resolved", 
                pr_id=pr_id,
                period=period,
                total_analyses=metrics.total_analyses,
                duration=time.time() - start_time
            )
            
            return FictionalityMetricsType(
                total_analyses=metrics.total_analyses,
                high_fictionality_count=metrics.high_fictionality_count,
                uncertain_count=metrics.uncertain_count,
                low_fictionality_count=metrics.low_fictionality_count,
                average_score=metrics.average_score,
                average_processing_time=metrics.average_processing_time,
                cache_hit_rate=metrics.cache_hit_rate,
                fictionality_distribution=json.dumps(metrics.fictionality_distribution)
            )
            
        except Exception as e:
            logger.error("Failed to resolve fictionality metrics", pr_id=pr_id, period=period, error=str(e))
            return FictionalityMetricsType(
                total_analyses=0,
                high_fictionality_count=0,
                uncertain_count=0,
                low_fictionality_count=0,
                average_score=0.0,
                average_processing_time=0.0,
                cache_hit_rate=0.0,
                fictionality_distribution={}
            )
    
    @staticmethod
    async def resolve_fictionality_summary(root, info, pr_id=None):
        """Resolver for getting fictionality summary"""
        start_time = time.time()
        try:
            # Get summary from database
            summary_data = await fictionality_dao.get_summary(pr_id=pr_id)
            
            # Convert recent analyses
            recent_analyses = []
            for analysis in summary_data.recent_analyses:
                recent_analyses.append(FictionalityAnalysisType(
                    id=analysis.id,
                    conflict_id=analysis.conflict_id,
                    pr_id=analysis.pr_id,
                    fictionality_score=analysis.fictionality_score,
                    confidence_level=analysis.confidence_level,
                    text_content=analysis.text_content,
                    analysis_features=json.dumps(analysis.analysis_features),
                    fictionality_indicators=analysis.fictionality_indicators,
                    realism_indicators=analysis.realism_indicators,
                    model=analysis.model,
                    processing_time=analysis.processing_time,
                    tokens_used=analysis.tokens_used,
                    reasoning=analysis.reasoning,
                    resolution_impact=analysis.resolution_impact,
                    strategy_adjustments=analysis.strategy_adjustments,
                    analysis_depth=analysis.analysis_depth,
                    custom_threshold=analysis.custom_threshold,
                    created_at=analysis.created_at,
                    updated_at=analysis.updated_at
                ))
            
            logger.info(
                "Fictionality summary resolved", 
                pr_id=pr_id,
                total_analyses=summary_data.total_analyses,
                duration=time.time() - start_time
            )
            
            return FictionalitySummaryType(
                total_analyses=summary_data.total_analyses,
                high_fictionality_count=summary_data.high_fictionality_count,
                uncertain_count=summary_data.uncertain_count,
                low_fictionality_count=summary_data.low_fictionality_count,
                average_score=summary_data.average_score,
                recent_analyses=recent_analyses,
                trends=json.dumps(summary_data.trends)
            )
            
        except Exception as e:
            logger.error("Failed to resolve fictionality summary", pr_id=pr_id, error=str(e))
            return FictionalitySummaryType(
                total_analyses=0,
                high_fictionality_count=0,
                uncertain_count=0,
                low_fictionality_count=0,
                average_score=0.0,
                recent_analyses=[],
                trends=[]
            )
    
    @staticmethod
    async def resolve_fictionality_trends(root, info, period="30d"):
        """Resolver for getting fictionality trends"""
        start_time = time.time()
        try:
            # Calculate period
            end_time = datetime.utcnow()
            if period == "7d":
                start_time = end_time - timedelta(days=7)
            elif period == "30d":
                start_time = end_time - timedelta(days=30)
            elif period == "90d":
                start_time = end_time - timedelta(days=90)
            else:
                start_time = end_time - timedelta(days=30)  # Default to 30 days
            
            # Get trend data from database
            trends = await fictionality_dao.get_trends(
                start_time=start_time,
                end_time=end_time
            )
            
            # Convert to GraphQL trend points
            result = []
            for trend in trends:
                result.append(TrendPointType(
                    timestamp=trend['timestamp'],
                    value=trend['value'],
                    label=trend['label']
                ))
            
            logger.info(
                "Fictionality trends resolved", 
                period=period,
                count=len(result),
                duration=time.time() - start_time
            )
            
            return result
            
        except Exception as e:
            logger.error("Failed to resolve fictionality trends", period=period, error=str(e))
            return []
    
    @staticmethod
    async def resolve_fictionality_health_report(root, info):
        """Resolver for getting fictionality health report"""
        start_time = time.time()
        try:
            # Get analyzer instance
            analyzer = await get_fictionality_analyzer()
            
            # Get health check
            health = await analyzer.health_check()
            
            # Get current metrics
            stats = analyzer.get_stats()
            metrics_data = await fictionality_dao.get_metrics(
                start_time=datetime.utcnow() - timedelta(days=1),
                end_time=datetime.utcnow()
            )
            
            # Create metrics type
            metrics = FictionalityMetricsType(
                total_analyses=metrics_data.total_analyses,
                high_fictionality_count=metrics_data.high_fictionality_count,
                uncertain_count=metrics_data.uncertain_count,
                low_fictionality_count=metrics_data.low_fictionality_count,
                average_score=metrics_data.average_score,
                average_processing_time=metrics_data.average_processing_time,
                cache_hit_rate=stats.get('cache_hit_rate', 0.0),
                fictionality_distribution=json.dumps(metrics_data.fictionality_distribution)
            )
            
            logger.info(
                "Fictionality health report resolved", 
                status=health.get('status'),
                healthy=health.get('healthy', False),
                duration=time.time() - start_time
            )
            
            return FictionalityHealthReportType(
                status=health.get('status', 'unknown'),
                healthy=health.get('healthy', False),
                services=json.dumps(health),
                timestamp=datetime.utcnow(),
                uptime=health.get('uptime', 0.0),
                metrics=metrics
            )
            
        except Exception as e:
            logger.error("Failed to resolve fictionality health report", error=str(e))
            return FictionalityHealthReportType(
                status="error",
                healthy=False,
                services=json.dumps({"error": str(e)}),
                timestamp=datetime.utcnow(),
                uptime=0.0,
                metrics=FictionalityMetricsType(
                    total_analyses=0,
                    high_fictionality_count=0,
                    uncertain_count=0,
                    low_fictionality_count=0,
                    average_score=0.0,
                    average_processing_time=0.0,
                    cache_hit_rate=0.0,
                    fictionality_distribution={}
                )
            )
    
    @staticmethod
    async def resolve_fictionality_analytics(root, info, pr_id=None, period="30d"):
        """Resolver for getting fictionality analytics"""
        start_time = time.time()
        try:
            # Calculate period
            end_time = datetime.utcnow()
            if period == "7d":
                start_time = end_time - timedelta(days=7)
            elif period == "30d":
                start_time = end_time - timedelta(days=30)
            elif period == "90d":
                start_time = end_time - timedelta(days=90)
            else:
                start_time = end_time - timedelta(days=30)  # Default to 30 days
            
            # Get analytics data
            analytics_data = await fictionality_dao.get_analytics(
                start_time=start_time,
                end_time=end_time,
                pr_id=pr_id
            )
            
            logger.info(
                "Fictionality analytics resolved", 
                pr_id=pr_id,
                period=period,
                duration=time.time() - start_time
            )
            
            return FictionalityAnalyticsType(
                total_analyses=analytics_data.get('total_analyses', 0),
                average_fictionality_score=analytics_data.get('average_fictionality_score', 0.0),
                high_fictionality_percentage=analytics_data.get('high_fictionality_percentage', 0.0),
                low_fictionality_percentage=analytics_data.get('low_fictionality_percentage', 0.0),
                trend_direction=analytics_data.get('trend_direction', 'stable'),
                top_fictionality_indicators=analytics_data.get('top_fictionality_indicators', []),
                analysis_distribution=json.dumps(analytics_data.get('analysis_distribution', {})),
                performance_metrics=json.dumps(analytics_data.get('performance_metrics', {}))
            )
            
        except Exception as e:
            logger.error("Failed to resolve fictionality analytics", pr_id=pr_id, period=period, error=str(e))
            return FictionalityAnalyticsType(
                total_analyses=0,
                average_fictionality_score=0.0,
                high_fictionality_percentage=0.0,
                low_fictionality_percentage=0.0,
                trend_direction='stable',
                top_fictionality_indicators=[],
                analysis_distribution={},
                performance_metrics={}
            )
    
    @staticmethod
    async def resolve_fictionality_filter_conflicts(root, info, **kwargs):
        """Resolver for filtering conflicts by fictionality criteria"""
        start_time = time.time()
        try:
            # Extract filter parameters
            min_score = kwargs.get('min_score')
            max_score = kwargs.get('max_score')
            confidence_levels = kwargs.get('confidence_levels', [])
            include_indicators = kwargs.get('include_indicators', [])
            exclude_indicators = kwargs.get('exclude_indicators', [])
            pr_id = kwargs.get('pr_id')
            limit = kwargs.get('limit', 50)
            offset = kwargs.get('offset', 0)
            
            # Get filtered conflicts
            conflicts = await fictionality_dao.filter_conflicts_by_fictionality(
                min_score=min_score,
                max_score=max_score,
                confidence_levels=confidence_levels,
                include_indicators=include_indicators,
                exclude_indicators=exclude_indicators,
                pr_id=pr_id,
                limit=limit,
                offset=offset
            )
            
            # Convert to GraphQL types
            result = []
            for conflict in conflicts:
                # Get associated fictionality analysis if available
                fictionality_analysis = None
                if conflict.get('fictionality_analysis_id'):
                    analysis = await fictionality_dao.get_analysis(conflict['fictionality_analysis_id'])
                    if analysis:
                        fictionality_analysis = FictionalityAnalysisType(
                            id=analysis.id,
                            conflict_id=analysis.conflict_id,
                            pr_id=analysis.pr_id,
                            fictionality_score=analysis.fictionality_score,
                            confidence_level=analysis.confidence_level,
                            text_content=analysis.text_content,
                            analysis_features=json.dumps(analysis.analysis_features),
                            fictionality_indicators=analysis.fictionality_indicators,
                            realism_indicators=analysis.realism_indicators,
                            model=analysis.model,
                            processing_time=analysis.processing_time,
                            tokens_used=analysis.tokens_used,
                            reasoning=analysis.reasoning,
                            resolution_impact=analysis.resolution_impact,
                            strategy_adjustments=analysis.strategy_adjustments,
                            analysis_depth=analysis.analysis_depth,
                            custom_threshold=analysis.custom_threshold,
                            created_at=analysis.created_at,
                            updated_at=analysis.updated_at
                        )
                
                result.append(ConflictWithFictionalityType(
                    id=conflict['id'],
                    type=conflict['type'],
                    severity=conflict['severity'],
                    description=conflict['description'],
                    affected_files=conflict.get('affected_files', []),
                    fictionality_analysis_id=conflict.get('fictionality_analysis_id'),
                    fictionality_score=conflict.get('fictionality_score'),
                    fictionality_indicators=conflict.get('fictionality_indicators', []),
                    fictionality_confidence=conflict.get('fictionality_confidence'),
                    fictionality_analysis=fictionality_analysis
                ))
            
            logger.info(
                "Conflicts filtered by fictionality criteria", 
                count=len(result),
                filters=kwargs,
                duration=time.time() - start_time
            )
            
            return FictionalityFilterResultType(
                conflicts=result,
                total_count=len(result),
                filters_applied=json.dumps(kwargs)
            )
            
        except Exception as e:
            logger.error("Failed to filter conflicts by fictionality", filters=kwargs, error=str(e))
            return FictionalityFilterResultType(
                conflicts=[],
                total_count=0,
                filters_applied=json.dumps(kwargs)
            )
    
    # Mutation Resolvers
    
    @staticmethod
    async def resolve_analyze_fictionality(
        root, info, 
        pr_id, conflict_id, content, analysis_options=None
    ):
        """Resolver for analyzing fictionality of content"""
        start_time = time.time()
        try:
            # Get analyzer instance
            analyzer = await get_fictionality_analyzer()
            
            # Get PR and conflict data
            pr_data = await pr_dao.get_pr(pr_id)
            conflict_data = await conflict_dao.get_conflict(conflict_id)
            
            if not pr_data or not conflict_data:
                raise Exception(f"PR {pr_id} or conflict {conflict_id} not found")
            
            # Create analysis context
            context = FictionalityContext(
                pr_data=pr_data.dict() if hasattr(pr_data, 'dict') else pr_data,
                conflict_data=conflict_data.dict() if hasattr(conflict_data, 'dict') else conflict_data,
                content_to_analyze=content,
                analysis_depth=analysis_options.analysis_depth if analysis_options else "standard",
                include_strategies=analysis_options.include_strategies if analysis_options else True,
                custom_threshold=analysis_options.custom_threshold if analysis_options else None
            )
            
            # Perform analysis
            cache_key = f"fictionality:{pr_id}:{conflict_id}:{hash(content)}"
            result = await analyzer.analyze_fictionality(context, cache_key=cache_key)
            
            if not result.success:
                raise Exception(result.error or "Analysis failed")
            
            analysis = result.analysis
            
            # Save to database
            await fictionality_dao.save_analysis(analysis)
            
            logger.info(
                "Fictionality analysis completed", 
                pr_id=pr_id,
                conflict_id=conflict_id,
                fictionality_score=analysis.fictionality_score,
                confidence_level=analysis.confidence_level.value,
                cached=result.cached,
                duration=time.time() - start_time
            )
            
            # Convert to GraphQL type
            return FictionalityAnalysisType(
                id=analysis.id,
                conflict_id=analysis.conflict_id,
                pr_id=analysis.pr_id,
                fictionality_score=analysis.fictionality_score,
                confidence_level=analysis.confidence_level,
                text_content=analysis.text_content,
                analysis_features=json.dumps(analysis.analysis_features),
                fictionality_indicators=analysis.fictionality_indicators,
                realism_indicators=analysis.realism_indicators,
                model=analysis.model,
                processing_time=analysis.processing_time,
                tokens_used=analysis.tokens_used,
                reasoning=analysis.reasoning,
                resolution_impact=analysis.resolution_impact,
                strategy_adjustments=analysis.strategy_adjustments,
                analysis_depth=analysis.analysis_depth,
                custom_threshold=analysis.custom_threshold,
                created_at=analysis.created_at,
                updated_at=analysis.updated_at
            )
            
        except Exception as e:
            logger.error(
                "Failed to analyze fictionality", 
                pr_id=pr_id, 
                conflict_id=conflict_id, 
                error=str(e)
            )
            raise
    
    @staticmethod
    async def resolve_batch_analyze_fictionality(
        root, info, 
        requests, max_concurrent=3
    ):
        """Resolver for batch analyzing fictionality"""
        start_time = time.time()
        try:
            # Get analyzer instance
            analyzer = await get_fictionality_analyzer()
            
            # Create contexts for all requests
            contexts = []
            for request in requests:
                # Get PR and conflict data
                pr_data = await pr_dao.get_pr(request.pr_id)
                conflict_data = await conflict_dao.get_conflict(request.conflict_id)
                
                if not pr_data or not conflict_data:
                    logger.warning(
                        "PR or conflict not found for batch analysis", 
                        pr_id=request.pr_id, 
                        conflict_id=request.conflict_id
                    )
                    continue
                
                context = FictionalityContext(
                    pr_data=pr_data.dict() if hasattr(pr_data, 'dict') else pr_data,
                    conflict_data=conflict_data.dict() if hasattr(conflict_data, 'dict') else conflict_data,
                    content_to_analyze=request.content,
                    analysis_depth=request.analysis_type or "standard"
                )
                contexts.append((request, context))
            
            # Process in batches
            results = []
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def process_single_analysis(request_context):
                async with semaphore:
                    request, context = request_context
                    try:
                        cache_key = f"batch_fictionality:{request.pr_id}:{request.conflict_id}:{hash(request.content)}"
                        result = await analyzer.analyze_fictionality(context, cache_key=cache_key)
                        
                        if result.success:
                            # Save to database
                            await fictionality_dao.save_analysis(result.analysis)
                            
                            # Convert to GraphQL type
                            analysis = result.analysis
                            return FictionalityAnalysisType(
                                id=analysis.id,
                                conflict_id=analysis.conflict_id,
                                pr_id=analysis.pr_id,
                                fictionality_score=analysis.fictionality_score,
                                confidence_level=analysis.confidence_level,
                                text_content=analysis.text_content,
                                analysis_features=json.dumps(analysis.analysis_features),
                                fictionality_indicators=analysis.fictionality_indicators,
                                realism_indicators=analysis.realism_indicators,
                                model=analysis.model,
                                processing_time=analysis.processing_time,
                                tokens_used=analysis.tokens_used,
                                reasoning=analysis.reasoning,
                                resolution_impact=analysis.resolution_impact,
                                strategy_adjustments=analysis.strategy_adjustments,
                                analysis_depth=analysis.analysis_depth,
                                custom_threshold=analysis.custom_threshold,
                                created_at=analysis.created_at,
                                updated_at=analysis.updated_at
                            )
                        else:
                            logger.error(
                                "Batch analysis failed", 
                                pr_id=request.pr_id, 
                                conflict_id=request.conflict_id, 
                                error=result.error
                            )
                            return None
                            
                    except Exception as e:
                        logger.error(
                            "Batch analysis error", 
                            pr_id=request.pr_id, 
                            conflict_id=request.conflict_id, 
                            error=str(e)
                        )
                        return None
            
            # Process all contexts
            tasks = [process_single_analysis(ctx) for ctx in contexts]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out None results and exceptions
            successful_results = [
                r for r in results 
                if r is not None and not isinstance(r, Exception)
            ]
            
            total_time = time.time() - start_time
            logger.info(
                "Batch fictionality analysis completed", 
                total_requests=len(requests),
                successful=len(successful_results),
                failed=len(requests) - len(successful_results),
                duration=total_time
            )
            
            return successful_results
            
        except Exception as e:
            logger.error("Failed to batch analyze fictionality", error=str(e))
            raise
    
    @staticmethod
    async def resolve_update_fictionality_settings(
        root, info, 
        sensitivity=None, cache_ttl=None, custom_prompts=None
    ):
        """Resolver for updating fictionality settings"""
        start_time = time.time()
        try:
            # Update settings in database
            settings_updated = await fictionality_dao.update_settings(
                sensitivity=sensitivity,
                cache_ttl=cache_ttl,
                custom_prompts=custom_prompts
            )
            
            # If settings are stored in config, update them there too
            if settings_updated:
                from ..config.fictionality_settings import fictionality_settings
                
                if sensitivity is not None:
                    fictionality_settings.sensitivity = sensitivity
                if cache_ttl is not None:
                    fictionality_settings.cache_ttl = cache_ttl
                if custom_prompts is not None:
                    fictionality_settings.custom_prompts = custom_prompts
            
            logger.info(
                "Fictionality settings updated", 
                sensitivity=sensitivity,
                cache_ttl=cache_ttl,
                custom_prompts=custom_prompts,
                duration=time.time() - start_time
            )
            
            return settings_updated
            
        except Exception as e:
            logger.error("Failed to update fictionality settings", error=str(e))
            return False
    
    @staticmethod
    async def resolve_clear_fictionality_cache(root, info, pattern=None):
        """Resolver for clearing fictionality cache"""
        start_time = time.time()
        try:
            # Clear cache through analyzer
            analyzer = await get_fictionality_analyzer()
            cleared_count = await analyzer.clear_cache(pattern=pattern)
            
            logger.info(
                "Fictionality cache cleared", 
                pattern=pattern,
                cleared_entries=cleared_count,
                duration=time.time() - start_time
            )
            
            return cleared_count
            
        except Exception as e:
            logger.error("Failed to clear fictionality cache", pattern=pattern, error=str(e))
            return 0
    
    @staticmethod
    async def resolve_prefetch_fictionality_analysis(root, info, pr_id):
        """Resolver for prefetching fictionality analysis for all conflicts in a PR"""
        start_time = time.time()
        try:
            # Get all conflicts for the PR
            conflicts = await pr_dao.get_pr_conflicts(pr_id)
            
            if not conflicts:
                logger.info("No conflicts found for prefetch", pr_id=pr_id)
                return True
            
            # Get analyzer instance
            analyzer = await get_fictionality_analyzer()
            
            # Get PR data
            pr_data = await pr_dao.get_pr(pr_id)
            if not pr_data:
                raise Exception(f"PR {pr_id} not found")
            
            # Create analysis requests for all conflicts
            requests = []
            for conflict in conflicts:
                # Generate content to analyze (conflict description, etc.)
                content = f"""
                PR Title: {pr_data.get('title', '') if isinstance(pr_data, dict) else pr_data.title}
                Conflict Description: {conflict.get('description', '') if isinstance(conflict, dict) else conflict.description}
                Conflict Type: {conflict.get('type', '') if isinstance(conflict, dict) else conflict.type}
                Affected Files: {', '.join(conflict.get('affected_files', []) if isinstance(conflict, dict) else getattr(conflict, 'affected_files', []))}
                """
                
                request = FictionalityAnalysisRequestType(
                    pr_id=pr_id,
                    conflict_id=conflict.id if hasattr(conflict, 'id') else conflict.get('id'),
                    content=content,
                    analysis_type="standard"
                )
                requests.append(request)
            
            # Run batch analysis
            results = await FictionalityResolvers.resolve_batch_analyze_fictionality(
                None, None, requests, max_concurrent=2
            )
            
            successful = len([r for r in results if r is not None])
            
            logger.info(
                "Fictionality analysis prefetch completed", 
                pr_id=pr_id,
                total_conflicts=len(conflicts),
                successful_analyses=successful,
                duration=time.time() - start_time
            )
            
            return True
            
        except Exception as e:
            logger.error("Failed to prefetch fictionality analysis", pr_id=pr_id, error=str(e))
            return False


# Import the missing types we need
from .schema import ConflictWithFictionalityType, FictionalityAnalyticsType, TrendPointType

# Apply resolvers to Query and Mutation classes
def apply_fictionality_resolvers():
    """Apply all fictionality resolvers to Query and Mutation classes"""
    from .schema import Query, Mutation
    
    # Query resolvers
    Query.resolve_fictionality_analysis = FictionalityResolvers.resolve_fictionality_analysis
    Query.resolve_fictionality_analyses = FictionalityResolvers.resolve_fictionality_analyses
    Query.resolve_fictionality_metrics = FictionalityResolvers.resolve_fictionality_metrics
    Query.resolve_fictionality_summary = FictionalityResolvers.resolve_fictionality_summary
    Query.resolve_fictionality_trends = FictionalityResolvers.resolve_fictionality_trends
    Query.resolve_fictionality_health_report = FictionalityResolvers.resolve_fictionality_health_report
    Query.resolve_fictionality_analytics = FictionalityResolvers.resolve_fictionality_analytics
    Query.resolve_fictionality_filter_conflicts = FictionalityResolvers.resolve_fictionality_filter_conflicts
    
    # Mutation resolvers
    Mutation.resolve_analyze_fictionality = FictionalityResolvers.resolve_analyze_fictionality
    Mutation.resolve_batch_analyze_fictionality = FictionalityResolvers.resolve_batch_analyze_fictionality
    Mutation.resolve_update_fictionality_settings = FictionalityResolvers.resolve_update_fictionality_settings
    Mutation.resolve_clear_fictionality_cache = FictionalityResolvers.resolve_clear_fictionality_cache
    Mutation.resolve_prefetch_fictionality_analysis = FictionalityResolvers.resolve_prefetch_fictionality_analysis
    
    logger.info("Fictionality resolvers applied to GraphQL schema")


# Apply resolvers when module is imported
apply_fictionality_resolvers()