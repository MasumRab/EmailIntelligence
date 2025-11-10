"""Authentication and authorization service."""

from enum import Enum
from typing import Optional, List
from abc import ABC, abstractmethod

from src.logging import get_logger


logger = get_logger(__name__)


class PermissionLevel(str, Enum):
    """Role-based permission levels."""

    READ = "read"           # View-only access
    RUN = "run"             # Execute verifications
    REVIEW = "review"       # Review and approve results
    ADMIN = "admin"         # Full administrative access


class AuthContext:
    """Authentication context for a user/service."""

    def __init__(
        self,
        user_id: str,
        token: str,
        permission_level: PermissionLevel = PermissionLevel.READ,
    ):
        """Initialize authentication context."""
        self.user_id = user_id
        self.token = token
        self.permission_level = permission_level

    def has_permission(self, required_level: PermissionLevel) -> bool:
        """Check if user has required permission level."""
        level_hierarchy = {
            PermissionLevel.READ: 0,
            PermissionLevel.RUN: 1,
            PermissionLevel.REVIEW: 2,
            PermissionLevel.ADMIN: 3,
        }
        return level_hierarchy[self.permission_level] >= level_hierarchy[required_level]


class AuthStrategy(ABC):
    """Abstract base class for authentication strategies."""

    @abstractmethod
    async def authenticate(self, token: str) -> Optional[AuthContext]:
        """Authenticate a user with the given token."""
        pass

    @abstractmethod
    async def authorize(self, context: AuthContext, required_level: PermissionLevel) -> bool:
        """Check if user has required authorization level."""
        pass


class TokenAuthStrategy(AuthStrategy):
    """Token-based authentication strategy."""

    def __init__(self, valid_tokens: Optional[dict[str, PermissionLevel]] = None):
        """Initialize token auth strategy."""
        self.valid_tokens = valid_tokens or {}
        self.logger = logger

    async def authenticate(self, token: str) -> Optional[AuthContext]:
        """Authenticate using token."""
        if token in self.valid_tokens:
            permission_level = self.valid_tokens[token]
            self.logger.info(
                f"Token authenticated with permission level: {permission_level}",
                token=token[:10] + "...",
            )
            return AuthContext(
                user_id="token_user",
                token=token,
                permission_level=permission_level,
            )
        self.logger.warning(f"Invalid token: {token[:10]}...")
        return None

    async def authorize(
        self, context: AuthContext, required_level: PermissionLevel
    ) -> bool:
        """Check authorization level."""
        return context.has_permission(required_level)


class AuthService:
    """Service for managing authentication and authorization."""

    def __init__(self, strategy: Optional[AuthStrategy] = None):
        """Initialize auth service with strategy."""
        self.strategy = strategy or TokenAuthStrategy()
        self.logger = logger

    async def authenticate(self, token: str) -> Optional[AuthContext]:
        """Authenticate a token."""
        return await self.strategy.authenticate(token)

    async def authorize(
        self, context: AuthContext, required_level: PermissionLevel
    ) -> bool:
        """Check if user is authorized for the required level."""
        is_authorized = await self.strategy.authorize(context, required_level)
        if not is_authorized:
            self.logger.warning(
                f"Authorization failed: user {context.user_id} "
                f"permission {context.permission_level} required {required_level}"
            )
        return is_authorized

    def set_strategy(self, strategy: AuthStrategy) -> None:
        """Set authentication strategy."""
        self.strategy = strategy
        self.logger.info(f"Auth strategy changed to: {strategy.__class__.__name__}")
