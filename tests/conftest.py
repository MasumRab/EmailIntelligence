from unittest.mock import AsyncMock

import pytest

from server.python_backend.database import get_db  # The actual dependency
from server.python_backend.main import \
    app  # Assuming 'app' is your FastAPI instance


@pytest.fixture(scope="session", autouse=True)
def mock_db_session_override():
    # Create a single AsyncMock instance for the session
    mock_db = AsyncMock()
    # Pre-configure any commonly returned objects or default behaviors if necessary
    # For example, if many methods return a list:
    # mock_db.get_all_categories = AsyncMock(return_value=[])
    # mock_db.get_emails = AsyncMock(return_value=[])
    # ... etc. Specific tests can override these.

    # This is the dependency that needs to be overridden
    # Ensure this path is correct for your project structure
    original_get_db_override = app.dependency_overrides.get(
        get_db
    )  # Store original override, if any

    # Define the override function that will return our session-scoped mock
    async def override_get_db_for_session():
        return mock_db

    app.dependency_overrides[get_db] = override_get_db_for_session

    yield mock_db  # Provide the mock to tests if they request it by this fixture name

    # Teardown: Restore original dependency override if it existed, or clear it
    if original_get_db_override:
        app.dependency_overrides[get_db] = original_get_db_override
    else:
        if get_db in app.dependency_overrides:  # Check if key exists before deleting
            del app.dependency_overrides[get_db]
