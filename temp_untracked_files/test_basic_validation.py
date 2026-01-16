"""Basic validation tests for EmailIntelligence."""

def test_basic_import():
    """Test that basic imports work."""
    try:
        import os
        import sys
        assert True
    except ImportError:
        assert False, "Basic imports failed"

def test_project_structure():
    """Test that the project has expected structure."""
    import os
    assert os.path.exists("setup")
    assert os.path.exists("pyproject.toml")
    assert os.path.exists("tests")
