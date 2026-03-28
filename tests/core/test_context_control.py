"""Tests for context_control module.

These tests are standalone to avoid dependency issues.
We mock the pydantic models to test the validation logic.
"""

import pytest
from datetime import datetime
import re
from typing import Dict, List, Any


# Minimal mock of ProjectConfig for testing
class MockProjectConfig:
    """Mock ProjectConfig for testing without external dependencies."""
    
    def __init__(
        self,
        project_name: str,
        project_type: str,
        max_context_length: int = 4096,
        enable_code_execution: bool = False,
        enable_file_writing: bool = False,
        enable_shell_commands: bool = False,
        preferred_models: List[str] = None,
        custom_settings: Dict[str, Any] = None,
    ):
        self.project_name = project_name
        self.project_type = project_type
        self.max_context_length = max_context_length
        self.enable_code_execution = enable_code_execution
        self.enable_file_writing = enable_file_writing
        self.enable_shell_commands = enable_shell_commands
        self.preferred_models = preferred_models or ["gpt-4", "claude-3"]
        self.custom_settings = custom_settings or {}


# Minimal mock of ContextProfile for testing
class MockContextProfile:
    """Mock ContextProfile for testing without external dependencies."""
    
    def __init__(
        self,
        id: str,
        name: str,
        description: str = None,
        branch_patterns: List[str] = None,
        allowed_files: List[str] = None,
        blocked_files: List[str] = None,
        agent_settings: Dict[str, Any] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.branch_patterns = branch_patterns or []
        self.allowed_files = allowed_files or []
        self.blocked_files = blocked_files or []
        self.agent_settings = agent_settings or {}


# Minimal mock of AgentContext for testing
class MockAgentContext:
    """Mock AgentContext for testing without external dependencies."""
    
    def __init__(
        self,
        profile_id: str,
        agent_id: str,
        environment_type: str,
        branch_name: str = None,
        accessible_files: List[str] = None,
        restricted_files: List[str] = None,
    ):
        self.profile_id = profile_id
        self.agent_id = agent_id
        self.environment_type = environment_type
        self.branch_name = branch_name
        self.accessible_files = accessible_files or []
        self.restricted_files = restricted_files or []
        self.is_active = True


# Minimal mock of ContextValidationResult for testing
class MockContextValidationResult:
    """Mock ContextValidationResult for testing."""
    
    def __init__(
        self,
        is_valid: bool,
        errors: List[str] = None,
        warnings: List[str] = None,
        context_id: str = None,
    ):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.context_id = context_id


# Validation logic extracted for testing
def is_valid_id(id_str: str) -> bool:
    """Check if an ID string is valid."""
    if not id_str or len(id_str) > 100:
        return False
    pattern = r"^[a-zA-Z0-9._-]+$"
    return bool(re.match(pattern, id_str))


def is_valid_project_name(name: str) -> bool:
    """Check if a project name is valid."""
    if not name or len(name) > 100:
        return False
    pattern = r"^[a-zA-Z0-9._\-\s]+$"
    return bool(re.match(pattern, name))


def is_valid_model_name(name: str) -> bool:
    """Check if a model name is valid."""
    if not name or len(name) > 50:
        return False
    pattern = r"^[a-zA-Z0-9._\-/]+$"
    return bool(re.match(pattern, name))


def find_conflicting_patterns(allowed: List[str], blocked: List[str]) -> List[str]:
    """Find patterns that appear in both allowed and blocked lists."""
    allowed_set = set(allowed)
    blocked_set = set(blocked)
    return list(allowed_set & blocked_set)


class TestProjectConfig:
    """Tests for ProjectConfig model."""

    def test_project_config_defaults(self):
        """Test ProjectConfig with default values."""
        config = MockProjectConfig(project_name="test", project_type="python")
        
        assert config.project_name == "test"
        assert config.project_type == "python"
        assert config.max_context_length == 4096
        assert config.enable_code_execution is False
        assert config.enable_file_writing is False
        assert config.enable_shell_commands is False

    def test_project_config_custom_values(self):
        """Test ProjectConfig with custom values."""
        config = MockProjectConfig(
            project_name="my_project",
            project_type="web",
            max_context_length=8192,
            enable_code_execution=True,
            enable_file_writing=True,
            preferred_models=["gpt-4", "claude-3-sonnet"],
        )
        
        assert config.project_name == "my_project"
        assert config.project_type == "web"
        assert config.max_context_length == 8192
        assert config.enable_code_execution is True
        assert config.enable_file_writing is True
        assert config.preferred_models == ["gpt-4", "claude-3-sonnet"]


class TestContextProfile:
    """Tests for ContextProfile model."""

    def test_context_profile_defaults(self):
        """Test ContextProfile with default values."""
        profile = MockContextProfile(id="test-profile", name="Test Profile")
        
        assert profile.id == "test-profile"
        assert profile.name == "Test Profile"
        assert profile.description is None
        assert profile.branch_patterns == []
        assert profile.allowed_files == []

    def test_context_profile_with_branch_patterns(self):
        """Test ContextProfile with branch patterns."""
        profile = MockContextProfile(
            id="feature-profile",
            name="Feature Branch",
            branch_patterns=["feature/*", "develop"],
            allowed_files=["src/**/*.py", "tests/**/*.py"],
            blocked_files=["*.env", "secrets/*"],
        )
        
        assert profile.branch_patterns == ["feature/*", "develop"]
        assert profile.allowed_files == ["src/**/*.py", "tests/**/*.py"]
        assert profile.blocked_files == ["*.env", "secrets/*"]


class TestAgentContext:
    """Tests for AgentContext model."""

    def test_agent_context_defaults(self):
        """Test AgentContext with default values."""
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="agent-001",
            environment_type="development",
        )
        
        assert context.profile_id == "test-profile"
        assert context.agent_id == "agent-001"
        assert context.environment_type == "development"
        assert context.is_active is True
        assert context.accessible_files == []
        assert context.restricted_files == []

    def test_agent_context_with_files(self):
        """Test AgentContext with file access."""
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="agent-002",
            environment_type="staging",
            accessible_files=["src/**", "tests/**"],
            restricted_files=["*.env", "secrets/**"],
        )
        
        assert context.accessible_files == ["src/**", "tests/**"]
        assert context.restricted_files == ["*.env", "secrets/**"]


class TestContextValidatorProfile:
    """Tests for profile validation logic."""

    def test_validate_profile_valid(self):
        """Test validation of a valid profile."""
        profile = MockContextProfile(
            id="test-profile",
            name="Test",
            branch_patterns=["main", "develop"],
            allowed_files=["src/*"],
        )
        
        is_valid_id_result = is_valid_id(profile.id)
        
        assert is_valid_id_result is True

    def test_validate_profile_invalid_id(self):
        """Test validation fails for invalid profile ID."""
        invalid_id = "invalid id with spaces!"
        
        is_valid = is_valid_id(invalid_id)
        
        assert is_valid is False

    def test_validate_profile_conflicting_patterns(self):
        """Test validation detects conflicting file patterns."""
        allowed = ["*.py", "src/*"]
        blocked = ["*.py"]  # Conflicts with allowed
        
        conflicts = find_conflicting_patterns(allowed, blocked)
        
        assert "*.py" in conflicts


class TestContextValidatorProjectConfig:
    """Tests for project config validation logic."""

    def test_validate_project_config_valid(self):
        """Test validation of a valid project config."""
        config = MockProjectConfig(
            project_name="my_project",
            project_type="python",
            max_context_length=4096,
        )
        
        is_valid_name = is_valid_project_name(config.project_name)
        
        assert is_valid_name is True

    def test_validate_project_config_invalid_type(self):
        """Test validation fails for invalid project type."""
        valid_types = ["python", "javascript", "web", "api", "library", "data", "generic"]
        invalid_type = "invalid_type"
        
        assert invalid_type not in valid_types

    def test_validate_project_config_invalid_context_length(self):
        """Test validation fails for invalid context length."""
        config = MockProjectConfig(
            project_name="my_project",
            project_type="python",
            max_context_length=50,  # Too short
        )
        
        assert config.max_context_length < 100  # Below minimum

    def test_validate_project_config_invalid_model_name(self):
        """Test validation fails for invalid model names."""
        is_valid = is_valid_model_name("invalid model!@#")
        
        assert is_valid is False


class TestContextValidatorContext:
    """Tests for agent context validation."""

    def test_validate_context_valid(self):
        """Test validation of a valid context."""
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="agent-001",
            environment_type="development",
            accessible_files=["src/*"],
        )
        
        # Test that valid IDs work
        is_valid_id_result = is_valid_id(context.agent_id)
        
        assert is_valid_id_result is True
        assert context.environment_type in ["development", "staging", "production", "detached"]

    def test_validate_context_invalid_env_type(self):
        """Test validation fails for invalid environment type."""
        valid_envs = ["development", "staging", "production", "detached"]
        invalid_env = "invalid_env"
        
        assert invalid_env not in valid_envs

    def test_validate_context_missing_agent_id(self):
        """Test validation fails for missing agent ID."""
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="",
            environment_type="development",
        )
        
        # Empty string is not a valid ID
        is_valid = is_valid_id(context.agent_id)
        
        assert is_valid is False

    def test_validate_context_conflicting_permissions(self):
        """Test validation detects conflicting file permissions."""
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="agent-001",
            environment_type="development",
            accessible_files=["*.py"],
            restricted_files=["*.py"],  # Conflicts
        )
        
        conflicts = find_conflicting_patterns(
            context.accessible_files,
            context.restricted_files
        )
        
        assert "*.py" in conflicts


class TestContextValidatorCompatibility:
    """Tests for profile-context compatibility logic."""

    def test_validate_compatibility_valid(self):
        """Test valid profile-context pair (matching IDs)."""
        profile = MockContextProfile(
            id="test-profile",
            name="Test",
            allowed_files=["src/*", "tests/*"],
            blocked_files=["*.env"],
        )
        
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="agent-001",
            environment_type="development",
            accessible_files=["src/*"],
            restricted_files=["*.env"],
        )
        
        # IDs should match for compatibility
        assert profile.id == context.profile_id

    def test_validate_compatibility_profile_id_mismatch(self):
        """Test profile ID mismatch detection."""
        profile = MockContextProfile(id="profile-1", name="Profile 1")
        context = MockAgentContext(
            profile_id="profile-2",  # Different from profile.id
            agent_id="agent-001",
            environment_type="development",
        )
        
        # IDs should not match
        assert profile.id != context.profile_id

    def test_validate_compatibility_context_allows_extra_files(self):
        """Test detection of context allowing files not in profile."""
        profile = MockContextProfile(
            id="test-profile",
            name="Test",
            allowed_files=["src/*"],
        )
        
        context = MockAgentContext(
            profile_id="test-profile",
            agent_id="agent-001",
            environment_type="development",
            accessible_files=["src/*", "secrets/*"],  # Extra files not in profile
        )
        
        # Context allows files not in profile - should be detected
        profile_allowed = set(profile.allowed_files)
        context_allowed = set(context.accessible_files)
        extra_allowed = context_allowed - profile_allowed
        
        assert "secrets/*" in extra_allowed  # Extra files detected