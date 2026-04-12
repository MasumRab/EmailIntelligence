from datetime import datetime, timezone
import pytest
from src.context_control.models import ProjectConfig, ContextProfile, AgentContext, ContextValidationResult

def test_project_config_datetime_is_aware():
    config = ProjectConfig(project_name="Test", project_type="web")
    assert config.created_at.tzinfo is not None
    assert config.updated_at.tzinfo is not None

def test_context_profile_datetime_is_aware():
    profile = ContextProfile(id="test", name="Test")
    assert profile.created_at.tzinfo is not None
    assert profile.updated_at.tzinfo is not None

def test_agent_context_datetime_is_aware():
    context = AgentContext(profile_id="test", agent_id="agent", environment_type="dev")
    assert context.activated_at.tzinfo is not None

def test_context_validation_result_datetime_is_aware():
    result = ContextValidationResult(is_valid=True)
    assert result.validated_at.tzinfo is not None
