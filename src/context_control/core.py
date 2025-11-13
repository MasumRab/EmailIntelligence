"""Core context control functionality for Agent Context Control."""

from pathlib import Path
from typing import Dict, List, Optional

from .config import get_current_config
from .environment import detect_branch, get_current_branch
from .exceptions import ContextNotFoundError
from .logging import get_context_logger
from .models import AgentContext, ContextProfile, ContextValidationResult
from .storage import ProfileStorage

logger = get_context_logger()


class BranchMatcher:
    """Handles branch pattern matching for context profiles."""
    
    @staticmethod
    def matches_pattern(branch_name: str, pattern: str) -> bool:
        """Check if branch name matches a pattern.

        Args:
            branch_name: Branch name to check
            pattern: Pattern to match against (supports wildcards)

        Returns:
            True if matches, False otherwise
        """
        # Simple wildcard matching
        if "*" in pattern:
            # Convert glob pattern to regex
            import fnmatch

            return fnmatch.fnmatch(branch_name, pattern)

        return branch_name == pattern

    @classmethod
    def find_profile_for_branch(cls, branch_name: str, profiles: List[ContextProfile]) -> Optional[ContextProfile]:
        """Find the best matching context profile for a branch.

        Args:
            branch_name: Branch name to match against
            profiles: List of available profiles

        Returns:
            Matching ContextProfile or None
        """
        # First, try exact match
        for profile in profiles:
            if branch_name in profile.branch_patterns:
                return profile

        # Then, try pattern matching
        for profile in profiles:
            for pattern in profile.branch_patterns:
                if cls.matches_pattern(branch_name, pattern):
                    return profile

        # Finally, try default profiles (empty patterns or wildcard)
        for profile in profiles:
            if not profile.branch_patterns or "*" in profile.branch_patterns:
                return profile

        return None


class EnvironmentTypeDetector:
    """Determines environment types based on branch names."""
    
    @staticmethod
    def determine_environment_type(branch_name: str) -> str:
        """Determine the environment type based on branch name.

        Args:
            branch_name: Branch name

        Returns:
            Environment type string
        """
        if branch_name.startswith("main") or branch_name == "master":
            return "production"
        elif branch_name.startswith("develop") or branch_name.startswith("dev"):
            return "development"
        elif branch_name.startswith("staging") or branch_name.startswith("stage"):
            return "staging"
        elif branch_name.startswith("feature/") or branch_name.startswith("bugfix/"):
            return "development"
        elif branch_name.startswith("release/"):
            return "staging"
        elif branch_name.startswith("detached-"):
            return "detached"
        else:
            return "development"


class ContextFileResolver:
    """Resolves file access permissions for contexts."""
    
    @staticmethod
    def resolve_accessible_files(profile: ContextProfile) -> List[str]:
        """Resolve the list of accessible files for a profile.

        Args:
            profile: ContextProfile to resolve files for

        Returns:
            List of accessible file paths/patterns
        """
        # For now, return allowed files directly
        # In future, this could resolve globs, check permissions, etc.
        return profile.allowed_files

    @staticmethod
    def resolve_restricted_files(profile: ContextProfile) -> List[str]:
        """Resolve the list of restricted files for a profile.

        Args:
            profile: ContextProfile to resolve files for

        Returns:
            List of restricted file paths/patterns
        """
        return profile.blocked_files


class ContextValidator:
    """Validates agent contexts for consistency and security."""
    
    @staticmethod
    def validate_context(context: AgentContext) -> ContextValidationResult:
        """Validate an agent context for consistency and security.

        Args:
            context: AgentContext to validate

        Returns:
            ContextValidationResult with validation status
        """
        errors = []
        warnings = []

        # Check that profile exists by loading it directly
        # Note: This would ideally use a profile service, but we'll keep the existing logic for now
        from .core import ContextController
        controller = ContextController()
        profile = None
        for p in controller._load_all_profiles():
            if p.id == context.profile_id:
                profile = p
                break

        if not profile:
            errors.append(f"Context profile '{context.profile_id}' not found")
        else:
            # Verify profile matches the context's branch if we have one
            if context.branch_name:
                profile_for_branch = BranchMatcher.find_profile_for_branch(context.branch_name, [profile])
                if profile_for_branch and profile_for_branch.id != context.profile_id:
                    errors.append(
                        f"Context profile ID mismatch for branch '{context.branch_name}': expected {profile_for_branch.id}, got {context.profile_id}"
                    )

        # Check for conflicting file permissions
        accessible_set = set(context.accessible_files)
        restricted_set = set(context.restricted_files)
        conflicts = accessible_set & restricted_set

        if conflicts:
            errors.append(f"Conflicting file permissions: {conflicts}")

        # Check agent ID format
        if not context.agent_id or not context.agent_id.strip():
            errors.append("Invalid agent ID")

        return ContextValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            context_id=context.profile_id,
        )


class ContextCreator:
    """Creates agent contexts from profiles and environment information."""
    
    def __init__(self, config=None):
        """Initialize the context creator.

        Args:
            config: Configuration instance
        """
        self.config = config or get_current_config()
    
    def create_context(
        self, 
        profile: ContextProfile, 
        branch_name: Optional[str], 
        agent_id: str
    ) -> AgentContext:
        """Create an agent context from a profile and environment info.

        Args:
            profile: The context profile to use
            branch_name: Branch name (can be None for detached HEAD)
            agent_id: Unique identifier for the agent

        Returns:
            AgentContext instance
        """
        # Load project configuration - prefer profile config, fallback to directory
        if profile.project_config:
            project_config = profile.project_config
        else:
            # Create a project loader with our config
            from .project import ProjectConfigLoader

            loader = ProjectConfigLoader(self.config)
            project_config = loader.load_project_config()

        # Determine environment type
        environment_type = EnvironmentTypeDetector.determine_environment_type(branch_name or "detached")

        # Create agent context
        context = AgentContext(
            profile_id=profile.id,
            agent_id=agent_id,
            branch_name=get_current_branch(),  # Only set if on a branch
            environment_type=environment_type,
            accessible_files=ContextFileResolver.resolve_accessible_files(profile),
            restricted_files=ContextFileResolver.resolve_restricted_files(profile),
            agent_settings=profile.agent_settings,  # Inherit agent settings from profile
        )

        # Attach project config to context for agent adaptation
        # Note: This extends the context object dynamically
        context.profile_config = project_config

        logger.info(f"Created context for branch '{branch_name}', agent '{agent_id}'")
        return context


class ContextController:
    """Main controller for agent context management."""

    def __init__(self, config=None):
        """Initialize the context controller.

        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()
        # Ensure global config is set for components that need it
        if (
            config
            and not hasattr(get_current_config, "_config")
            or get_current_config.__globals__.get("_config") is None
        ):
            from .config import init_config

            init_config(
                override_config=(
                    self.config.dict() if hasattr(self.config, "dict") else None
                )
            )
        self.storage = ProfileStorage(self.config)
        self._context_cache: Dict[str, AgentContext] = {}
        self._creator = ContextCreator(self.config)
        logger.info("Context controller initialized")

    def get_context_for_branch(
        self, branch_name: Optional[str] = None, agent_id: str = "default"
    ) -> AgentContext:
        """Get the appropriate context for a given branch and agent.

        Args:
            branch_name: Branch name to get context for. If None, detects current branch.
            agent_id: Unique identifier for the agent

        Returns:
            AgentContext instance for the branch/agent combination

        Raises:
            ContextNotFoundError: If no suitable context profile is found
        """
        # Ensure branch_name is a string
        if branch_name is None:
            branch_name = detect_branch()

        cache_key = f"{branch_name}:{agent_id}"

        # Check cache first
        if cache_key in self._context_cache:
            cached_context = self._context_cache[cache_key]
            logger.debug(f"Returning cached context for {cache_key}")
            return cached_context

        # Find matching profile
        assert isinstance(branch_name, str), "branch_name must be a string"
        profile = self._find_profile_for_branch(branch_name)
        if not profile:
            raise ContextNotFoundError(
                f"No context profile found for branch '{branch_name}'",
                context_id=branch_name,
            )

        # Create context using the dedicated creator
        context = self._creator.create_context(profile, branch_name, agent_id)

        # Cache the context
        self._context_cache[cache_key] = context

        return context

    def _find_profile_for_branch(self, branch_name: str) -> Optional[ContextProfile]:
        """Find the best matching context profile for a branch.

        Args:
            branch_name: Branch name to match against

        Returns:
            Matching ContextProfile or None
        """
        profiles = self._load_all_profiles()
        return BranchMatcher.find_profile_for_branch(branch_name, profiles)

    def _load_all_profiles(self) -> List[ContextProfile]:
        """Load all available context profiles.

        Returns:
            List of ContextProfile instances
        """
        return self.storage.load_all_profiles()

    def validate_context(self, context: AgentContext) -> ContextValidationResult:
        """Validate an agent context for consistency and security.

        Args:
            context: AgentContext to validate

        Returns:
            ContextValidationResult with validation status
        """
        return ContextValidator.validate_context(context)

    def clear_cache(self):
        """Clear all cached profiles and contexts."""
        self.storage.clear_cache()
        self._context_cache.clear()
        logger.info("Cache cleared")
