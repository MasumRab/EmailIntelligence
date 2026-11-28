def test_reset_clears_module_global():
    import src.backend.python_backend.dependencies as deps
    deps._workflow_engine_instance = object()
    deps.reset_workflow_engine()
    assert deps._workflow_engine_instance is None
