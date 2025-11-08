import pytest
from unittest.mock import patch

@patch('src.backend.python_nlp.smart_retrieval.GmailAIService.__init__')
def test_smart_retrieval_manager_inheritance_and_initialization(mock_super_init):
    """
    Tests that SmartRetrievalManager can be instantiated and correctly inherits from GmailAIService.
    """
    # Arrange
    from src.backend.python_nlp.smart_retrieval import SmartRetrievalManager
    from src.backend.python_nlp.gmail_service import GmailAIService
    mock_super_init.return_value = None

    # Act
    # We patch the methods on the instance that perform external operations (db init)
    # so that the constructor can run without side effects.
    with patch.object(SmartRetrievalManager, '_init_checkpoint_db', return_value=None), \
         patch.object(SmartRetrievalManager, '_load_credentials', return_value=None, create=True), \
         patch.object(SmartRetrievalManager, '_authenticate', return_value=None, create=True):
        manager = SmartRetrievalManager()
        # Manually set attributes that would be set by the parent constructor
        manager.advanced_ai_engine = None
        manager.credentials = None

    # Assert
    assert isinstance(manager, GmailAIService)
    assert hasattr(manager, 'advanced_ai_engine')
    assert hasattr(manager, '_init_checkpoint_db')
    assert hasattr(manager, 'credentials')
