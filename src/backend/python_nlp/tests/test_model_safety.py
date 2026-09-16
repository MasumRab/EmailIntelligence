import pytest
from unittest.mock import patch
from backend.python_nlp.nlp_engine import NLPEngine
from core.model_registry import ModelRegistry, ModelMetadata, ModelType
from pathlib import Path

@patch("os.path.exists", return_value=True)
@patch("backend.python_nlp.nlp_engine.verify_model_safety", return_value=False)
@patch("backend.python_nlp.nlp_engine.joblib.load")
def test_nlp_engine_load_model_rejects_unsafe(mock_load, mock_verify, mock_exists):
    """Test that NLPEngine rejects unsafe model paths without loading."""
    engine = NLPEngine()
    result = engine._load_model("/unsafe/path.pkl")
    assert result is None
    mock_verify.assert_called_once_with("/unsafe/path.pkl", expected_hash=None)
    mock_load.assert_not_called()

@patch("os.path.exists", return_value=True)
@patch("backend.python_nlp.nlp_engine.verify_model_safety", return_value=True)
@patch("backend.python_nlp.nlp_engine.joblib.load")
def test_nlp_engine_load_model_accepts_safe(mock_load, mock_verify, mock_exists):
    """Test that NLPEngine loads safe model paths."""
    mock_load.return_value = "safe_model"
    engine = NLPEngine()
    result = engine._load_model("/safe/path.pkl")
    assert result == "safe_model"
    mock_verify.assert_called_once_with("/safe/path.pkl", expected_hash=None)
    mock_load.assert_called_once_with("/safe/path.pkl")

@pytest.mark.asyncio
@patch("pathlib.Path.exists", return_value=True)
@patch("core.model_registry.verify_model_safety", return_value=False)
@patch("core.model_registry.joblib.load")
async def test_model_registry_load_sklearn_rejects_unsafe(mock_load, mock_verify, mock_exists):
    """Test that ModelRegistry rejects unsafe sklearn models during load."""
    registry = ModelRegistry()
    metadata = ModelMetadata(model_id="test", model_type=ModelType.CUSTOM, name="test", version="1", path=Path("/unsafe"), framework="sklearn")
    result = await registry._load_sklearn_model(metadata)
    assert result is None
    mock_verify.assert_called_once_with(Path("/unsafe/test.pkl"), expected_hash=None)
    mock_load.assert_not_called()

@pytest.mark.asyncio
@patch("pathlib.Path.exists", return_value=True)
@patch("core.model_registry.verify_model_safety", return_value=False)
@patch("core.model_registry.joblib.load")
async def test_model_registry_validate_sklearn_rejects_unsafe(mock_load, mock_verify, mock_exists):
    """Test that ModelRegistry rejects unsafe sklearn models during validation."""
    registry = ModelRegistry()
    metadata = ModelMetadata(model_id="test", model_type=ModelType.CUSTOM, name="test", version="1", path=Path("/unsafe"), framework="sklearn")
    result = await registry._validate_model_file(metadata)
    assert result["passed"] is False
    assert "Model path failed safety verification" in result["issues"]
    mock_verify.assert_called_once_with(Path("/unsafe/test.pkl"), expected_hash=None)
    mock_load.assert_not_called()
