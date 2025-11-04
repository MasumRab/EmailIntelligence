"""
Authentication and authorization system for the Email Intelligence Platform.

This module implements JWT-based authentication for API endpoints using the new
core architecture and database management system.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import hashlib
import logging
import secrets
from argon2 import PasswordHasher

import jwt
from .database import DatabaseManager
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import hashlib
import secrets

from .database import get_db
from .settings import settings

# Import the security framework components
from .security import SecurityContext, Permission, SecurityLevel

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    username: Optional[str] = None


class AuthManager:
    """
    Authentication manager for the Email Intelligence Platform.
    
    This class handles user authentication, token management, and authorization.
    """
    
    def __init__(self):
        self.db_manager = None
        
    async def initialize(self):
        """Initialize the AuthManager with database connection."""
        from .database import get_db
        self.db_manager = await get_db()
        
    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate a user with username and password."""
        if not self.db_manager:
            await self.initialize()
            
        # In a real implementation, this would check against the database
        # For now, we'll return a mock user
        return {
            "id": 1,
            "username": username,
            "email": f"{username}@example.com"
        }
        
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
        return encoded_jwt
        
    async def get_current_user(self, token: str) -> Optional[dict]:
        """Get the current user from a JWT token."""
        # In a real implementation, this would decode the token and get user from database
        # For now, we'll return a mock user
        return {
            "id": 1,
            "username": "testuser",
            "email": "testuser@example.com"
        }


# Initialize security scheme
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password using salted hashing."""
    salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + pwdhash.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    salt = hashed_password[:32]
    stored_password = hashed_password[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_password


async def create_user(username: str, password: str, db: DatabaseManager) -> bool:
    """Create a new user with hashed password."""
    # Check if user already exists
    users = db.users_data
    for user in users:
        if user.get("username") == username:
            return False  # User already exists
    
    # Hash the password
    hashed_password = hash_password(password)

    # Create new user
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }

    db.users_data.append(new_user)
    await db._save_data("users")
    return True


async def authenticate_user(username: str, password: str, db: DatabaseManager) -> Optional[dict]:
    """Authenticate a user by username and password."""
    users = db.users_data
    for user in users:
        if user.get("username") == username and user.get("is_active", True):
            if verify_password(password, user.get("hashed_password")):
                return user
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with the provided data."""
    # Try to get the settings if possible
    try:
        from ..backend.python_backend.settings import settings
        secret_key = settings.secret_key
        algorithm = settings.algorithm
        expire_minutes = settings.access_token_expire_minutes
    except ImportError:
        # Fallback to core settings
        from .settings import settings
        secret_key = settings.secret_key
        algorithm = settings.algorithm
        expire_minutes = settings.access_token_expire_minutes

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.

    Args:
        password: Plain text password

    Returns:
        Argon2 hashed password (including salt and parameters)
    """
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against an Argon2-hashed password.

    Args:
        plain_password: Plain text password
        hashed_password: Argon2 hashed password

    Returns:
        True if passwords match, False otherwise
    """
    ph = PasswordHasher()
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        # Verification failed (wrong password, corrupted hash, etc.)
        return False


async def authenticate_user(username: str, password: str, db) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user by username and password.
    
    Args:
        username: Username to authenticate
        password: Password to verify
        db: Database connection
        
    Returns:
        User data if authentication is successful, None otherwise
    """
    try:
        # Try to get user from database
        user_data = await db.get_user_by_username(username)
        if user_data and verify_password(password, user_data.get("hashed_password", "")):
            return user_data
        return None
    except Exception as e:
        logger.error(f"Error authenticating user {username}: {e}")
        return None


async def create_user(username: str, password: str, db) -> bool:
    """
    Create a new user in the database.
    
    Args:
        username: Username for the new user
        password: Password for the new user
        db: Database connection
        
    Returns:
        True if user was created successfully, False if user already exists or on error
    """
    try:
        # Check if user already exists
        existing_user = await db.get_user_by_username(username)
        if existing_user:
            return False
            
        # Hash the password
        hashed_password = hash_password(password)
        
        # Create user in database
        user_data = {
            "username": username,
            "hashed_password": hashed_password
        }
        
        await db.create_user(user_data)
        return True
    except Exception as e:
        logger.error(f"Error creating user {username}: {e}")
        return False


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Verify the JWT token from the Authorization header.
    
    This function checks if the provided token is valid and returns the token data.
    If the token is invalid or expired, it raises an HTTPException.
    """
    # Try to get the settings if possible
    try:
        from ..backend.python_backend.settings import settings
        secret_key = settings.secret_key
        algorithm = settings.algorithm
    except ImportError:
        # Fallback to core settings
        from .settings import settings
        secret_key = settings.secret_key
        algorithm = settings.algorithm

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials, 
            secret_key,
            algorithms=[algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception
    
    return token_data


async def get_current_user(token_data: TokenData = Depends(verify_token)) -> str:
    """
    Get the current authenticated user from the token.
    
    This function can be used as a dependency to protect endpoints.
    """
    return token_data.username


async def get_current_active_user(current_user: str = Depends(get_current_user)) -> str:
    """
    Get the current active user, ensuring they are active.
    """
    db = await get_db()
    users = db.users_data
    
    for user in users:
        if user.get("username") == current_user and user.get("is_active", True):
            return current_user

    raise HTTPException(status_code=400, detail="Inactive user")


def create_authentication_middleware():
    """
    Create and return an authentication middleware.
    
    This is a placeholder function that could be expanded to implement
    custom authentication middleware if needed.
    """
    def role_checker(token_data: TokenData = Depends(verify_token)) -> TokenData:
        # In a real implementation, you would check the user's actual role from the database
        # For now, we'll check the role from the token
        if token_data.role not in [role.value for role in required_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. One of {[role.value for role in required_roles]} roles required."
            )
        return token_data
    return role_checker


def create_security_context_for_user(username: str) -> SecurityContext:
    """
    Create a security context for an authenticated user.
    
    This integrates with the existing security framework.
    
    Args:
        username: Username of the authenticated user
        
    Returns:
        SecurityContext for the user
    """
    # In a production system, you would fetch user permissions from the database
    # For now, we'll give standard permissions
    permissions = [Permission.READ, Permission.WRITE]
    
    # Create a session token (in a real system, this would be linked to the JWT)
    session_token = secrets.token_urlsafe(32)
    
    context = SecurityContext(
        user_id=username,
        permissions=permissions,
        security_level=SecurityLevel.INTERNAL,
        session_id=session_token,
        allowed_resources=["*"],  # All resources allowed for now
    )
    
    return context
