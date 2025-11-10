"""Pytest configuration and fixtures."""

import pytest
import asyncio
from typing import Generator

from src.config import Settings
from src.services.verification_service import VerificationService
from src.services.auth_service import AuthService, PermissionLevel
from src.models.verification import VerificationProfile


@pytest.fixture
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def verification_service() -> VerificationService:
    """Create a verification service instance."""
    service = VerificationService()

    # Register default profile
    profile = VerificationProfile(
        name="test",
        description="Test profile",
        scenarios=["test_scenario_1", "test_scenario_2"],
        context_checks=["test_check_1"],
    )
    service.register_profile(profile)

    return service


@pytest.fixture
def auth_service() -> AuthService:
    """Create an authentication service instance."""
    service = AuthService()
    return service


@pytest.fixture
def settings() -> Settings:
    """Create settings instance."""
    return Settings(
        environment="test",
        debug=True,
        log_level="DEBUG",
    )


@pytest.fixture(autouse=True)
def reset_logging() -> None:
    """Reset logging between tests."""
    import logging
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
