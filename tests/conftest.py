"""
Advanced test configuration and fixtures for scientific testing methodologies.

This conftest.py provides comprehensive testing infrastructure including:
- Property-based testing configuration
- Performance benchmarking setup
- Advanced mocking fixtures
- Integration testing utilities
- Mutation testing support
"""

import pytest
import asyncio
from typing import Dict, Any, List, Generator
from unittest.mock import MagicMock, AsyncMock
import tempfile
import os
from pathlib import Path

from hypothesis import settings, Phase
import pytest_asyncio

# Hypothesis configuration for property-based testing
settings.register_profile(
    "ci",
    settings(
        max_examples=100,  # More examples in CI for thorough testing
        deadline=None,     # No time limits in CI
        phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.target],
        stateful_step_count=50,
    )
)
settings.register_profile(
    "dev",
    settings(
        max_examples=10,   # Fewer examples during development
        deadline=1000,     # 1 second deadline per test
        phases=[Phase.explicit, Phase.reuse, Phase.generate],
    )
)

# Load appropriate profile
settings.load_profile("ci" if os.getenv("CI") else "dev")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_workflow_engine():
    """Mock WorkflowEngine for testing."""
    mock_engine = MagicMock()
    mock_engine.create_workflow.return_value = {"id": "test_workflow", "status": "created"}
    mock_engine.execute_workflow.return_value = {"status": "completed", "results": []}
    mock_engine.get_workflow_status.return_value = {"status": "running", "progress": 50}
    return mock_engine


@pytest.fixture
def mock_data_source():
    """Mock DataSource for testing."""
    mock_ds = MagicMock()
    mock_ds.query_emails.return_value = [
        {"id": "1", "subject": "Test Email", "content": "Test content"}
    ]
    mock_ds.get_email_count.return_value = 42
    mock_ds.get_categories.return_value = ["work", "personal", "spam"]
    return mock_ds


@pytest.fixture
def mock_ai_engine():
    """Mock AI engine for testing."""
    mock_ai = MagicMock()
    mock_ai.analyze_sentiment.return_value = {"sentiment": "positive", "confidence": 0.85}
    mock_ai.analyze_topic.return_value = {"topic": "business", "confidence": 0.72}
    mock_ai.analyze_intent.return_value = {"intent": "inquiry", "confidence": 0.68}
    return mock_ai


@pytest.fixture
async def async_mock_data_source():
    """Async mock DataSource for async testing."""
    mock_ds = AsyncMock()
    mock_ds.query_emails.return_value = [
        {"id": "1", "subject": "Async Test Email", "content": "Async test content"}
    ]
    mock_ds.get_email_count.return_value = 24
    mock_ds.get_categories.return_value = ["async_work", "async_personal"]
    return mock_ds


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return [
        {
            "id": "email_1",
            "subject": "Meeting Request",
            "content": "Let's schedule a meeting for tomorrow at 2 PM.",
            "sender": "boss@company.com",
            "timestamp": "2024-01-01T10:00:00Z",
            "category": "work"
        },
        {
            "id": "email_2",
            "subject": "Weekend Plans",
            "content": "Hey, want to go hiking this weekend?",
            "sender": "friend@example.com",
            "timestamp": "2024-01-01T15:30:00Z",
            "category": "personal"
        },
        {
            "id": "email_3",
            "subject": "Special Offer",
            "content": "Get 50% off on all products!",
            "sender": "spam@marketing.com",
            "timestamp": "2024-01-01T20:00:00Z",
            "category": "spam"
        }
    ]


@pytest.fixture
def large_email_dataset():
    """Large dataset for performance testing."""
    emails = []
    for i in range(1000):
        emails.append({
            "id": f"email_{i}",
            "subject": f"Subject {i}",
            "content": f"Content {i} with some additional text to make it longer.",
            "sender": f"user{i}@example.com",
            "timestamp": f"2024-01-{str(i % 28 + 1).zfill(2)}T{str(i % 24).zfill(2)}:00:00Z",
            "category": ["work", "personal", "spam"][i % 3]
        })
    return emails


@pytest.fixture
def mock_database_session():
    """Mock database session for testing."""
    mock_session = MagicMock()
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.rollback.return_value = None
    mock_session.close.return_value = None

    # Context manager support
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=None)

    return mock_session


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for testing."""
    mock_redis = MagicMock()
    mock_redis.get.return_value = b"test_value"
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = 1
    mock_redis.exists.return_value = True
    mock_redis.expire.return_value = True
    return mock_redis


@pytest.fixture
def integration_test_config():
    """Configuration for integration tests."""
    return {
        "database_url": "sqlite:///:memory:",
        "redis_url": "redis://localhost:6379/1",
        "api_base_url": "http://localhost:8000",
        "test_timeout": 30,
        "enable_performance_monitoring": True,
        "enable_audit_logging": True
    }


@pytest.fixture(scope="session")
def performance_baseline():
    """Performance baseline data for regression testing."""
    return {
        "workflow_creation_time": 0.001,  # seconds
        "email_query_time": 0.005,
        "ai_analysis_time": 0.1,
        "database_query_time": 0.002,
        "memory_usage_mb": 50,
        "cpu_usage_percent": 5
    }


# Custom markers for advanced testing
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "property_test: marks tests as property-based tests")
    config.addinivalue_line("markers", "integration_test: marks tests as integration tests")
    config.addinivalue_line("markers", "performance_test: marks tests as performance benchmarks")
    config.addinivalue_line("markers", "mutation_test: marks tests for mutation testing")
    config.addinivalue_line("markers", "scientific_test: marks tests using scientific methodologies")


# Hypothesis strategies for common test data
from hypothesis import strategies as st

email_strategy = st.builds(
    dict,
    id=st.text(min_size=1, max_size=50),
    subject=st.text(min_size=1, max_size=200),
    content=st.text(min_size=1, max_size=1000),
    sender=st.emails(),
    category=st.sampled_from(["work", "personal", "spam", "news", "social"])
)

workflow_config_strategy = st.builds(
    dict,
    name=st.text(min_size=1, max_size=100),
    nodes=st.lists(
        st.builds(dict, id=st.text(min_size=1, max_size=20), type=st.text(min_size=1, max_size=20)),
        min_size=1, max_size=20
    )
)


# Mutation testing utilities
@pytest.fixture
def mutation_test_config():
    """Configuration for mutation testing."""
    return {
        "paths_to_mutate": ["src/backend"],
        "tests_dir": "tests",
        "output_format": "html",
        "runner": "pytest",
        "exclude_files": ["__init__.py", "conftest.py"],
        "dict_synonyms": ["dict", "Dict", "Mapping"]
    }


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Clean up temporary files created during tests."""
    yield
    # Cleanup logic would go here if needed


# Test data factories for complex objects
@pytest.fixture
def email_factory():
    """Factory for creating test email objects."""
    def _create_email(**kwargs):
        defaults = {
            "id": "test_email_1",
            "subject": "Test Subject",
            "content": "Test content for email",
            "sender": "test@example.com",
            "timestamp": "2024-01-01T00:00:00Z",
            "category": "test"
        }
        defaults.update(kwargs)
        return defaults
    return _create_email


@pytest.fixture
def workflow_factory():
    """Factory for creating test workflow objects."""
    def _create_workflow(**kwargs):
        defaults = {
            "id": "test_workflow_1",
            "name": "Test Workflow",
            "status": "created",
            "nodes": [
                {"id": "node_1", "type": "input", "status": "pending"},
                {"id": "node_2", "type": "process", "status": "pending"},
                {"id": "node_3", "type": "output", "status": "pending"}
            ],
            "created_at": "2024-01-01T00:00:00Z"
        }
        defaults.update(kwargs)
        return defaults
    return _create_workflow