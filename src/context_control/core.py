"""Core context control functionality for Agent Context Control."""

from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

from .config import get_current_config, _global_config
from .environment import detect_branch, get_current_branch
from .exceptions import ContextNotFoundError
from .logging import get_context_logger
from .models import AgentContext, ContextProfile, ContextValidationResult
from .storage import ProfileStorage

logger = get_context_logger()


class IBranchMatcher(ABC):
    """Interface for branch matching strategies."""
    
    @abstractmethod
    def find_profile_for_branch(self, branch_name: str, profiles: List[ContextProfile]) -> Optional[ContextProfile]:
        """Find matching profile for branch."""
        pass


class BranchMatcher(IBranchMatcher):
    """Handles branch pattern matching for context profiles."""
    
    def find_profile_for_branch(self, branch_name: str, profiles: List[ContextProfile]) -> Optional[ContextProfile]:
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
                if self._matches_pattern(branch_name, pattern):
                    return profile

        # Finally, try default profiles (empty patterns or wildcard)
        for profile in profiles:
            if not profile.branch_patterns or "*" in profile.branch_patterns:
                return profile

        return None

    def _matches_pattern(self, branch_name: str, pattern: str) -> bool:
        """Check if branch name matches a pattern.

        Args:
            branch_name: Branch name to check
            pattern: Pattern to match against (supports wildcards)

        Returns:
            True if matches, False otherwise
        """
        if "*" in pattern:
            import fnmatch
            return fnmatch.fnmatch(branch_name, pattern)
        return branch_name == pattern


class IEnvironmentDetector(ABC):
    """Interface for environment type detection."""
    
    @abstractmethod
    def determine_environment_type(self, branch_name: str) -> str:
        """Determine environment type from branch name."""
        pass


class EnvironmentTypeDetector(IEnvironmentDetector):
    """Determines environment types based on branch names."""
    
    def determine_environment_type(self, branch_name: str) -> str:
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


class IFileResolver(ABC):
    """Interface for file permission resolution."""
    
    @abstractmethod
    def resolve_accessible_files(self, profile: ContextProfile) -> List[str]:
        """Resolve accessible files for a profile."""
        pass
    
    @abstractmethod
    def resolve_restricted_files(self, profile: ContextProfile) -> List[str]:
        """Resolve restricted files for a profile."""
        pass


class ContextFileResolver(IFileResolver):
    """Resolves file access permissions for contexts."""
    
    def resolve_accessible_files(self, profile: ContextProfile) -> List[str]:
        """Resolve the list of accessible files for a profile.

        Args:
            profile: ContextProfile to resolve files for

        Returns:
            List of accessible file paths/patterns
        """
        return profile.allowed_files

    def resolve_restricted_files(self, profile: ContextProfile) -> List[str]:
        """Resolve the list of restricted files for a profile.

        Args:
            profile: ContextProfile to resolve files for

        Returns:
            List of restricted file paths/patterns
        """
        return profile.blocked_files


class IContextValidator(ABC):
    """Interface for context validation."""
    
    @abstractmethod
    def validate_context(self, context: AgentContext) -> ContextValidationResult:
        """Validate an agent context."""
        pass


class ContextValidator(IContextValidator):
    """Validates agent contexts for consistency and security."""
    
    def __init__(self, branch_matcher: Optional[IBranchMatcher] = None, config=None):
        """Initialize the context validator.

        Args:
            branch_matcher: Optional branch matcher instance
            config: Configuration instance
        """
        self.branch_matcher = branch_matcher or BranchMatcher()
        self.config = config or get_current_config()

    def validate_context(self, context: AgentContext) -> ContextValidationResult:
        """Validate an agent context for consistency and security.

        Args:
            context: AgentContext to validate

        Returns:
            ContextValidationResult with validation status
        """
        errors = []
        warnings = []

        # Check that profile exists
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
                profile_for_branch = self.branch_matcher.find_profile_for_branch(context.branch_name, [profile])
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


class IContextCreator(ABC):
    """Interface for context creation."""
    
    @abstractmethod
    def create_context(self, profile: ContextProfile, branch_name: Optional[str], agent_id: str) -> AgentContext:
        """Create an agent context from profile and environment info."""
        pass


class ContextCreator(IContextCreator):
    """Creates agent contexts from profiles and environment information."""
    
    def __init__(
        self, 
        config=None,
        environment_detector: Optional[IEnvironmentDetector] = None,
        file_resolver: Optional[IFileResolver] = None
    ):
        """Initialize the context creator.

        Args:
            config: Configuration instance
            environment_detector: Optional environment detector
            file_resolver: Optional file resolver
        """
        self.config = config or get_current_config()
        self.environment_detector = environment_detector or EnvironmentTypeDetector()
        self.file_resolver = file_resolver or ContextFileResolver()
    
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
            from .project import ProjectConfigLoader
            loader = ProjectConfigLoader(self.config)
            project_config = loader.load_project_config()

        # Determine environment type
        environment_type = self.environment_detector.determine_environment_type(branch_name or "detached")

        # Create agent context
        context = AgentContext(
            profile_id=profile.id,
            agent_id=agent_id,
            branch_name=get_current_branch(),
            environment_type=environment_type,
            accessible_files=self.file_resolver.resolve_accessible_files(profile),
            restricted_files=self.file_resolver.resolve_restricted_files(profile),
            agent_settings=profile.agent_settings,
        )

        # Attach project config to context for agent adaptation
        context.profile_config = project_config

        logger.info(f"Created context for branch '{branch_name}', agent '{agent_id}'")
        return context


class IContextController(ABC):
    """Interface for context controller operations."""
    
    @abstractmethod
    def get_context_for_branch(self, branch_name: Optional[str] = None, agent_id: str = "default") -> AgentContext:
        """Get context for a branch and agent."""
        pass
    
    @abstractmethod
    def get_context_for_agent(self, agent_id: str) -> AgentContext:
        """Get context for an agent."""
        pass
    
    @abstractmethod
    def get_available_profiles(self) -> List[ContextProfile]:
        """Get all available profiles."""
        pass


class ContextController(IContextController):
    """Main controller for agent context management following SOLID principles."""

    def __init__(
        self, 
        config=None,
        storage: Optional[ProfileStorage] = None,
        context_creator: Optional[IContextCreator] = None,
        context_validator: Optional[IContextValidator] = None,
        branch_matcher: Optional[IBranchMatcher] = None
    ):
        """Initialize the context controller with dependencies.

        Args:
            config: Optional configuration override
            storage: Optional storage instance for dependency injection
            context_creator: Optional context creator for dependency injection
            context_validator: Optional context validator for dependency injection
            branch_matcher: Optional branch matcher for dependency injection
        """
        # Handle legacy case where no config is provided
        if config is None:
            from .config import get_current_config
            self.config = get_current_config()
        else:
            self.config = config
            from .config import _global_config
            if _global_config is None:
                _global_config = self.config
        
        # Dependency injection with fallbacks
        self.storage = storage or ProfileStorage(self.config)
        self.context_creator = context_creator or ContextCreator(self.config)
        self.context_validator = context_validator or ContextValidator(config=self.config)
        self.branch_matcher = branch_matcher or BranchMatcher()
        
        # Ensure global config is set for backward compatibility
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
        
        self._context_cache: Dict[str, AgentContext] = {}
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

        # Create context using injected creator
        context = self.context_creator.create_context(profile, branch_name, agent_id)

        # Validate the context before returning
        validation_result = self.context_validator.validate_context(context)
        if not validation_result.is_valid:
            logger.warning(f"Created context failed validation: {validation_result.errors}")

        # Cache the context
        self._context_cache[cache_key] = context

        return context

    def get_context_for_agent(self, agent_id: str) -> AgentContext:
        """Get the current context for a specific agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            AgentContext instance for the current environment

        Raises:
            ContextNotFoundError: If no suitable context profile is found
        """
        return self.get_context_for_branch(agent_id=agent_id)

    def get_available_profiles(self) -> List[ContextProfile]:
        """Get all available context profiles.

        Returns:
            List of all ContextProfile instances
        """
        return self._load_all_profiles()

    def get_profile_by_id(self, profile_id: str) -> Optional[ContextProfile]:
        """Get a specific profile by ID.

        Args:
            profile_id: Profile identifier

        Returns:
            ContextProfile instance or None if not found
        """
        profiles = self._load_all_profiles()
        for profile in profiles:
            if profile.id == profile_id:
                return profile
        return None

    def create_profile(self, profile: ContextProfile) -> bool:
        """Create a new context profile.

        Args:
            profile: ContextProfile to create

        Returns:
            True if successful, False otherwise
        """
        # Validate the profile first
        validation_result = self.context_validator.validate_context(AgentContext(
            profile_id=profile.id,
            agent_id="validation",
            environment_type="development"
        ))
        if not validation_result.is_valid:
            logger.error(f"Profile validation failed: {validation_result.errors}")
            return False

        # Store the profile
        success = self.storage.save_profile(profile)
        if success:
            logger.info(f"Created new profile: {profile.id}")
        return success

    def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing context profile.

        Args:
            profile_id: Profile identifier
            updates: Dictionary of updates to apply

        Returns:
            True if successful, False otherwise
        """
        profile = self.get_profile_by_id(profile_id)
        if not profile:
            logger.error(f"Profile not found: {profile_id}")
            return False

        # Apply updates
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        # Validate the updated profile
        validation_result = self.context_validator.validate_context(AgentContext(
            profile_id=profile.id,
            agent_id="validation",
            environment_type="development"
        ))
        if not validation_result.is_valid:
            logger.error(f"Updated profile validation failed: {validation_result.errors}")
            return False

        # Save the updated profile
        success = self.storage.save_profile(profile)
        if success:
            logger.info(f"Updated profile: {profile_id}")
        return success

    def delete_profile(self, profile_id: str) -> bool:
        """Delete a context profile.

        Args:
            profile_id: Profile identifier

        Returns:
            True if successful, False otherwise
        """
        success = self.storage.delete_profile(profile_id)
        if success:
            logger.info(f"Deleted profile: {profile_id}")
        return success

    def validate_context(self, context: AgentContext) -> ContextValidationResult:
        """Validate an agent context for consistency and security.

        Args:
            context: AgentContext to validate

        Returns:
            ContextValidationResult with validation status
        """
        return self.context_validator.validate_context(context)

    def clear_cache(self):
        """Clear all cached profiles and contexts."""
        self.storage.clear_cache()
        self._context_cache.clear()
        logger.info("Cache cleared")

    def _find_profile_for_branch(self, branch_name: str) -> Optional[ContextProfile]:
        """Find the best matching context profile for a branch.

        Args:
            branch_name: Branch name to match against

        Returns:
            Matching ContextProfile or None
        """
        profiles = self._load_all_profiles()
        return self.branch_matcher.find_profile_for_branch(branch_name, profiles)

    def _load_all_profiles(self) -> List[ContextProfile]:
        """Load all available context profiles.

        Returns:
            List of ContextProfile instances
        """
        return self.storage.load_all_profiles()


# Backward compatibility - keep old class names and functions working
class BranchMatcherLegacy(BranchMatcher):
    """Legacy branch matcher for backward compatibility."""
    pass


class EnvironmentTypeDetectorLegacy(EnvironmentTypeDetector):
    """Legacy environment detector for backward compatibility."""
    pass


class ContextFileResolverLegacy(ContextFileResolver):
    """Legacy file resolver for backward compatibility."""
    pass


class ContextValidatorLegacy(ContextValidator):
    """Legacy context validator for backward compatibility."""
    pass


class ContextCreatorLegacy(ContextCreator):
    """Legacy context creator for backward compatibility."""
    pass


# Legacy function aliases
def get_context_for_branch(branch_name: Optional[str] = None, agent_id: str = "default") -> AgentContext:
    """Legacy function to get context for branch (deprecated)."""
    controller = ContextController()
    return controller.get_context_for_branch(branch_name, agent_id)


def get_context_for_agent(agent_id: str) -> AgentContext:
    """Legacy function to get context for agent (deprecated)."""
    controller = ContextController()
    return controller.get_context_for_agent(agent_id)


def get_available_profiles() -> List[ContextProfile]:
    """Legacy function to get available profiles (deprecated)."""
    controller = ContextController()
    return controller.get_available_profiles()
