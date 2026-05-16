import pytest
from backend.python_backend.model_manager import ModelManager

@pytest.fixture
def model_manager():
    return ModelManager()

def test_get_active_models(model_manager):
    assert model_manager.get_active_models() == []

def test_check_health(model_manager):
    assert model_manager.check_health() == True
