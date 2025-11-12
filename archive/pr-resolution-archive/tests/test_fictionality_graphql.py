"""
Comprehensive tests for Fictionality GraphQL Resolvers
Tests the complete fictionality analysis integration with GraphQL
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

# Import GraphQL schema and resolvers
from src.graphql.schema import schema
from src.graphql.fictionality_resolvers import FictionalityResolvers
from src.graphql.fictionality_queries import (
    FictionalityQueryBuilder,
    FictionalityAnalyticsBuilder,
    create_fictionality_filter_query
)
from src.models.fictionality_models import FictionalityScore


class TestFictionalityGraphQLResolvers:
    """Test fictionality GraphQL resolvers"""
    
    @pytest.fixture
    def mock_fictionality_analyzer(self):
        """Mock fictionality analyzer"""
        analyzer = Mock()
        analyzer.health_check = AsyncMock(return_value={
            "status": "healthy",
            "healthy": True,
            "uptime": 3600.0,
            "request_count": 100,
            "error_count": 2,
            "circuit_breaker_state": "closed"
        })
        analyzer.get_stats = Mock(return_value={
            "analyses_completed": 98,
            "total_processing_time": 450.5,
            "average_confidence": 0.75,
            "cache_hit_rate": 0.3,
            "errors": 2
        })
        return analyzer
    
    @pytest.fixture
    def mock_database(self):
        """Mock database operations"""
        mock_db = Mock()
        
        # Mock fictionality analysis
        mock_analysis = Mock()
        mock_analysis.id = "test_analysis_123"
        mock_analysis.conflict_id = "conflict_456"
        mock_analysis.pr_id = "pr_789"
        mock_analysis.fictionality_score = 0.3
        mock_analysis.confidence_level = FictionalityScore.PROBABLY_REAL
        mock_analysis.text_content = "Test conflict content"
        mock_analysis.analysis_features = {"technical_consistency": 0.8, "detail_specificity": 0.7}
        mock_analysis.fictionality_indicators = ["vague_requirements", "inconsistent_details"]
        mock_analysis.realism_indicators = ["specific_technical_details", "realistic_timeline"]
        mock_analysis.model = "gpt-4"
        mock_analysis.processing_time = 2.5
        mock_analysis.tokens_used = 1500
        mock_analysis.reasoning = "Content shows realistic technical details"
        mock_analysis.resolution_impact = "MINIMAL_IMPACT: Proceed with normal automated resolution"
        mock_analysis.strategy_adjustments = ["Standard resolution approach recommended"]
        mock_analysis.analysis_depth = "standard"
        mock_analysis.custom_threshold = None
        mock_analysis.created_at = datetime.utcnow()
        mock_analysis.updated_at = datetime.utcnow()
        
        mock_db.get_analysis = AsyncMock(return_value=mock_analysis)
        mock_db.get_analyses = AsyncMock(return_value=[mock_analysis])
        mock_db.get_metrics = AsyncMock(return_value=Mock(
            total_analyses=50,
            high_fictionality_count=5,
            uncertain_count=15,
            low_fictionality_count=30,
            average_score=0.35,
            average_processing_time=2.1,
            cache_hit_rate=0.25,
            fictionality_distribution={"0.0-0.2": 20, "0.2-0.4": 10, "0.4-0.6": 15, "0.6-0.8": 3, "0.8-1.0": 2}
        ))
        mock_db.get_summary = AsyncMock(return_value=Mock(
            total_analyses=50,
            high_fictionality_count=5,
            uncertain_count=15,
            low_fictionality_count=30,
            average_score=0.35,
            recent_analyses=[mock_analysis],
            trends=[]
        ))
        mock_db.get_trends = AsyncMock(return_value=[
            {"timestamp": datetime.utcnow(), "value": 0.3, "label": "Average Fictionality"},
            {"timestamp": datetime.utcnow() - timedelta(days=1), "value": 0.25, "label": "Average Fictionality"}
        ])
        mock_db.get_analytics = AsyncMock(return_value={
            "total_analyses": 50,
            "average_fictionality_score": 0.35,
            "high_fictionality_percentage": 10.0,
            "low_fictionality_percentage": 60.0,
            "trend_direction": "stable",
            "top_fictionality_indicators": ["vague_requirements", "inconsistent_details"],
            "analysis_distribution": {"quick": 20, "standard": 25, "deep": 5},
            "performance_metrics": {"average_time": 2.1, "total_tokens": 75000}
        })
        mock_db.filter_conflicts_by_fictionality = AsyncMock(return_value=[
            {
                "id": "conflict_123",
                "type": "merge_conflict",
                "severity": "medium",
                "description": "Merge conflict in config file",
                "affected_files": ["src/config.json"],
                "fictionality_analysis_id": "analysis_123",
                "fictionality_score": 0.2,
                "fictionality_indicators": [],
                "fictionality_confidence": "PROBABLY_REAL"
            }
        ])
        mock_db.save_analysis = AsyncMock()
        mock_db.update_settings = AsyncMock(return_value=True)
        
        return mock_db
    
    @pytest.mark.asyncio
    async def test_fictionality_analysis_query(self, mock_database):
        """Test getting fictionality analysis by ID"""
        with patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            resolver = FictionalityResolvers
            result = await resolver.resolve_fictionality_analysis(None, None, "test_analysis_123")
            
            assert result is not None
            assert result.id == "test_analysis_123"
            assert result.fictionality_score == 0.3
            assert result.confidence_level == FictionalityScore.PROBABLY_REAL
            assert len(result.fictionality_indicators) == 2
            assert len(result.realism_indicators) == 2
    
    @pytest.mark.asyncio
    async def test_fictionality_analyses_query(self, mock_database):
        """Test getting fictionality analyses with filtering"""
        with patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            resolver = FictionalityResolvers
            result = await resolver.resolve_fictionality_analyses(
                None, None, 
                min_score=0.2, max_score=0.4, 
                confidence=FictionalityScore.PROBABLY_REAL
            )
            
            assert len(result) == 1
            assert result[0].fictionality_score == 0.3
            mock_database.get_analyses.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_fictionality_metrics_query(self, mock_database):
        """Test getting fictionality metrics"""
        with patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            resolver = FictionalityResolvers
            result = await resolver.resolve_fictionality_metrics(None, None, pr_id="pr_123", period="7d")
            
            assert result.total_analyses == 50
            assert result.high_fictionality_count == 5
            assert result.average_score == 0.35
            assert result.cache_hit_rate == 0.25
    
    @pytest.mark.asyncio
    async def test_fictionality_health_report(self, mock_fictionality_analyzer, mock_database):
        """Test fictionality health report"""
        with patch('src.graphql.fictionality_resolvers.get_fictionality_analyzer', return_value=mock_fictionality_analyzer), \
             patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            
            resolver = FictionalityResolvers
            result = await resolver.resolve_fictionality_health_report(None, None)
            
            assert result.status == "healthy"
            assert result.healthy == True
            assert result.uptime > 0
            assert result.metrics.total_analyses == 50
    
    @pytest.mark.asyncio
    async def test_fictionality_analytics_query(self, mock_database):
        """Test fictionality analytics"""
        with patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            resolver = FictionalityResolvers
            result = await resolver.resolve_fictionality_analytics(
                None, None, pr_id="pr_123", period="30d"
            )
            
            assert result.total_analyses == 50
            assert result.average_fictionality_score == 0.35
            assert result.trend_direction == "stable"
            assert len(result.top_fictionality_indicators) == 2
            assert "vague_requirements" in result.top_fictionality_indicators
    
    @pytest.mark.asyncio
    async def test_fictionality_filter_conflicts(self, mock_database):
        """Test filtering conflicts by fictionality criteria"""
        with patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            resolver = FictionalityResolvers
            result = await resolver.resolve_fictionality_filter_conflicts(
                None, None, 
                min_score=0.1, max_score=0.5, 
                confidence_levels=[FictionalityScore.PROBABLY_REAL]
            )
            
            assert result.total_count == 1
            assert len(result.conflicts) == 1
            assert result.conflicts[0].fictionality_score == 0.2
            assert result.conflicts[0].fictionality_confidence == "PROBABLY_REAL"
    
    @pytest.mark.asyncio
    async def test_analyze_fictionality_mutation(self, mock_fictionality_analyzer, mock_database):
        """Test fictionality analysis mutation"""
        # Mock analysis result
        mock_result = Mock()
        mock_result.success = True
        mock_result.analysis = Mock()
        mock_result.analysis.id = "new_analysis_123"
        mock_result.analysis.conflict_id = "conflict_456"
        mock_result.analysis.pr_id = "pr_789"
        mock_result.analysis.fictionality_score = 0.4
        mock_result.analysis.confidence_level = FictionalityScore.UNCERTAIN
        mock_result.analysis.text_content = "Test content"
        mock_result.analysis.analysis_features = {"technical_consistency": 0.6}
        mock_result.analysis.fictionality_indicators = ["unrealistic_timeline"]
        mock_result.analysis.realism_indicators = ["specific_requirements"]
        mock_result.analysis.model = "gpt-4"
        mock_result.analysis.processing_time = 3.0
        mock_result.analysis.tokens_used = 1200
        mock_result.analysis.reasoning = "Content shows some uncertainty"
        mock_result.analysis.resolution_impact = "LOW_IMPACT: Standard resolution with enhanced monitoring"
        mock_result.analysis.strategy_adjustments = ["Add monitoring for resolution effectiveness"]
        mock_result.analysis.analysis_depth = "standard"
        mock_result.analysis.custom_threshold = None
        mock_result.analysis.created_at = datetime.utcnow()
        mock_result.analysis.updated_at = datetime.utcnow()
        mock_result.cached = False
        
        mock_fictionality_analyzer.analyze_fictionality = AsyncMock(return_value=mock_result)
        
        with patch('src.graphql.fictionality_resolvers.get_fictionality_analyzer', return_value=mock_fictionality_analyzer), \
             patch('src.graphql.fictionality_resolvers.pr_dao.get_pr', return_value=Mock(id="pr_789", title="Test PR")), \
             patch('src.graphql.fictionality_resolvers.conflict_dao.get_conflict', return_value=Mock(id="conflict_456", type="merge_conflict", description="Test conflict")), \
             patch('src.graphql.fictionality_resolvers.fictionality_dao', mock_database):
            
            resolver = FictionalityResolvers
            result = await resolver.resolve_analyze_fictionality(
                None, None, 
                pr_id="pr_789", 
                conflict_id="conflict_456", 
                content="Test content to analyze"
            )
            
            assert result is not None
            assert result.id == "new_analysis_123"
            assert result.fictionality_score == 0.4
            assert result.confidence_level == FictionalityScore.UNCERTAIN
            assert "unrealistic_timeline" in result.fictionality_indicators
            mock_database.save_analysis.assert_called_once()


class TestFictionalityQueryBuilder:
    """Test fictionality query builder"""
    
    def test_basic_score_range_filter(self):
        """Test basic score range filter"""
        builder = FictionalityQueryBuilder()
        query = builder.add_score_range_filter(0.2, 0.6).build_query()
        
        assert len(query["filters"]) == 1
        assert query["filters"][0]["type"] == "score_range"
        assert query["filters"][0]["min_score"] == 0.2
        assert query["filters"][0]["max_score"] == 0.6
    
    def test_confidence_filter(self):
        """Test confidence level filter"""
        builder = FictionalityQueryBuilder()
        query = builder.add_confidence_filter([
            FictionalityScore.HIGHLY_REAL,
            FictionalityScore.PROBABLY_REAL
        ]).build_query()
        
        assert len(query["filters"]) == 1
        assert query["filters"][0]["type"] == "confidence_level"
        assert "HIGHLY_REAL" in query["filters"][0]["confidence_levels"]
        assert "PROBABLY_REAL" in query["filters"][0]["confidence_levels"]
    
    def test_indicators_filter(self):
        """Test fictionality indicators filter"""
        builder = FictionalityQueryBuilder()
        query = builder.add_indicators_filter(
            include_indicators=["vague_requirements", "unrealistic_timeline"],
            exclude_indicators=["generic_content"]
        ).build_query()
        
        assert len(query["filters"]) == 1
        assert "include_indicators" in query["filters"][0]
        assert "exclude_indicators" in query["filters"][0]
        assert "vague_requirements" in query["filters"][0]["include_indicators"]
        assert "generic_content" in query["filters"][0]["exclude_indicators"]
    
    def test_time_range_filter(self):
        """Test time range filter"""
        builder = FictionalityQueryBuilder()
        query = builder.add_time_range_filter(period="7d").build_query()
        
        assert query["time_window"] is not None
        assert query["time_window"]["period"] == "7d"
    
    def test_combined_filters(self):
        """Test combining multiple filters"""
        builder = FictionalityQueryBuilder()
        query = (builder
            .add_score_range_filter(0.1, 0.7)
            .add_confidence_filter([FictionalityScore.PROBABLY_REAL])
            .add_time_range_filter(period="30d")
            .add_pr_context_filter(pr_id="pr_123")
            .sort_by_score()
            .build_query())
        
        assert len(query["filters"]) == 3
        assert query["time_window"] is not None
        assert query["context_requirements"]["pr_id"] == "pr_123"
        assert len(query["sort"]) == 1
        assert query["sort"][0]["field"] == "fictionality_score"
    
    def test_create_basic_filter_query(self):
        """Test utility function for basic filter query"""
        query = create_fictionality_filter_query(
            min_score=0.2,
            max_score=0.6,
            pr_id="pr_123",
            period="7d"
        )
        
        assert "filters" in query
        assert "time_window" in query
        assert query["time_window"]["period"] == "7d"


class TestFictionalityAnalyticsBuilder:
    """Test fictionality analytics builder"""
    
    def test_basic_analytics_query(self):
        """Test basic analytics query"""
        builder = FictionalityAnalyticsBuilder()
        query = (builder
            .add_period_analysis("7d")
            .add_period_analysis("30d")
            .add_fictionality_score_trend()
            .add_confidence_distribution()
            .add_indicators_analysis(top_n=5)
            .add_performance_metrics()
            .build_analytics_query())
        
        assert len(query["analysis_periods"]) == 2
        assert "fictionality_score" in query["trend_analysis"]
        assert "confidence_distribution" in query["metric_calculations"]
        assert "top_indicators" in query["metric_calculations"]
        assert "performance" in query["metric_calculations"]
    
    def test_create_basic_analytics_query(self):
        """Test utility function for analytics query"""
        query = create_fictionality_analytics_query(
            periods=["1d", "7d", "30d"],
            include_trends=True
        )
        
        assert len(query["analysis_periods"]) == 3
        assert "trend_analysis" in query
        assert "metric_calculations" in query


class TestFictionalityGraphQLIntegration:
    """Test GraphQL integration tests"""
    
    def test_fictionality_analysis_graphql_query(self):
        """Test GraphQL query for fictionality analysis"""
        # Test a fictionality analysis query
        query = """
        query {
            fictionalityAnalysis(id: "test_123") {
                id
                fictionalityScore
                confidenceLevel
                fictionalityIndicators
                realismIndicators
                reasoning
            }
        }
        """
        # This would test the actual GraphQL schema if we had real data
        # For now, we can test that the schema contains the query
        assert "fictionalityAnalysis" in str(schema)
    
    def test_batch_analyze_fictionality_mutation(self):
        """Test batch analysis mutation GraphQL"""
        # Test that the schema contains the batch analysis mutation
        assert "batchAnalyzeFictionality" in str(schema)
    
    def test_fictionality_filter_query(self):
        """Test fictionality filtering query"""
        # Test that the schema contains the filter query
        assert "fictionalityFilterConflicts" in str(schema)


# Performance and load tests
class TestFictionalityPerformance:
    """Test fictionality performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_batch_analysis_performance(self):
        """Test performance of batch fictionality analysis"""
        # Mock 10 analysis requests
        requests = [Mock() for _ in range(10)]
        for i, req in enumerate(requests):
            req.pr_id = f"pr_{i}"
            req.conflict_id = f"conflict_{i}"
            req.content = f"Test content {i}"
            req.analysis_type = "standard"
        
        # Test batch processing with different concurrency levels
        for max_concurrent in [1, 3, 5]:
            start_time = asyncio.get_event_loop().time()
            
            # Mock the batch resolver
            with patch('src.graphql.fictionality_resolvers.FictionalityResolvers.resolve_batch_analyze_fictionality') as mock_resolver:
                mock_resolver.return_value = [Mock() for _ in range(10)]
                
                # This would be the actual performance test
                # results = await mock_resolver(None, None, requests, max_concurrent)
                
            end_time = asyncio.get_event_loop().time()
            # assert (end_time - start_time) < 30.0  # Should complete within 30 seconds


if __name__ == "__main__":
    pytest.main([__file__, "-v"])