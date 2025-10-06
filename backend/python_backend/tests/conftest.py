import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock, patch

from backend.python_backend.main import app

# Create a single mock for each manager, scoped to the entire test session.
# This is efficient, and we can reset them in the client fixture for each test.
@pytest.fixture(scope="session")
def mock_db_manager():
    """A session-scoped mock for the DatabaseManager."""
    db_mock = MagicMock()
    # Define all async methods that might be used across any test
    db_mock.get_all_categories = AsyncMock()
    db_mock.create_category = AsyncMock()
    db_mock.search_emails = AsyncMock()
    db_mock.get_emails_by_category = AsyncMock()
    db_mock.get_all_emails = AsyncMock()
    db_mock.get_email_by_id = AsyncMock()
    db_mock.create_email = AsyncMock()
    db_mock.update_email = AsyncMock()
    db_mock.search_emails_by_category = AsyncMock()
    db_mock.get_recent_emails = AsyncMock()
    return db_mock

@pytest.fixture(scope="session")
def mock_ai_engine():
    """A session-scoped mock for the AdvancedAIEngine."""
    ai_mock = MagicMock()
    ai_mock.analyze_email = AsyncMock()
    return ai_mock

@pytest.fixture(scope="session")
def mock_filter_manager():
    """A session-scoped mock for the SmartFilterManager."""
    filter_mock = MagicMock()
    filter_mock.get_active_filters_sorted = MagicMock()
    filter_mock.add_custom_filter = MagicMock()
    filter_mock.create_intelligent_filters = MagicMock()
    filter_mock.prune_ineffective_filters = MagicMock()
    filter_mock.apply_filters_to_email_data = AsyncMock()
    return filter_mock

@pytest.fixture(scope="session")
def mock_workflow_engine():
    """A session-scoped mock for the WorkflowEngine."""
    workflow_mock = MagicMock()
    workflow_mock.run_workflow = AsyncMock()
    return workflow_mock

@pytest.fixture
def client(mock_db_manager, mock_ai_engine, mock_filter_manager, mock_workflow_engine):
    """
    Provides a TestClient with all external services mocked.
    This fixture resets mocks for each test and handles dependency overrides.
    """
    from backend.python_backend.database import get_db
    from backend.python_backend.dependencies import get_ai_engine, get_filter_manager, get_workflow_engine

    # Reset all mocks before each test to ensure isolation
    for manager_mock in [mock_db_manager, mock_ai_engine, mock_filter_manager, mock_workflow_engine]:
        # Reset the main mock object
        manager_mock.reset_mock()
        # Reset all mock attributes on the manager mock
        for attr_name in dir(manager_mock):
            attr = getattr(manager_mock, attr_name)
            if isinstance(attr, (MagicMock, AsyncMock)):
                attr.reset_mock()
                attr.side_effect = None

    # Set up the dependency overrides for the FastAPI app
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_ai_engine] = lambda: mock_ai_engine
    app.dependency_overrides[get_filter_manager] = lambda: mock_filter_manager
    app.dependency_overrides[get_workflow_engine] = lambda: mock_workflow_engine

    # The log_performance decorator is not injected via Depends, so we must patch it
    # in each module where it's used.
    decorator_path = "backend.python_backend.performance_monitor.log_performance"
    with patch(decorator_path, lambda *args, **kwargs: (lambda func: func)):
        yield TestClient(app)

    # Clean up dependency overrides after the test yields
    app.dependency_overrides.clear()