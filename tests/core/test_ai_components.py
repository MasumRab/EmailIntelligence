import pytest
from unittest.mock import MagicMock, AsyncMock

from src.core.ai_engine import ModernAIEngine
from src.core.dynamic_model_manager import DynamicModelManager
from src.core.model_registry import ModelRegistry
from src.core.smart_filter_manager import SmartFilterManager

@pytest.mark.asyncio
async def test_modern_ai_engine_dependency_injection():
    """
    Tests that ModernAIEngine correctly accepts a DynamicModelManager instance.
    """
    mock_model_manager = MagicMock(spec=DynamicModelManager)
    engine = ModernAIEngine(model_manager=mock_model_manager)
    assert engine._model_manager is mock_model_manager

@pytest.mark.asyncio
async def test_dynamic_model_manager_dependency_injection():
    """
    Tests that DynamicModelManager correctly accepts a ModelRegistry instance.
    """
    mock_model_registry = MagicMock(spec=ModelRegistry)
    manager = DynamicModelManager(registry=mock_model_registry)
    assert manager.registry is mock_model_registry

@pytest.mark.asyncio
async def test_smart_filter_manager_instantiation():
    """
    Tests that SmartFilterManager can be instantiated without a global instance.
    """
    manager = SmartFilterManager(db_path=":memory:")
    assert manager is not None
    await manager.close()

@pytest.mark.asyncio
async def test_modern_ai_engine_initialization():
    """
    Tests the initialization of the ModernAIEngine.
    """
    mock_model_manager = AsyncMock(spec=DynamicModelManager)
    engine = ModernAIEngine(model_manager=mock_model_manager)
    await engine.initialize()
    mock_model_manager.initialize.assert_called_once()
    assert engine._initialized

@pytest.mark.asyncio
async def test_modern_ai_engine_health_check_unhealthy():
    """
    Tests the health check of the ModernAIEngine when the model manager is unhealthy.
    """
    mock_model_manager = AsyncMock(spec=DynamicModelManager)
    mock_model_manager.get_available_models.side_effect = RuntimeError("Model manager is down")
    engine = ModernAIEngine(model_manager=mock_model_manager)
    engine.analyze_email = AsyncMock(side_effect=RuntimeError("Analysis engine is down"))
    await engine.initialize()
    health_status = await engine.health_check()
    assert health_status["status"] == "unhealthy"

@pytest.mark.asyncio
async def test_modern_ai_engine_health_check_healthy():
    """
    Tests the health check of the ModernAIEngine when everything is healthy.
    """
    mock_model_manager = AsyncMock(spec=DynamicModelManager)
    mock_model_manager.get_available_models.return_value = ["model1"]
    engine = ModernAIEngine(model_manager=mock_model_manager)
    engine.analyze_email = AsyncMock()
    await engine.initialize()
    health_status = await engine.health_check()
    assert health_status["status"] == "healthy"
