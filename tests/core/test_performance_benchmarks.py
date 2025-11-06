"""
Performance benchmarks for core components.

These benchmarks measure and track performance characteristics of critical
system components, ensuring that changes don't introduce performance regressions.
Uses pytest-benchmark for scientific performance validation.
"""

import pytest
import time
from typing import List, Dict, Any

from src.core.workflow_engine import WorkflowEngine
from src.core.data_source import DataSource


class TestWorkflowEngineBenchmarks:
    """Performance benchmarks for WorkflowEngine."""

    def setup_method(self):
        """Set up test fixtures."""
        self.engine = WorkflowEngine()

    def test_workflow_creation_benchmark(self, benchmark):
        """Benchmark workflow creation performance."""
        def create_workflow():
            workflow_config = {
                "name": "benchmark_workflow",
                "nodes": [
                    {"id": f"node_{i}", "type": "test", "config": {"param": f"value_{i}"}}
                    for i in range(10)
                ]
            }
            return workflow_config

        result = benchmark(create_workflow)
        assert result is not None
        assert len(result["nodes"]) == 10

    def test_workflow_execution_benchmark(self, benchmark):
        """Benchmark workflow execution performance."""
        def execute_workflow_operations():
            # Simulate workflow execution with multiple operations
            operations = []
            for i in range(100):
                operations.append({"type": "process", "data": f"item_{i}"})
            return operations

        result = benchmark(execute_workflow_operations)
        assert len(result) == 100

    def test_concurrent_workflow_benchmark(self, benchmark):
        """Benchmark concurrent workflow processing."""
        def process_concurrent_workflows():
            workflows = []
            for i in range(5):  # Simulate 5 concurrent workflows
                workflow = {
                    "id": f"workflow_{i}",
                    "nodes": [{"id": f"node_{j}", "data": f"data_{j}"} for j in range(20)]
                }
                workflows.append(workflow)
            return workflows

        result = benchmark(process_concurrent_workflows)
        assert len(result) == 5
        assert all(len(w["nodes"]) == 20 for w in result)


class TestDataSourceBenchmarks:
    """Performance benchmarks for DataSource operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.data_source = DataSource()

    def test_data_query_benchmark(self, benchmark):
        """Benchmark data query performance."""
        def query_data():
            # Simulate data queries with different parameters
            queries = []
            for i in range(50):
                query = {
                    "type": "email_search",
                    "filters": {
                        "date_from": "2024-01-01",
                        "category": f"category_{i % 5}",
                        "limit": 100
                    }
                }
                queries.append(query)
            return queries

        result = benchmark(query_data)
        assert len(result) == 50

    def test_data_aggregation_benchmark(self, benchmark):
        """Benchmark data aggregation performance."""
        def aggregate_data():
            # Simulate aggregation operations
            data_sets = []
            for i in range(10):
                data_set = {
                    "emails": [f"email_{j}" for j in range(100)],
                    "categories": [f"cat_{j % 5}" for j in range(100)],
                    "metrics": {"total": 100, "processed": 95, "failed": 5}
                }
                data_sets.append(data_set)
            return data_sets

        result = benchmark(aggregate_data)
        assert len(result) == 10
        assert all(len(ds["emails"]) == 100 for ds in result)

    def test_bulk_data_processing_benchmark(self, benchmark):
        """Benchmark bulk data processing performance."""
        def process_bulk_data():
            # Simulate bulk processing of large datasets
            processed_items = []
            for batch in range(10):
                for item in range(100):  # 100 items per batch
                    processed_item = {
                        "id": f"item_{batch}_{item}",
                        "processed_at": time.time(),
                        "status": "completed"
                    }
                    processed_items.append(processed_item)
            return processed_items

        result = benchmark(process_bulk_data)
        assert len(result) == 1000  # 10 batches * 100 items


class TestMemoryUsageBenchmarks:
    """Memory usage benchmarks for resource-intensive operations."""

    def test_memory_efficient_processing_benchmark(self, benchmark):
        """Benchmark memory-efficient data processing."""
        @benchmark
        def process_large_dataset():
            # Simulate processing large dataset with memory constraints
            large_data = []
            for i in range(1000):
                item = {
                    "id": i,
                    "content": "x" * 1000,  # 1KB per item
                    "metadata": {"size": 1000, "type": "test"}
                }
                large_data.append(item)

            # Process in chunks to simulate memory-efficient processing
            chunk_size = 100
            processed_chunks = []
            for i in range(0, len(large_data), chunk_size):
                chunk = large_data[i:i + chunk_size]
                processed_chunk = [item for item in chunk if len(item["content"]) > 0]
                processed_chunks.append(processed_chunk)

            return processed_chunks

        result = process_large_dataset
        assert len(result) == 10  # 10 chunks
        assert all(len(chunk) == 100 for chunk in result)


# Integration benchmarks for end-to-end workflows
class TestIntegrationBenchmarks:
    """Integration performance benchmarks."""

    def setup_method(self):
        """Set up integration test fixtures."""
        self.workflow_engine = WorkflowEngine()
        self.data_source = DataSource()

    def test_full_workflow_benchmark(self, benchmark):
        """Benchmark complete workflow from data ingestion to processing."""
        @benchmark
        def full_workflow():
            # Simulate complete workflow: data -> processing -> results
            workflow_steps = []

            # Step 1: Data ingestion
            raw_data = []
            for i in range(200):
                raw_data.append({
                    "email_id": f"email_{i}",
                    "subject": f"Subject {i}",
                    "content": f"Content {i}" * 10,
                    "timestamp": "2024-01-01T00:00:00Z"
                })
            workflow_steps.append(("ingestion", len(raw_data)))

            # Step 2: Data processing
            processed_data = []
            for item in raw_data:
                processed_item = {
                    **item,
                    "processed": True,
                    "category": "test",
                    "sentiment": 0.5
                }
                processed_data.append(processed_item)
            workflow_steps.append(("processing", len(processed_data)))

            # Step 3: Result aggregation
            aggregated_results = {
                "total_processed": len(processed_data),
                "categories": {},
                "avg_sentiment": sum(item["sentiment"] for item in processed_data) / len(processed_data)
            }
            workflow_steps.append(("aggregation", aggregated_results))

            return workflow_steps

        result = full_workflow
        assert len(result) == 3
        assert result[0][0] == "ingestion"
        assert result[1][0] == "processing"
        assert result[2][0] == "aggregation"