from src.core.ai_engine import get_active_ai_engine
from modules.default_ai_engine.engine import DefaultAIEngine

def test_default_ai_engine_is_active(client):  # client fixture to ensure app is initialized
    """
    Tests that the DefaultAIEngine is set as the active AI engine
    when the application starts up.
    """
    active_engine = get_active_ai_engine()
    assert isinstance(active_engine, DefaultAIEngine)