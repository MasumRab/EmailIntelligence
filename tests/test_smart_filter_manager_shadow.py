import os

def test_smart_filter_manager_shadow():
    """
    Test that the stub module `src/backend/python_backend/smart_filters.py`
    has been removed and does not exist.
    """
    stub_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "src",
        "backend",
        "python_backend",
        "smart_filters.py"
    )
    assert not os.path.exists(stub_path), f"Stub file still exists at {stub_path}"
