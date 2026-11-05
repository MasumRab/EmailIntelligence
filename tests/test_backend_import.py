import sys
import pytest

def test_import_main_does_not_block():
    """
    Test that importing src.backend.python_backend.main does not block 
    (i.e. uvicorn.run is properly guarded by if __name__ == "__main__":)
    """
    import unittest.mock
    
    with unittest.mock.patch('sqlite3.connect'):
        with unittest.mock.patch('src.core.security.PathValidator.validate_database_path', getattr(sys.modules.get('src.core.security.PathValidator'), 'validate_and_resolve_db_path', lambda x, y: x), create=True):
            with unittest.mock.patch.dict('sys.modules', {'src.backend.python_backend.model_manager': unittest.mock.MagicMock()}):
                import src.backend.python_backend.main
                assert src.backend.python_backend.main.app is not None
