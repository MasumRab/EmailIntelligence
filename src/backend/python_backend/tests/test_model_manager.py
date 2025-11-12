import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.backend.python_backend.model_manager import ModelManager


@pytest.fixture
def model_manager():
    """Provides a clean ModelManager instance for each test."""
    return ModelManager()


def test_discover_models_success(model_manager):
    """Tests that models are correctly discovered from JSON config files."""
    mock_sentiment_config = {
        "name": "sentiment-test",
        "module": "test.sentiment_module",
        "class": "TestSentimentModel",
    }
    mock_topic_config = {
        "name": "topic-test",
        "module": "test.topic_module",
        "class": "TestTopicModel",
    }

    m = mock_open()
    m.side_effect = [
        mock_open(read_data=json.dumps(mock_sentiment_config)).return_value,
        mock_open(read_data=json.dumps(mock_topic_config)).return_value,
    ]

    with (
        patch("os.path.exists", return_value=True),
        patch("os.listdir", return_value=["sentiment-test.json", "topic-test.json"]),
        patch("builtins.open", m),
    ):
        model_manager.discover_models()

        assert len(model_manager.list_models()) == 2
        assert "sentiment-test" in model_manager._model_metadata
        assert "topic-test" in model_manager._model_metadata
        assert (
            model_manager._model_metadata["sentiment-test"]["module"]
            == "test.sentiment_module"
        )


def test_discover_models_file_not_found(model_manager):
    """Tests that model discovery handles a missing directory gracefully."""
    with patch("os.path.exists", return_value=False):
        model_manager.discover_models()
        assert len(model_manager.list_models()) == 0


@patch("importlib.import_module")
def test_load_model_success(mock_import_module, model_manager):
    """Tests that a model is loaded dynamically using importlib."""
    model_name = "sentiment-test"
    model_meta = {
        "name": model_name,
        "module": "test.sentiment_module",
        "status": "unloaded",
    }
    model_manager._model_metadata[model_name] = model_meta

    # Mock the imported module and class
    mock_module = MagicMock()
    mock_class = MagicMock()
    mock_import_module.return_value = mock_module
    setattr(mock_module, "TestSentimentModel", mock_class)

    model_manager.load_model(model_name)

    mock_import_module.assert_called_once_with("test.sentiment_module")
    mock_class.assert_called_once()
    assert model_name in model_manager._models
    assert model_manager._model_metadata[model_name]["status"] == "loaded"


def test_load_nonexistent_model(model_manager):
    """Tests that loading a nonexistent model raises a ValueError."""
    with pytest.raises(ValueError, match="Model 'nonexistent' not found."):
        model_manager.load_model("nonexistent")


def test_get_model_loads_if_unloaded(model_manager):
    """Tests that get_model triggers load_model if the model is not yet loaded."""
    model_name = "sentiment-test"
    model_manager._model_metadata[model_name] = {
        "name": model_name,
        "module": "test.module",
        "class": "TestClass",
        "status": "unloaded",
    }

    with patch.object(model_manager, "load_model") as mock_load_model:
        model_manager.get_model(model_name)
        mock_load_model.assert_called_once_with(model_name)


def test_unload_model(model_manager):
    """Tests that a loaded model can be unloaded."""
    model_name = "sentiment-test"
    model_manager._models[model_name] = "mock_model_instance"
    model_manager._model_metadata[model_name] = {"status": "loaded"}

    model_manager.unload_model(model_name)

    assert model_name not in model_manager._models
    assert model_manager._model_metadata[model_name]["status"] == "unloaded"
