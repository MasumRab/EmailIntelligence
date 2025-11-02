"""
Authentication and authorization system for the Email Intelligence Platform.

This module implements JWT-based authentication for API endpoints using the new
core architecture and database management system.
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import hashlib
import secrets

from .database import get_db, DatabaseManager
from .security import DataSanitizer


class TokenData(BaseModel):
    username: Optional[str] = None


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
    pass