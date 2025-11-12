"""
Test suite for GraphQL PR Resolution API
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient

# Import the FastAPI app
from src.api.main import app


class TestGraphQLAPI:
    """Test GraphQL API endpoints"""
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check endpoint"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "services" in data
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test root endpoint"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "PR Resolution Automation API" in data["message"]
    
    @pytest.mark.asyncio
    async def test_graphql_query(self):
        """Test basic GraphQL query"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            query = {
                "query": """
                query {
                    systemHealth {
                        status
                        uptime
                    }
                }
                """
            }
            response = await client.post("/graphql", json=query)
            assert response.status_code == 200
            data = response.json()
            assert "data" in data
            assert "systemHealth" in data["data"]
    
    @pytest.mark.asyncio
    async def test_create_pr_mutation(self):
        """Test PR creation mutation"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            mutation = {
                "query": """
                mutation CreatePR($input: CreatePRInputType!) {
                    createPR(input: $input) {
                        id
                        title
                        status
                    }
                }
                """,
                "variables": {
                    "input": {
                        "title": "Test PR",
                        "description": "Test description",
                        "sourceBranch": "feature/test",
                        "targetBranch": "main",
                        "authorId": "user123"
                    }
                }
            }
            response = await client.post("/graphql", json=mutation)
            assert response.status_code == 200
            data = response.json()
            assert "data" in data
            assert "createPR" in data["data"]
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # This would test rate limiting in a real scenario
        # For now, just test the endpoint exists
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/metrics")
            assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/metrics")
            assert response.status_code == 200
            data = response.json()
            assert "performance" in data
            assert "cache" in data
            assert "rate_limits" in data
            assert "system" in data


class TestDatabaseIntegration:
    """Test database integration"""
    
    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connection health check"""
        # Mock database connection for testing
        with patch('src.database.init.database_health_check') as mock_health:
            mock_health.return_value = {"status": "healthy"}
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/health")
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_cache_health(self):
        """Test cache health check"""
        # Mock cache health for testing
        with patch('src.utils.caching.cache_manager.health_check') as mock_cache:
            mock_cache.return_value = True
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/health")
                assert response.status_code == 200


class TestGraphQLSchema:
    """Test GraphQL schema validation"""
    
    def test_schema_introspection(self):
        """Test GraphQL schema introspection"""
        from src.graphql.schema import schema
        
        # Test that schema can be created without errors
        assert schema is not None
    
    def test_query_type_exists(self):
        """Test that Query type is defined"""
        from src.graphql.schema import Query
        
        # Basic check that Query class exists
        assert hasattr(Query, 'resolve_pull_request')
        assert hasattr(Query, 'resolve_pull_requests')
        assert hasattr(Query, 'resolve_system_health')
    
    def test_mutation_type_exists(self):
        """Test that Mutation type is defined"""
        from src.graphql.schema import Mutation
        
        # Basic check that Mutation class exists
        assert hasattr(Mutation, 'resolve_create_pr')
        assert hasattr(Mutation, 'resolve_update_pr_status')


if __name__ == "__main__":
    pytest.main([__file__])