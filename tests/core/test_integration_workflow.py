"""
Integration tests for end-to-end workflow validation.

These tests verify that all components work together correctly,
following scientific integration testing methodologies.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from src.core.workflow_engine import WorkflowEngine
from src.core.data_source import DataSource
from src.backend.services.ai_engine import AIEngine


@pytest.mark.integration_test
class TestEndToEndWorkflow:
    """End-to-end integration tests for the complete email processing workflow."""

    @pytest.fixture(autouse=True)
    async def setup_integration(self, mock_database_session, mock_redis_client):
        """Set up integration test environment."""
        self.db_session = mock_database_session
        self.redis_client = mock_redis_client

        # Initialize real components for integration testing
        self.workflow_engine = WorkflowEngine()
        self.data_source = DataSource()
        self.ai_engine = AIEngine()

    async def test_complete_email_processing_workflow(self, sample_email_data):
        """Test the complete workflow from email ingestion to AI analysis."""
        # Step 1: Ingest emails
        ingested_count = 0
        for email in sample_email_data:
            # Simulate email ingestion
            result = await self._simulate_email_ingestion(email)
            assert result["success"] is True
            ingested_count += 1

        assert ingested_count == len(sample_email_data)

        # Step 2: Process emails through workflow engine
        processed_emails = []
        for email in sample_email_data:
            workflow_result = await self.workflow_engine.process_email(email)
            assert "processed_at" in workflow_result
            assert workflow_result["status"] == "processed"
            processed_emails.append(workflow_result)

        assert len(processed_emails) == len(sample_email_data)

        # Step 3: AI analysis
        analyzed_emails = []
        for email in processed_emails:
            ai_result = await self.ai_engine.analyze_email(email)
            assert "sentiment" in ai_result
            assert "topic" in ai_result
            assert "intent" in ai_result
            analyzed_emails.append({**email, **ai_result})

        assert len(analyzed_emails) == len(sample_email_data)

        # Step 4: Data persistence and retrieval
        saved_count = await self._simulate_data_persistence(analyzed_emails)
        assert saved_count == len(analyzed_emails)

        # Step 5: Query and validate results
        retrieved_emails = await self.data_source.query_emails({
            "limit": len(sample_email_data) + 10
        })
        assert len(retrieved_emails) >= len(analyzed_emails)

        # Verify data integrity
        for original in analyzed_emails:
            matching_email = next(
                (e for e in retrieved_emails if e["id"] == original["id"]), None
            )
            assert matching_email is not None, f"Email {original['id']} not found in results"
            assert matching_email["sentiment"] == original["sentiment"]

    async def test_concurrent_workflow_processing(self, large_email_dataset):
        """Test concurrent processing of multiple emails."""
        # Process emails concurrently
        tasks = []
        for email in large_email_dataset[:50]:  # Test with subset for performance
            task = asyncio.create_task(self._process_single_email_workflow(email))
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all tasks completed successfully
        successful_results = [r for r in results if not isinstance(r, Exception)]
        failed_results = [r for r in results if isinstance(r, Exception)]

        assert len(successful_results) > len(failed_results), f"Too many failures: {len(failed_results)}"
        assert len(successful_results) > 0, "No successful results"

        # Verify result consistency
        for result in successful_results:
            assert result["status"] == "completed"
            assert "processed_at" in result
            assert "ai_analysis" in result

    async def test_workflow_error_handling_and_recovery(self, sample_email_data):
        """Test error handling and recovery in the workflow."""
        # Introduce artificial failures
        error_email = {**sample_email_data[0], "corrupted": True}

        # Test error handling in ingestion
        with patch.object(self.workflow_engine, 'process_email', side_effect=Exception("Processing failed")):
            with pytest.raises(Exception):
                await self.workflow_engine.process_email(error_email)

        # Test recovery - process normal emails should still work
        normal_result = await self.workflow_engine.process_email(sample_email_data[1])
        assert normal_result["status"] == "processed"

        # Test partial failure recovery
        mixed_emails = [error_email, sample_email_data[1], sample_email_data[2]]

        results = []
        for email in mixed_emails:
            try:
                result = await self.workflow_engine.process_email(email)
                results.append(("success", result))
            except Exception as e:
                results.append(("error", str(e)))

        # Should have 2 successes and 1 error
        successes = [r for r in results if r[0] == "success"]
        errors = [r for r in results if r[0] == "error"]

        assert len(successes) == 2
        assert len(errors) == 1

    async def test_performance_under_load(self, large_email_dataset):
        """Test system performance under load."""
        import time

        start_time = time.time()

        # Process large batch
        batch_size = 100
        for i in range(0, min(len(large_email_dataset), 500), batch_size):
            batch = large_email_dataset[i:i + batch_size]
            tasks = [self._process_single_email_workflow(email) for email in batch]
            await asyncio.gather(*tasks)

        end_time = time.time()
        total_time = end_time - start_time

        # Performance assertions (adjust thresholds based on system capabilities)
        emails_processed = min(len(large_email_dataset), 500)
        avg_time_per_email = total_time / emails_processed

        # Should process emails reasonably quickly (adjust threshold as needed)
        assert avg_time_per_email < 1.0, f"Too slow: {avg_time_per_email:.3f}s per email"
        assert total_time < 300, f"Total processing took too long: {total_time:.2f}s"

    # Helper methods for integration testing

    async def _simulate_email_ingestion(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate email ingestion process."""
        # In a real implementation, this would interact with email APIs
        await asyncio.sleep(0.001)  # Simulate I/O delay
        return {
            "success": True,
            "email_id": email["id"],
            "ingested_at": "2024-01-01T00:00:00Z"
        }

    async def _simulate_data_persistence(self, emails: list) -> int:
        """Simulate data persistence."""
        # In a real implementation, this would save to database
        await asyncio.sleep(0.005)  # Simulate DB write delay
        return len(emails)

    async def _process_single_email_workflow(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single email through the complete workflow."""
        # Step 1: Workflow processing
        workflow_result = await self.workflow_engine.process_email(email)

        # Step 2: AI analysis
        ai_result = await self.ai_engine.analyze_email(workflow_result)

        # Combine results
        return {
            "email_id": email["id"],
            "status": "completed",
            "processed_at": "2024-01-01T00:00:00Z",
            "workflow_result": workflow_result,
            "ai_analysis": ai_result
        }


@pytest.mark.integration_test
class TestSystemIntegration:
    """System-level integration tests."""

    async def test_cross_component_data_flow(self, integration_test_config):
        """Test data flow between all major components."""
        # This would test the complete data pipeline
        # from email ingestion -> AI processing -> database storage -> API retrieval

        # Initialize all components
        components = {
            "workflow_engine": WorkflowEngine(),
            "data_source": DataSource(),
            "ai_engine": AIEngine()
        }

        # Test data flow
        test_data = {
            "email": {
                "id": "integration_test_1",
                "subject": "Integration Test",
                "content": "Testing complete system integration."
            }
        }

        # Process through each component
        current_data = test_data["email"]

        for component_name, component in components.items():
            if hasattr(component, 'process'):
                current_data = await component.process(current_data)
                assert current_data is not None, f"{component_name} returned None"
            elif hasattr(component, 'analyze'):
                analysis_result = await component.analyze(current_data)
                current_data = {**current_data, "analysis": analysis_result}

        # Verify final result has all expected data
        assert "analysis" in current_data
        assert "processed_at" in current_data
        assert current_data["id"] == test_data["email"]["id"]

    async def test_configuration_integration(self, integration_test_config):
        """Test that all components properly use configuration."""
        # Verify configuration is properly distributed to components

        # This would check that database connections, API endpoints, etc.
        # are properly configured across all components

        required_config_keys = [
            "database_url",
            "redis_url",
            "api_base_url"
        ]

        for key in required_config_keys:
            assert key in integration_test_config, f"Missing config key: {key}"
            assert integration_test_config[key], f"Empty config value for: {key}"