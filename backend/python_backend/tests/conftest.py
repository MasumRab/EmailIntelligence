import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.python_backend.dependencies import _workflow_engine_instance, initialize_services
from backend.python_backend.main import app



# Create a single mock for each manager, scoped to the entire test session.
@pytest.fixture(scope="session")
def mock_db_manager():
    """A session-scoped mock for the DatabaseManager."""
    db_mock = MagicMock()
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
    filter_mock.apply_filters_to_email_data = AsyncMock()
    return filter_mock


@pytest.fixture(scope="session")
def mock_workflow_engine():
    """A session-scoped mock for the WorkflowEngine."""
    workflow_mock = MagicMock()
    workflow_mock.run_workflow = AsyncMock()
    workflow_mock.create_and_register_workflow_from_config = AsyncMock()
    return workflow_mock


@pytest.fixture
def client(mock_db_manager, mock_ai_engine, mock_filter_manager, mock_workflow_engine):
    """
    Provides a TestClient with all external services mocked.
    This fixture resets mocks for each test and handles dependency overrides.
    """
    from backend.python_backend.database import get_db
    from backend.python_backend.dependencies import (
        get_ai_engine,
        get_filter_manager,
        get_workflow_engine,
    )

    # Reset all mocks
    for manager_mock in [
        mock_db_manager,
        mock_ai_engine,
        mock_filter_manager,
        mock_workflow_engine,
    ]:
        manager_mock.reset_mock()
        for attr_name in dir(manager_mock):
            attr = getattr(manager_mock, attr_name)
            if isinstance(attr, (MagicMock, AsyncMock)):
                attr.reset_mock()
                attr.side_effect = None

    # Set up dependency overrides
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_ai_engine] = lambda: mock_ai_engine
    app.dependency_overrides[get_filter_manager] = lambda: mock_filter_manager
    app.dependency_overrides[get_workflow_engine] = lambda: mock_workflow_engine

    decorator_path = "backend.python_backend.performance_monitor.log_performance"
    with patch(decorator_path, lambda *args, **kwargs: (lambda func: func)):
        yield TestClient(app)

    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_real_workflows(mock_db_manager, mock_ai_engine, mock_filter_manager):
    """
    Provides a TestClient with a REAL WorkflowEngine but mocks other services.
    This is for testing the workflow and plugin discovery process.
    """
    from backend.python_backend.database import get_db
    from backend.python_backend.dependencies import (
        get_ai_engine,
        get_filter_manager,
        get_workflow_engine,
    )

    # We are NOT mocking get_workflow_engine here.

    # Reset mocks
    for manager_mock in [mock_db_manager, mock_ai_engine, mock_filter_manager]:
        manager_mock.reset_mock()
        for attr_name in dir(manager_mock):
            attr = getattr(manager_mock, attr_name)
            if isinstance(attr, (MagicMock, AsyncMock)):
                attr.reset_mock()
                attr.side_effect = None

    # Override dependencies
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_ai_engine] = lambda: mock_ai_engine
    app.dependency_overrides[get_filter_manager] = lambda: mock_filter_manager

    # Manually run the startup events to initialize the real workflow engine
    # This is a bit of a hack, but necessary for this kind of integration test.
    async def run_startup():
        await initialize_services()

    # We need to run the async startup event in a sync context for the test fixture
    asyncio.run(run_startup())

    decorator_path = "backend.python_backend.performance_monitor.log_performance"
    with patch(decorator_path, lambda *args, **kwargs: (lambda func: func)):
        yield TestClient(app)

    # Clean up
    app.dependency_overrides.clear()
    # Reset the global instance so other tests are not affected
    global _workflow_engine_instance
    _workflow_engine_instance = None
