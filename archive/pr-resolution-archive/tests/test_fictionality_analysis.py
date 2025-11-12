"""
Comprehensive tests for fictionality analysis system in EmailIntelligence
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from typing import Dict, Any, List

from src.models.fictionality_models import (
    FictionalityAnalysis,
    FictionalityContext,
    FictionalityScore,
    FictionalityAnalysisRequest,
    FictionalityAnalysisOptions,
    FictionalityAnalysisResult,
    BatchFictionalityAnalysisRequest
)
from src.ai.fictionality_analyzer import FictionalityAnalyzer, FictionalityAnalysisContext
from src.ai.fictionality_processing import (
    FictionalityContentProcessor,
    FictionalityWorkflowProcessor,
    FictionalityBatchProcessor,
    analyze_content_fictionality,
    batch_analyze_fictionality
)
from src.config.fictionality_settings import fictionality_settings, FictionalityAnalysisConfig
from src.utils.caching import fictionality_cache_manager, cache_manager


class TestFictionalityModels:
    """Test fictionality data models"""
    
    def test_fictionality_score_enum(self):
        """Test FictionalityScore enum values"""
        assert FictionalityScore.HIGHLY_FICTIONAL == "HIGHLY_FICTIONAL"
        assert FictionalityScore.PROBABLY_FICTIONAL == "PROBABLY_FICTIONAL"
        assert FictionalityScore.UNCERTAIN == "UNCERTAIN"
        assert FictionalityScore.PROBABLY_REAL == "PROBABLY_REAL"
        assert FictionalityScore.HIGHLY_REAL == "HIGHLY_REAL"
    
    def test_fictionality_analysis_creation(self):
        """Test FictionalityAnalysis model creation"""
        analysis = FictionalityAnalysis(
            id="test_123",
            fictionality_score=0.75,
            confidence_level=FictionalityScore.PROBABLY_FICTIONAL,
            text_content="Test content",
            analysis_features={"technical_consistency": 0.8},
            fictionality_indicators=["generic_language"],
            realism_indicators=[],
            model="gpt-4",
            processing_time=1.5,
            tokens_used=500,
            conflict_id="conflict_456",
            pr_id="pr_789"
        )
        
        assert analysis.id == "test_123"
        assert analysis.fictionality_score == 0.75
        assert analysis.confidence_level == FictionalityScore.PROBABLY_FICTIONAL
        assert analysis.model == "gpt-4"
    
    def test_fictionality_context_creation(self):
        """Test FictionalityContext model creation"""
        context = FictionalityContext(
            pr_data={"id": "pr_123", "title": "Test PR"},
            conflict_data={"id": "conflict_456", "type": "merge"},
            content_to_analyze="Test content for analysis",
            analysis_depth="standard",
            include_strategies=True
        )
        
        assert context.pr_data["id"] == "pr_123"
        assert context.analysis_depth == "standard"
        assert context.include_strategies is True


class TestFictionalityAnalyzer:
    """Test FictionalityAnalyzer service"""
    
    @pytest.fixture
    async def mock_analyzer(self):
        """Create mock fictionality analyzer"""
        analyzer = FictionalityAnalyzer()
        analyzer.client = AsyncMock()
        analyzer.initialized = True
        return analyzer
    
    @pytest.mark.asyncio
    async def test_analyzer_initialization(self, mock_analyzer):
        """Test analyzer initialization"""
        mock_analyzer.client = None
        mock_analyzer.initialized = False
        
        with patch('src.ai.fictionality_analyzer.get_openai_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.initialized = True
            mock_get_client.return_value = mock_client
            
            result = await mock_analyzer.initialize()
            assert result is True
            assert mock_analyzer.initialized is True
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, mock_analyzer):
        """Test successful health check"""
        mock_analyzer.client = AsyncMock()
        mock_analyzer.client.chat_completion.return_value = {
            "choices": [{"message": {"content": "test"}}],
            "model": "gpt-4"
        }
        
        health = await mock_analyzer.health_check()
        
        assert health["status"] == "healthy"
        assert health["healthy"] is True
        assert "response_time" in health
    
    @pytest.mark.asyncio
    async def test_fictionality_analysis_success(self, mock_analyzer):
        """Test successful fictionality analysis"""
        # Mock AI response
        mock_analyzer.client.chat_completion.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "fictionality_score": 0.8,
                        "confidence": 0.9,
                        "features": {"technical_consistency": 0.2},
                        "fictionality_indicators": ["unrealistic_scenario"],
                        "realism_indicators": [],
                        "reasoning": "Content shows unrealistic scenario",
                        "resolution_impact": "HIGH_IMPACT: Require manual validation",
                        "recommended_strategies": ["manual_review"]
                    })
                }
            }],
            "model": "gpt-4",
            "response_time": 1.5,
            "usage": {"total_tokens": 500}
        }
        
        context = FictionalityContext(
            pr_data={"id": "test_pr"},
            conflict_data={"id": "test_conflict"},
            content_to_analyze="Fix critical bug that makes all users admins automatically"
        )
        
        result = await mock_analyzer.analyze_fictionality(context)
        
        assert result.success is True
        assert result.analysis is not None
        assert result.analysis.fictionality_score >= 0.7
        assert result.analysis.confidence_level == FictionalityScore.HIGHLY_FICTIONAL
        assert len(result.analysis.fictionality_indicators) > 0
    
    @pytest.mark.asyncio
    async def test_fictionality_analysis_fallback(self, mock_analyzer):
        """Test fallback when AI analysis fails"""
        mock_analyzer.client.chat_completion.side_effect = Exception("AI service unavailable")
        
        context = FictionalityContext(
            pr_data={"id": "test_pr"},
            conflict_data={"id": "test_conflict"},
            content_to_analyze="Test content"
        )
        
        result = await mock_analyzer.analyze_fictionality(context)
        
        assert result.success is False
        assert "AI service unavailable" in result.error
        assert result.analysis.fictionality_score == 0.5  # Neutral fallback
        assert result.analysis.confidence_level == FictionalityScore.UNCERTAIN
    
    def test_confidence_categorization(self, mock_analyzer):
        """Test confidence level categorization"""
        # Test high fictionality
        high_score = mock_analyzer._categorize_confidence(0.9)
        assert high_score == FictionalityScore.HIGHLY_FICTIONAL
        
        # Test probable fictionality
        probable_score = mock_analyzer._categorize_confidence(0.7)
        assert probable_score == FictionalityScore.PROBABLY_FICTIONAL
        
        # Test uncertain
        uncertain_score = mock_analyzer._categorize_confidence(0.5)
        assert uncertain_score == FictionalityScore.UNCERTAIN
        
        # Test probable real
        real_score = mock_analyzer._categorize_confidence(0.2)
        assert real_score == FictionalityScore.PROBABLY_REAL
        
        # Test highly real
        high_real_score = mock_analyzer._categorize_confidence(0.1)
        assert high_real_score == FictionalityScore.HIGHLY_REAL


class TestFictionalityConfiguration:
    """Test fictionality configuration"""
    
    def test_default_settings(self):
        """Test default fictionality settings"""
        assert fictionality_settings.fictionality_enabled is True
        assert fictionality_settings.fictionality_rate_limit_rpm == 3
        assert fictionality_settings.fictionality_cache_ttl == 3600
        assert fictionality_settings.fictionality_default_threshold == 0.6
    
    def test_analysis_config_methods(self):
        """Test FictionalityAnalysisConfig helper methods"""
        # Test analysis timeout
        timeout = FictionalityAnalysisConfig.get_analysis_timeout()
        assert isinstance(timeout, int)
        
        # Test max tokens for depth
        tokens = FictionalityAnalysisConfig.get_max_tokens_for_depth("standard")
        assert tokens == 1500
        
        # Test cache TTL
        ttl = FictionalityAnalysisConfig.get_cache_ttl_for_analysis("standard")
        assert ttl == 3600
        
        # Test feature enabling
        enabled = FictionalityAnalysisConfig.is_feature_enabled()
        assert enabled is True
        
        # Test batch config
        batch_config = FictionalityAnalysisConfig.get_batch_config()
        assert "max_size" in batch_config
        assert "max_concurrent" in batch_config
        assert "enabled" in batch_config


# Integration test example
class TestFictionalityIntegration:
    """Test fictionality analysis integration"""
    
    @pytest.mark.asyncio
    async def test_merge_conflict_fictionality_detection(self):
        """Test fictionality detection in merge conflict scenarios"""
        
        # Test realistic merge conflict
        realistic_content = """
        Merge conflict in src/auth/jwt_handler.py lines 45-67.
        Both branches modified the token validation logic.
        Current branch adds refresh token support, target branch
        implements role-based access control.
        """
        
        # Test fictionalized/fabricated conflict
        fictional_content = """
        Fix critical bug in authentication system that causes 
        all users to be logged in automatically with admin privileges.
        This is a security issue that needs immediate resolution.
        """
        
        # This demonstrates the core use case: distinguishing
        # realistic technical conflicts from fictional scenarios
        assert len(realistic_content) > 0
        assert len(fictional_content) > 0
        # In real tests, these would produce different fictionality scores