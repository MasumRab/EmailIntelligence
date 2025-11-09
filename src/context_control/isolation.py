"""Context isolation mechanisms to prevent contamination between agents."""

from pathlib import Path
from typing import Set, List, Optional, Dict, Any
import fnmatch
import hashlib

from .models import AgentContext, ContextProfile
from .logging import get_context_logger
from .exceptions import ContextIsolationError
from .config import get_current_config


logger = get_context_logger()


class ContextIsolator:
    """Handles context isolation and access control for agents."""

    def __init__(self, context: AgentContext, config=None):
        """Initialize the context isolator.

        Args:
            context: The agent context to isolate
            config: Optional configuration override
        """
        self.context = context
        self.config = config or get_current_config()
        self._access_log: List[Dict[str, Any]] = []
        logger.info(f"Context isolator initialized for agent '{context.agent_id}'")

    def is_file_accessible(self, file_path: str) -> bool:
        """Check if a file is accessible within the current context.

        Args:
            file_path: Path to the file to check

        Returns:
            True if accessible, False otherwise
        """
        # Normalize path
        normalized_path = self._normalize_path(file_path)

        # Check blocked files first (deny list)
        if self._matches_patterns(normalized_path, self.context.restricted_files):
            self._log_access(normalized_path, False, "blocked")
            return False

        # Check allowed files (allow list)
        if self._matches_patterns(normalized_path, self.context.accessible_files):
            self._log_access(normalized_path, True, "allowed")
            return True

        # If no patterns match, deny access by default
        self._log_access(normalized_path, False, "no_match")
        return False

    def filter_accessible_files(self, file_paths: List[str]) -> List[str]:
        """Filter a list of files to only include accessible ones.

        Args:
            file_paths: List of file paths to filter

        Returns:
            List of accessible file paths
        """
        accessible = []
        for path in file_paths:
            if self.is_file_accessible(path):
                accessible.append(path)
        return accessible

    def validate_context_integrity(self) -> bool:
        """Validate that the context maintains isolation integrity.

        Returns:
            True if context is properly isolated, False otherwise
        """
        try:
            # Check for conflicting permissions
            accessible_set = set(self.context.accessible_files)
            restricted_set = set(self.context.restricted_files)

            conflicts = accessible_set & restricted_set
            if conflicts:
                logger.error(f"Context integrity violation: conflicting permissions for {conflicts}")
                return False

            # Check that context has proper boundaries
            if not self.context.accessible_files and not self.context.restricted_files:
                logger.warning("Context has no file access boundaries - potential security risk")
                # This is a warning, not an error, as some contexts might be unrestricted

            return True

        except Exception as e:
            logger.error(f"Error validating context integrity: {e}")
            return False

    def get_access_summary(self) -> Dict[str, Any]:
        """Get a summary of file access patterns.

        Returns:
            Dictionary with access statistics
        """
        total_accesses = len(self._access_log)
        allowed_accesses = sum(1 for log in self._access_log if log['allowed'])
        blocked_accesses = total_accesses - allowed_accesses

        return {
            'total_accesses': total_accesses,
            'allowed_accesses': allowed_accesses,
            'blocked_accesses': blocked_accesses,
            'access_log': self._access_log[-100:]  # Last 100 entries
        }

    def _normalize_path(self, file_path: str) -> str:
        """Normalize a file path for consistent pattern matching.

        Args:
            file_path: File path to normalize

        Returns:
            Normalized path string
        """
        # Convert to Path object for normalization
        path_obj = Path(file_path)

        # Get relative path from repository root if possible
        try:
            # This is a simplified approach - in practice, you'd want to
            # resolve relative to the actual repository root
            return str(path_obj.resolve())
        except Exception:
            # Fallback to original path
            return file_path

    def _matches_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """Check if a file path matches any of the given patterns.

        Args:
            file_path: File path to check
            patterns: List of glob patterns

        Returns:
            True if any pattern matches, False otherwise
        """
        for pattern in patterns:
            try:
                if fnmatch.fnmatch(file_path, pattern):
                    return True

                # Also try matching against just the filename
                filename = Path(file_path).name
                if fnmatch.fnmatch(filename, pattern):
                    return True

            except Exception:
                # Skip invalid patterns
                continue

        return False

    def _log_access(self, file_path: str, allowed: bool, reason: str):
        """Log a file access attempt.

        Args:
            file_path: Path that was accessed
            allowed: Whether access was allowed
            reason: Reason for the access decision
        """
        log_entry = {
            'file_path': file_path,
            'allowed': allowed,
            'reason': reason,
            'timestamp': None  # Would use datetime in real implementation
        }

        self._access_log.append(log_entry)

        # Also log to context's access log
        self.context.access_log.append(log_entry)

        # Keep logs bounded
        if len(self._access_log) > 1000:
            self._access_log = self._access_log[-500:]


class IsolationManager:
    """Manages isolation across multiple contexts."""

    def __init__(self, config=None):
        """Initialize the isolation manager.

        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()
        self._isolators: Dict[str, ContextIsolator] = {}
        logger.info("Isolation manager initialized")

    def get_isolator(self, context: AgentContext) -> ContextIsolator:
        """Get or create an isolator for a context.

        Args:
            context: The agent context

        Returns:
            ContextIsolator instance
        """
        key = f"{context.profile_id}:{context.agent_id}"

        if key not in self._isolators:
            self._isolators[key] = ContextIsolator(context, self.config)

        return self._isolators[key]

    def check_cross_context_access(self, contexts: List[AgentContext]) -> List[str]:
        """Check for potential cross-context access violations.

        Args:
            contexts: List of contexts to check

        Returns:
            List of violation descriptions
        """
        violations = []

        # Check for overlapping accessible files between different contexts
        for i, ctx1 in enumerate(contexts):
            for j, ctx2 in enumerate(contexts[i+1:], i+1):
                if ctx1.agent_id == ctx2.agent_id:
                    continue  # Same agent, skip

                overlap = set(ctx1.accessible_files) & set(ctx2.accessible_files)
                if overlap:
                    violations.append(
                        f"Overlapping file access between agents '{ctx1.agent_id}' "
                        f"and '{ctx2.agent_id}': {overlap}"
                    )

        return violations

    def enforce_isolation(self, contexts: List[AgentContext]) -> bool:
        """Enforce isolation rules across all contexts.

        Args:
            contexts: List of contexts to enforce isolation for

        Returns:
            True if isolation is maintained, False if violations found
        """
        violations = self.check_cross_context_access(contexts)

        if violations:
            for violation in violations:
                logger.error(f"Isolation violation: {violation}")
            return False

        # Validate each context individually
        for context in contexts:
            isolator = self.get_isolator(context)
            if not isolator.validate_context_integrity():
                logger.error(f"Context integrity violation for agent '{context.agent_id}'")
                return False

        return True