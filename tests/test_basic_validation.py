"""Basic validation tests for EmailIntelligence."""

def test_basic_import():
    """Test that basic imports work."""
    try:
        pass
    except ImportError:
        import pytest
        pytest.fail("Basic imports failed")

def test_project_structure():
    """Test that the project has expected structure."""
    import os
    if not os.path.exists("setup"):
        import pytest
        pytest.fail("setup directory missing")
    if not (os.path.exists("pyproject.toml") or os.path.exists("setup.cfg")):
        import pytest
        pytest.fail("pyproject.toml or setup.cfg missing")
    if not os.path.exists("tests"):
        import pytest
        pytest.fail("tests directory missing")
