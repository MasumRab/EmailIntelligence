"""Basic validation tests for EmailIntelligence."""


def test_basic_import():
    """Test that basic imports work."""
    try:
        # Test core module imports
        from src.core import models, interfaces, exceptions  # noqa: F401
        from src.git import conflict_detector, repository, worktree  # noqa: F401
        from src.cli import commands, arguments  # noqa: F401
        from src.utils import logger  # noqa: F401

        assert True, "All basic imports succeeded"
    except ImportError as e:
        assert False, f"Basic imports failed: {e}"


def test_project_structure():
    """Test that the project has expected structure."""
    import os

    assert os.path.exists("setup")
    assert os.path.exists("pyproject.toml")
    assert os.path.exists("tests")
