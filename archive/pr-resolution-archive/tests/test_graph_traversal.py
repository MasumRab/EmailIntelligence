"""
Comprehensive test suite for graph traversal and conflict detection system
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import List, Dict, Any
from datetime import datetime, timedelta
import time

from src.graph.traversal import GraphTraversalEngine, TraversalStrategy, TraversalDirection, TraversalResult
from src.graph.analytics import GraphAnalyticsEngine, CentralityMetric
from src.graph.performance import PerformanceOptimizationEngine, QueryOptimizer
from src.graph.query_builder import GraphQueryBuilder, ConflictQueryBuilder, QueryNodeType
from src.graph.scoring import ConflictScoringEngine, ConflictScore, PriorityLevel
from src.graph.specialized import SpecializedTraversalEngine, FileConflict, DependencyConflict
from src.models.graph_entities import PullRequest, Conflict, ConflictType, ConflictSeverity

# Test fixtures and utilities

@pytest.fixture
def mock_pull_requests():
    """Create mock pull requests for testing"""
    return [
        PullRequest(
            id="pr_1",
            title="Add user authentication",
            source_branch="feature/auth",
            target_branch="main",
            author_id="dev_1",
            complexity=0.7,
            estimated_resolution_time=120
        ),
        PullRequest(
            id="pr_2",
            title="Fix security vulnerability",
            source_branch="hotfix/security",
            target_branch="main",
            author_id="dev_2",
            complexity=0.9,
            estimated_resolution_time=60
        ),
        PullRequest(
            id="pr_3",
            title="Add database migrations",
            source_branch="feature/migrations",
            target_branch="main",
            author_id="dev_1",
            complexity=0.5,
            estimated_resolution_time=90
        )
    ]


@pytest.fixture
def mock_conflicts():
    """Create mock conflicts for testing"""
    return [
        Conflict(
            id="conflict_1",
            type=ConflictType.MERGE_CONFLICT,
            severity=ConflictSeverity.HIGH,
            description="Merge conflict in auth.py",
            affected_file_ids=["file_1", "file_2"],
            affected_commit_ids=["commit_1", "commit_2"]
        ),
        Conflict(
            id="conflict_2",
            type=ConflictType.DEPENDENCY_CONFLICT,
            severity=ConflictSeverity.CRITICAL,
            description="Circular dependency detected",
            affected_file_ids=["file_3"],
            affected_commit_ids=["commit_3"]
        )
    ]


# Graph Traversal Tests

class TestGraphTraversalEngine:
    """Test suite for GraphTraversalEngine"""
    
    @pytest.mark.asyncio
    async def test_breadth_first_search(self, mock_pull_requests):
        """Test BFS traversal functionality"""
        engine = GraphTraversalEngine()
        
        # Mock the database connection
        with patch('src.graph.traversal.connection_manager') as mock_conn:
            # Setup mock responses
            mock_conn.execute_query.return_value = asyncio.Future()
            mock_conn.execute_query.return_value.set_result([
                {"n": {"id": "node_1", "type": "PullRequest"}},
                {"n": {"id": "node_2", "type": "PullRequest"}}
            ])
            
            # Mock get_node method
            async def mock_get_node(node_id, node_type):
                return type('MockNode', (), {
                    'id': node_id,
                    'type': node_type,
                    'visited': False,
                    'distance': 0,
                    'parent': None
                })()
            
            engine.get_node = mock_get_node
            
            # Mock get_adjacent_nodes method
            async def mock_get_adjacent(node_id, relationships, direction):
                return [("node_2", "DEPENDS_ON")]
            
            engine.get_adjacent_nodes = mock_get_adjacent
            
            # Test BFS
            result = await engine.breadth_first_search(
                start_node_id="pr_1",
                start_node_type="PullRequest"
            )
            
            assert isinstance(result, TraversalResult)
            assert result.nodes_visited >= 0
            assert result.execution_time >= 0
    
    @pytest.mark.asyncio
    async def test_cycle_detection(self, mock_pull_requests):
        """Test cycle detection functionality"""
        engine = GraphTraversalEngine()
        
        with patch('src.graph.traversal.connection_manager') as mock_conn:
            mock_conn.execute_query.return_value = asyncio.Future()
            mock_conn.execute_query.return_value.set_result([])
            
            async def mock_get_node(node_id, node_type):
                return type('MockNode', (), {
                    'id': node_id,
                    'type': node_type
                })()
            
            async def mock_get_adjacent(node_id, relationships, direction):
                return [("pr_1", "DEPENDS_ON")]  # Self-loop to create cycle
            
            engine.get_node = mock_get_node
            engine.get_adjacent_nodes = mock_get_adjacent
            
            result = await engine.detect_cycles(
                start_node_id="pr_1",
                start_node_type="PullRequest"
            )
            
            assert isinstance(result, TraversalResult)
            assert result.metadata["strategy"] == "cycle_detection"


# Performance Tests

class TestPerformanceOptimizationEngine:
    """Test suite for PerformanceOptimizationEngine"""
    
    def test_query_optimizer(self):
        """Test query optimization"""
        engine = PerformanceOptimizationEngine()
        query = "MATCH (n:PullRequest) WHERE n.id = $pr_id RETURN n"
        parameters = {"pr_id": "pr_1"}
        
        optimized_query, optimized_params = asyncio.run(
            engine.query_optimizer.optimize_query(query, parameters)
        )
        
        assert isinstance(optimized_query, str)
        assert isinstance(optimized_params, dict)
        assert len(optimized_query) > 0
    
    @pytest.mark.asyncio
    async def test_execute_optimized_query(self):
        """Test optimized query execution"""
        engine = PerformanceOptimizationEngine()
        
        with patch('src.graph.performance.connection_manager') as mock_conn:
            mock_conn.execute_query.return_value = [
                {"n": {"id": "pr_1", "title": "Test PR"}}
            ]
            
            result = await engine.execute_optimized_query(
                "MATCH (n:PullRequest) RETURN n LIMIT 10"
            )
            
            assert isinstance(result, list)
            assert len(result) >= 0
    
    def test_cache_performance(self):
        """Test caching performance"""
        engine = PerformanceOptimizationEngine()
        
        # Test query caching
        query_hash = "test_query_hash"
        params_hash = "test_params_hash"
        test_data = {"test": "data"}
        
        engine.graph_cache.cache_query_result(
            query_hash, params_hash, test_data
        )
        
        cached_result = engine.graph_cache.get_cached_query(
            query_hash, params_hash
        )
        
        assert cached_result == test_data


# Conflict Scoring Tests

class TestConflictScoringEngine:
    """Test suite for ConflictScoringEngine"""
    
    @pytest.mark.asyncio
    async def test_score_single_conflict(self, mock_conflicts):
        """Test scoring a single conflict"""
        engine = ConflictScoringEngine()
        conflict = mock_conflicts[0]
        
        score = await engine.score_conflict(conflict)
        
        assert isinstance(score, ConflictScore)
        assert 0.0 <= score.total_score <= 10.0
        assert score.priority in [p for p in PriorityLevel]
        assert 0.0 <= score.confidence <= 1.0
    
    @pytest.mark.asyncio
    async def test_create_priority_queue(self, mock_conflicts):
        """Test creating priority queue"""
        engine = ConflictScoringEngine()
        queue = await engine.create_priority_queue(mock_conflicts)
        
        assert isinstance(queue, dict)
        assert PriorityLevel.URGENT in queue
        assert PriorityLevel.HIGH in queue
        assert isinstance(queue[PriorityLevel.URGENT], list)


# Integration Tests

class TestGraphSystemIntegration:
    """Integration tests for the entire graph system"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_conflict_analysis(self, mock_pull_requests, mock_conflicts):
        """Test complete conflict analysis workflow"""
        # Mock the full system
        with patch('src.graph.scoring.connection_manager') as mock_conn:
            # Setup comprehensive mock responses
            mock_conn.execute_query.return_value = asyncio.Future()
            mock_conn.execute_query.return_value.set_result([
                {"n": {"id": "pr_1", "complexity": 0.7}},
                {"n": {"id": "conflict_1", "severity": "HIGH"}}
            ])
            
            # Initialize engines
            scoring_engine = ConflictScoringEngine()
            
            # Score and prioritize conflicts
            prioritized_conflicts = await scoring_engine.prioritize_conflicts(mock_conflicts)
            
            # Verify the workflow completed
            assert isinstance(prioritized_conflicts, list)
            assert len(prioritized_conflicts) > 0
            
            # Verify scoring is working
            for score in prioritized_conflicts:
                assert 0.0 <= score.total_score <= 10.0
                assert isinstance(score.priority, PriorityLevel)


# Performance Benchmark Tests

class TestPerformanceBenchmarks:
    """Performance benchmark tests"""
    
    @pytest.mark.asyncio
    async def test_traversal_performance_benchmark(self):
        """Benchmark traversal engine performance"""
        engine = GraphTraversalEngine()
        start_time = time.time()
        
        # Mock large graph traversal
        with patch('src.graph.traversal.connection_manager') as mock_conn:
            mock_conn.execute_query.return_value = asyncio.Future()
            mock_conn.execute_query.return_value.set_result([
                {"n": {"id": f"node_{i}", "type": "PullRequest"}} for i in range(100)
            ])
            
            async def mock_get_node(node_id, node_type):
                return type('MockNode', (), {
                    'id': node_id,
                    'type': node_type
                })()
            
            async def mock_get_adjacent(node_id, relationships, direction):
                return [("node_1", "DEPENDS_ON")]
            
            engine.get_node = mock_get_node
            engine.get_adjacent_nodes = mock_get_adjacent
            
            result = await engine.breadth_first_search(
                start_node_id="node_0",
                start_node_type="PullRequest",
                max_depth=5
            )
            
            execution_time = time.time() - start_time
            
            # Performance assertions
            assert execution_time < 2.0  # Should complete within 2 seconds
            assert result.nodes_visited >= 0


# Test Configuration and Utilities

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )


# Test data generators

def generate_mock_prs(count: int) -> List[PullRequest]:
    """Generate mock PRs for testing"""
    prs = []
    for i in range(count):
        pr = PullRequest(
            id=f"pr_{i}",
            title=f"Test PR {i}",
            source_branch=f"feature/branch_{i}",
            target_branch="main",
            author_id=f"dev_{i % 3}",  # Cycle through 3 developers
            complexity=0.1 * (i % 10),  # Vary complexity
            estimated_resolution_time=60 + (i * 10)  # Vary resolution time
        )
        prs.append(pr)
    return prs


def generate_mock_conflicts(count: int) -> List[Conflict]:
    """Generate mock conflicts for testing"""
    conflicts = []
    conflict_types = list(ConflictType)
    severities = list(ConflictSeverity)
    
    for i in range(count):
        conflict = Conflict(
            id=f"conflict_{i}",
            type=conflict_types[i % len(conflict_types)],
            severity=severities[i % len(severities)],
            description=f"Test conflict {i}",
            affected_file_ids=[f"file_{j}" for j in range(1 + (i % 3))],
            affected_commit_ids=[f"commit_{j}" for j in range(1 + (i % 2))],
            detected_at=datetime.utcnow() - timedelta(hours=i)
        )
        conflicts.append(conflict)
    
    return conflicts


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])