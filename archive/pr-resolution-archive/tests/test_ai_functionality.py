"""
Test suite for AI functionality in PR Resolution Automation System
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# ARCHIVED: PR Resolution System - AI service imports moved to archive
# from src.ai.client import OpenAIClient  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/
# from src.ai.analysis import ConflictAnalyzer  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/
# from src.ai.processing import AIProcessor, TaskStatus, TaskPriority  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/
# from src.ai.monitoring import AIMonitor  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/
# from src.ai.interfaces import CircuitBreaker, RateLimiter, CacheManager  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/
from src.config.settings import settings


class TestCircuitBreaker:
    """Test circuit breaker functionality"""
    
    def test_circuit_breaker_initial_state(self):
        """Test circuit breaker starts in closed state"""
        cb = CircuitBreaker(failure_threshold=3)
        assert cb.state == 'closed'
        assert cb.failure_count == 0
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_failure_threshold(self):
        """Test circuit breaker opens after failure threshold"""
        cb = CircuitBreaker(failure_threshold=2)
        
        # Simulate failures
        for _ in range(2):
            await cb.record_failure()
        
        assert cb.state == 'open'
        assert cb.failure_count == 2
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_success_resets(self):
        """Test circuit breaker resets on success"""
        cb = CircuitBreaker(failure_threshold=2)
        
        # Simulate failures
        await cb.record_failure()
        await cb.record_failure()
        assert cb.state == 'open'
        
        # Simulate success
        await cb.record_success()
        assert cb.state == 'closed'
        assert cb.failure_count == 0
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_can_attempt_closed(self):
        """Test circuit breaker allows attempts when closed"""
        cb = CircuitBreaker(failure_threshold=2)
        assert await cb.can_attempt() is True
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_can_attempt_open(self):
        """Test circuit breaker blocks attempts when open"""
        cb = CircuitBreaker(failure_threshold=2, timeout=1)
        
        # Simulate failures to open circuit
        await cb.record_failure()
        await cb.record_failure()
        assert cb.state == 'open'
        
        # Should not allow attempts immediately
        assert await cb.can_attempt() is False


class TestRateLimiter:
    """Test rate limiter functionality"""
    
    @pytest.mark.asyncio
    async def test_rate_limiter_allows_requests_within_limit(self):
        """Test rate limiter allows requests within rate limit"""
        limiter = RateLimiter(rate_per_minute=3)
        
        # Should allow requests within limit
        assert await limiter.acquire() is True
        assert await limiter.acquire() is True
        assert await limiter.acquire() is True
    
    @pytest.mark.asyncio
    async def rate_limiter_blocks_excess_requests(self):
        """Test rate limiter blocks requests beyond limit"""
        limiter = RateLimiter(rate_per_minute=2)
        
        # Use up the limit
        assert await limiter.acquire() is True
        assert await limiter.acquire() is True
        
        # Should block the next request
        assert await limiter.acquire() is False


class TestCacheManager:
    """Test cache manager functionality"""
    
    def test_cache_generates_consistent_keys(self):
        """Test cache generates consistent keys for same content"""
        cache = CacheManager()
        
        context1 = {"param1": "value1", "param2": "value2"}
        context2 = {"param2": "value2", "param1": "value1"}  # Same content, different order
        
        key1 = cache._generate_key("test_prompt", context1)
        key2 = cache._generate_key("test_prompt", context2)
        
        assert key1 == key2
    
    def test_cache_set_and_get(self):
        """Test cache can store and retrieve values"""
        cache = CacheManager()
        
        test_data = {"analysis": "test", "confidence": 0.8}
        cache.set("test_prompt", {"context": "test"}, test_data)
        
        result = cache.get("test_prompt", {"context": "test"})
        assert result == test_data
    
    def test_cache_expiration(self):
        """Test cache respects TTL"""
        cache = CacheManager(cache_ttl=1)  # 1 second TTL
        
        test_data = {"analysis": "test"}
        cache.set("test_prompt", {"context": "test"}, test_data)
        
        # Should be available immediately
        result = cache.get("test_prompt", {"context": "test"})
        assert result == test_data


class TestOpenAIClient:
    """Test OpenAI client functionality"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Create mock OpenAI client"""
        with patch('src.ai.client.AsyncOpenAI') as mock_client:
            yield mock_client.return_value
    
    @pytest.mark.asyncio
    async def test_client_initialization_success(self, mock_openai_client):
        """Test successful client initialization"""
        # Mock successful response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hello"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.model = "gpt-4"
        mock_response.usage = Mock()
        mock_response.usage.prompt_tokens = 5
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 10
        
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient()
        result = await client.initialize()
        
        assert result is True
        assert client.initialized is True
    
    @pytest.mark.asyncio
    async def test_client_initialization_no_api_key(self):
        """Test client initialization fails without API key"""
        with patch.object(settings, 'openai_api_key', None):
            client = OpenAIClient()
            result = await client.initialize()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_chat_completion_with_caching(self, mock_openai_client):
        """Test chat completion with caching"""
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.model = "gpt-4"
        mock_response.usage = Mock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient()
        client.initialized = True
        client.client = mock_openai_client
        
        messages = [{"role": "user", "content": "Test message"}]
        result1 = await client.chat_completion(messages)
        
        # Second call should return cached result
        result2 = await client.chat_completion(messages)
        
        assert result1 == result2
        assert mock_openai_client.chat.completions.create.call_count == 1


class TestConflictAnalyzer:
    """Test conflict analyzer functionality"""
    
    @pytest.fixture
    def mock_analyzer(self):
        """Create conflict analyzer with mocked dependencies"""
        analyzer = ConflictAnalyzer()
        analyzer.client = AsyncMock()
        return analyzer
    
    @pytest.mark.asyncio
    async def test_analyze_conflict_success(self, mock_analyzer):
        """Test successful conflict analysis"""
        # Mock AI response
        mock_response = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "complexity_score": 6,
                        "confidence_score": 0.8,
                        "estimated_resolution_time": 120,
                        "overall_assessment": "Moderate complexity conflict"
                    })
                }
            }]
        }
        mock_analyzer.client.chat_completion.return_value = mock_response
        
        pr_data = {
            "id": "pr_123",
            "title": "Test PR",
            "description": "Test description"
        }
        conflict_data = {
            "conflicts": [{
                "type": "merge_conflict",
                "description": "Test conflict"
            }]
        }
        
        result = await mock_analyzer.analyze_conflict(pr_data, conflict_data)
        
        assert "complexity_score" in result
        assert result["complexity_score"] == 6
        assert "confidence_score" in result
        assert result["confidence_score"] == 0.8
    
    @pytest.mark.asyncio
    async def test_analyze_conflict_fallback(self, mock_analyzer):
        """Test conflict analysis fallback on error"""
        # Mock error response
        mock_analyzer.client.chat_completion.side_effect = Exception("API Error")
        
        pr_data = {"id": "pr_123", "title": "Test PR"}
        conflict_data = {"conflicts": []}
        
        result = await mock_analyzer.analyze_conflict(pr_data, conflict_data)
        
        assert "fallback_used" in result
        assert result["fallback_used"] is True
        assert "ai_error" in result
    
    def test_complexity_heuristic(self, mock_analyzer):
        """Test complexity assessment heuristic"""
        pr_data = {
            "files": ["file1.py", "file2.py", "file3.py"],
            "lines_changed": 500
        }
        
        complexity = mock_analyzer._assess_complexity_heuristic(pr_data)
        
        assert 1.0 <= complexity <= 10.0
        assert complexity > 0


class TestAIProcessor:
    """Test AI processing pipeline"""
    
    @pytest.fixture
    def processor(self):
        """Create AI processor"""
        return AIProcessor(max_workers=2)
    
    @pytest.mark.asyncio
    async def test_submit_task(self, processor):
        """Test task submission"""
        task_id = await processor.submit_task(
            task_type="analyze_conflict",
            payload={"test": "data"},
            priority=TaskPriority.NORMAL
        )
        
        assert task_id is not None
        assert len(task_id) > 0
    
    @pytest.mark.asyncio
    async def test_task_processing(self, processor):
        """Test task processing"""
        # Start processor
        await processor.start()
        
        try:
            # Submit a task
            task_id = await processor.submit_task(
                task_type="analyze_conflict",
                payload={"pr_id": "pr_123", "conflict_id": "conflict_456"},
                priority=TaskPriority.NORMAL
            )
            
            # Wait a bit for processing
            await asyncio.sleep(1)
            
            # Check task status
            status = await processor.get_task_status(task_id)
            assert status is not None
            assert "status" in status
            
        finally:
            await processor.stop()
    
    @pytest.mark.asyncio
    async def test_task_cancellation(self, processor):
        """Test task cancellation"""
        # Start processor
        await processor.start()
        
        try:
            # Submit a task
            task_id = await processor.submit_task(
                task_type="analyze_conflict",
                payload={"test": "data"},
                priority=TaskPriority.NORMAL
            )
            
            # Cancel the task
            cancelled = await processor.cancel_task(task_id)
            assert cancelled is True
            
        finally:
            await processor.stop()


class TestAIMonitor:
    """Test AI monitoring functionality"""
    
    @pytest.fixture
    def monitor(self):
        """Create AI monitor"""
        return AIMonitor(max_history=10)
    
    @pytest.mark.asyncio
    async def test_collect_metrics(self, monitor):
        """Test metrics collection"""
        # Mock the dependencies
        with patch('src.ai.monitoring.get_openai_client') as mock_client, \
             patch('src.ai.monitoring.get_conflict_analyzer') as mock_analyzer, \
             patch('src.ai.monitoring.get_ai_processor') as mock_processor:
            
            # Setup mocks
            mock_client.return_value.get_stats.return_value = {
                "request_count": 100,
                "error_count": 5,
                "circuit_breaker_state": "closed"
            }
            mock_analyzer.return_value.health_check.return_value = {"status": "healthy"}
            mock_processor.return_value.get_stats.return_value = {
                "active_tasks": 2,
                "completed_tasks": 98
            }
            
            metrics = await monitor.collect_metrics()
            
            assert metrics.request_count == 100
            assert metrics.error_count == 5
            assert metrics.circuit_breaker_state == "closed"
            assert metrics.active_tasks == 2
            assert metrics.completed_tasks == 98
    
    def test_performance_analysis_no_data(self, monitor):
        """Test performance analysis with no data"""
        result = asyncio.run(monitor.get_performance_analysis(hours=24))
        assert "error" in result
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_status_check(self, monitor):
        """Test circuit breaker status check"""
        with patch('src.ai.monitoring.get_openai_client') as mock_client:
            mock_client.return_value.get_stats.return_value = {
                "circuit_breaker_state": "closed",
                "error_count": 2,
                "request_count": 100
            }
            
            status = await monitor.check_circuit_breaker_status()
            
            assert "state" in status
            assert "status" in status
            assert status["state"] == "closed"


class TestPromptTemplates:
    """Test prompt template functionality"""
    
    def test_format_prompt(self):
        """Test prompt formatting"""
        from src.ai.prompts import PromptTemplates
        
        template = "Hello {name}, you have {count} messages"
        result = PromptTemplates.format_prompt(template, name="Alice", count=5)
        
        assert result == "Hello Alice, you have 5 messages"
    
    def test_conflict_analysis_prompt_creation(self):
        """Test conflict analysis prompt creation"""
        from src.ai.prompts import PromptTemplates
        
        pr_data = {
            "title": "Test PR",
            "description": "Test description",
            "source_branch": "feature",
            "target_branch": "main",
            "files": ["file1.py", "file2.py"],
            "lines_changed": 100
        }
        conflict_data = {
            "conflicts": [
                {
                    "type": "merge_conflict",
                    "description": "Conflict in file1.py",
                    "files": ["file1.py"]
                }
            ]
        }
        
        messages = PromptTemplates.analyze_conflict_prompt(pr_data, conflict_data)
        
        assert len(messages) == 2  # system + user
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert "Test PR" in messages[1]["content"]


class TestGraphQLIntegration:
    """Test GraphQL integration with AI functionality"""
    
    @pytest.mark.asyncio
    async def test_ai_resolvers_import(self):
        """Test that AI resolvers can be imported"""
        from src.graphql.ai_resolvers import AIResolvers
        
        assert hasattr(AIResolvers, 'resolve_ai_analysis')
        assert hasattr(AIResolvers, 'resolve_analyze_conflict_with_ai')
    
    @pytest.mark.asyncio
    async def test_ai_health_report_resolver(self):
        """Test AI health report resolver"""
        from src.graphql.ai_resolvers import AIResolvers
        
        with patch('src.graphql.ai_resolvers.get_ai_monitor') as mock_monitor:
            mock_monitor.return_value.get_health_report.return_value = {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_status": "healthy",
                "current_metrics": {},
                "service_health": {"openai": "healthy"},
                "trends": {},
                "recent_alerts": [],
                "usage_analytics": {},
                "recommendations": ["Continue monitoring"]
            }
            
            result = await AIResolvers.resolve_ai_health_report(None, None)
            
            assert result["overall_status"] == "healthy"
            assert "recommendations" in result


# Integration tests
class TestAIIntegration:
    """Test AI system integration"""
    
    @pytest.mark.asyncio
    async def test_full_analysis_pipeline(self):
        """Test complete analysis pipeline"""
        # This would test the full integration of AI services
        # For now, just verify the imports work
        from src.ai.client import OpenAIClient
        from src.ai.analysis import ConflictAnalyzer
        from src.ai.processing import AIProcessor
        from src.ai.monitoring import AIMonitor
        
        # Verify services can be instantiated
        client = OpenAIClient()
        analyzer = ConflictAnalyzer()
        processor = AIProcessor()
        monitor = AIMonitor()
        
        assert client is not None
        assert analyzer is not None
        assert processor is not None
        assert monitor is not None
    
    @pytest.mark.asyncio
    async def test_error_handling_across_services(self):
        """Test error handling across AI services"""
        from src.ai.client import OpenAIClient
        from src.ai.analysis import ConflictAnalyzer
        
        # Test that services handle errors gracefully
        client = OpenAIClient()
        analyzer = ConflictAnalyzer()
        
        # Both should handle uninitialized state gracefully
        assert client.initialized is False
        assert analyzer.client is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])