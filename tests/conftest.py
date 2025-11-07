"""Pytest configuration and fixtures for EmailIntelligence tests."""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Add setup directory to path for imports
SETUP_DIR = ROOT_DIR / "setup"
sys.path.insert(0, str(SETUP_DIR))


@pytest.fixture
def project_root():
    """Fixture providing the project root directory."""
    return ROOT_DIR


@pytest.fixture
def setup_dir():
    """Fixture providing the setup directory."""
    return SETUP_DIR
