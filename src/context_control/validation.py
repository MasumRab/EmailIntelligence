"""Comprehensive validation for context control components."""

from typing import List, Dict, Any, Optional
import re

from .models import ContextProfile, AgentContext, ContextValidationResult, ProjectConfig
from .logging import get_context_logger
from .config import get_current_config


logger = get_context_logger()


class ContextValidator:
    """Comprehensive validator for context control components."""

    def __init__(self, config=None):
        """Initialize the context validator.

        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()

    def validate_profile(self, profile: ContextProfile) -> ContextValidationResult:
        """Validate a context profile.

        Args:
            profile: Profile to validate

        Returns:
            Validation result
        """
        errors = []
        warnings = []

        # Validate ID
        if not self._is_valid_id(profile.id):
            errors.append(f"Invalid profile ID: '{profile.id}'")

        # Validate branch patterns
        for pattern in profile.branch_patterns:
            if not self._is_valid_branch_pattern(pattern):
                errors.append(f"Invalid branch pattern: '{pattern}'")

        # Validate file patterns
        for pattern in profile.allowed_files + profile.blocked_files:
            if not self._is_valid_file_pattern(pattern):
                errors.append(f"Invalid file pattern: '{pattern}'")

        # Check for conflicting patterns
        conflicts = self._find_conflicting_patterns(
            profile.allowed_files, profile.blocked_files
        )
        if conflicts:
            errors.append(f"Conflicting file patterns: {conflicts}")

        # Validate agent settings
        if profile.agent_settings:
            setting_errors = self._validate_agent_settings(profile.agent_settings)
            errors.extend(setting_errors)

        return ContextValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            context_id=profile.id,
        )

    def validate_project_config(self, config: ProjectConfig) -> ContextValidationResult:
        """Validate a project configuration.

        Args:
            config: ProjectConfig to validate

        Returns:
            Validation result
        """
        errors = []
        warnings = []

        # Validate project name
        if not config.project_name or not config.project_name.strip():
            errors.append("Project name is required")
        elif not self._is_valid_project_name(config.project_name):
            errors.append(f"Invalid project name: '{config.project_name}'")

        # Validate project type
        valid_types = [
            "python",
            "javascript",
            "web",
            "api",
            "library",
            "data",
            "generic",
        ]
        if config.project_type not in valid_types:
            errors.append(
                f"Invalid project type: '{config.project_type}'. Must be one of {valid_types}"
            )

        # Validate context length
        if config.max_context_length < 100:
            errors.append("Maximum context length must be at least 100")
        elif config.max_context_length > 100000:
            errors.append("Maximum context length cannot exceed 100,000")

        # Validate preferred models
        if not config.preferred_models:
            warnings.append("No preferred models specified")
        else:
            invalid_models = [
                m for m in config.preferred_models if not self._is_valid_model_name(m)
            ]
            if invalid_models:
                errors.append(f"Invalid model names: {invalid_models}")

        # Validate boolean flags make sense for project type
        if config.project_type == "data" and not config.enable_file_writing:
            warnings.append("Data projects typically need file writing enabled")

        if (
            config.project_type in ["python", "javascript"]
            and not config.enable_code_execution
        ):
            warnings.append(
                f"{config.project_type.capitalize()} projects typically need code execution enabled"
            )

        return ContextValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            context_id=f"project_config_{config.project_name}",
        )

    def _is_valid_project_name(self, name: str) -> bool:
        """Check if a project name is valid.

        Args:
            name: Project name to validate

        Returns:
            True if valid, False otherwise
        """
        if not name or len(name) > 100:
            return False

        # Allow alphanumeric, hyphens, underscores, dots, spaces
        import re

        pattern = r"^[a-zA-Z0-9._\-\s]+$"
        return bool(re.match(pattern, name))

    def _is_valid_model_name(self, name: str) -> bool:
        """Check if a model name is valid.

        Args:
            name: Model name to validate

        Returns:
            True if valid, False otherwise
        """
        if not name or len(name) > 50:
            return False

        # Allow common model name patterns
        import re

        pattern = r"^[a-zA-Z0-9._\-/]+$"
        return bool(re.match(pattern, name))

    def validate_context(self, context: AgentContext) -> ContextValidationResult:
        """Validate an agent context.

        Args:
            context: Context to validate

        Returns:
            Validation result
        """
        errors = []
        warnings = []

        # Validate agent ID
        if not context.agent_id or not context.agent_id.strip():
            errors.append("Agent ID is required")
        elif not self._is_valid_id(context.agent_id):
            errors.append(f"Invalid agent ID: '{context.agent_id}'")

        # Validate profile ID
        if not context.profile_id or not context.profile_id.strip():
            errors.append("Profile ID is required")

        # Validate environment type
        valid_env_types = ["development", "staging", "production", "detached"]
        if context.environment_type not in valid_env_types:
            errors.append(f"Invalid environment type: '{context.environment_type}'")

        # Validate file permissions
        conflicts = self._find_conflicting_patterns(
            context.accessible_files, context.restricted_files
        )
        if conflicts:
            errors.append(f"Conflicting file permissions: {conflicts}")

        # Check for empty permissions (warning)
        if not context.accessible_files and not context.restricted_files:
            warnings.append("Context has no file access boundaries")

        # Validate timestamps
        if context.last_validated and context.activated_at > context.last_validated:
            errors.append("Context was validated before activation")

        return ContextValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            context_id=context.profile_id,
        )

    def validate_profile_context_compatibility(
        self, profile: ContextProfile, context: AgentContext
    ) -> ContextValidationResult:
        """Validate compatibility between a profile and context.

        Args:
            profile: Context profile
            context: Agent context

        Returns:
            Validation result
        """
        errors = []
        warnings = []

        # Check profile ID match
        if profile.id != context.profile_id:
            errors.append(
                f"Profile ID mismatch: profile='{profile.id}', context='{context.profile_id}'"
            )

        # Check branch compatibility
        if context.branch_name:
            if not self._branch_matches_profile(context.branch_name, profile):
                errors.append(
                    f"Branch '{context.branch_name}' not compatible with profile '{profile.id}'"
                )

        # Check file permissions alignment
        profile_allowed = set(profile.allowed_files)
        profile_blocked = set(profile.blocked_files)
        context_allowed = set(context.accessible_files)
        context_blocked = set(context.restricted_files)

        # Context should not allow more than profile allows
        extra_allowed = context_allowed - profile_allowed
        if extra_allowed:
            errors.append(
                f"Context allows files not permitted by profile: {extra_allowed}"
            )

        # Context should not block less than profile blocks
        missing_blocks = profile_blocked - context_blocked
        if missing_blocks:
            warnings.append(
                f"Context does not block files blocked by profile: {missing_blocks}"
            )

        return ContextValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            context_id=context.profile_id,
        )

    def _is_valid_id(self, id_str: str) -> bool:
        """Check if an ID string is valid.

        Args:
            id_str: ID to validate

        Returns:
            True if valid, False otherwise
        """
        if not id_str or len(id_str) > 100:
            return False

        # Allow alphanumeric, hyphens, underscores, dots
        pattern = r"^[a-zA-Z0-9._-]+$"
        return bool(re.match(pattern, id_str))

    def _is_valid_branch_pattern(self, pattern: str) -> bool:
        """Check if a branch pattern is valid.

        Args:
            pattern: Pattern to validate

        Returns:
            True if valid, False otherwise
        """
        if not pattern or len(pattern) > 200:
            return False

        # Allow glob patterns with common branch naming
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-/*?"
        )
        return all(c in allowed_chars for c in pattern)

    def _is_valid_file_pattern(self, pattern: str) -> bool:
        """Check if a file pattern is valid.

        Args:
            pattern: Pattern to validate

        Returns:
            True if valid, False otherwise
        """
        if len(pattern) > 500:
            return False

        # Allow common glob patterns
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-/*?[]{}"
        )
        return all(c in allowed_chars for c in pattern)

    def _find_conflicting_patterns(
        self, allowed: List[str], blocked: List[str]
    ) -> List[str]:
        """Find patterns that appear in both allowed and blocked lists.

        Args:
            allowed: List of allowed patterns
            blocked: List of blocked patterns

        Returns:
            List of conflicting patterns
        """
        allowed_set = set(allowed)
        blocked_set = set(blocked)
        return list(allowed_set & blocked_set)

    def _validate_agent_settings(self, settings: Dict[str, Any]) -> List[str]:
        """Validate agent settings.

        Args:
            settings: Settings dictionary to validate

        Returns:
            List of validation errors
        """
        errors = []

        # Add specific validation rules as needed
        # For now, just check for obviously invalid values

        for key, value in settings.items():
            if not isinstance(key, str) or not key.strip():
                errors.append(f"Invalid setting key: '{key}'")

        return errors

    def _branch_matches_profile(
        self, branch_name: str, profile: ContextProfile
    ) -> bool:
        """Check if a branch matches a profile's patterns.

        Args:
            branch_name: Branch name to check
            profile: Profile to check against

        Returns:
            True if matches, False otherwise
        """
        import fnmatch

        for pattern in profile.branch_patterns:
            if fnmatch.fnmatch(branch_name, pattern):
                return True

        return False
