"""
Authentication module for the Email Intelligence Platform.

This module implements JWT-based authentication for API endpoints and integrates with the existing security framework.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib
import secrets

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from .database_dependencies import DatabaseDep
from .database import DatabaseManager
from .settings import settings

# Import the security framework components
from .security import SecurityContext, Permission

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """Data structure for JWT token payload"""
    username: Optional[str] = None


class User(BaseModel):
    """User model for authentication"""
    username: str
    hashed_password: str


# Initialize security scheme
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the provided data.
    
    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration
        
    Returns:
        Encoded JWT token as a string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with a salt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password with salt
    """
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{password_hash}:{salt}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password with salt
        
    Returns:
        True if passwords match, False otherwise
    """
    try:
        password_hash, salt = hashed_password.split(":")
        return hashlib.sha256((plain_password + salt).encode()).hexdigest() == password_hash
    except ValueError:
        # Invalid format
        return False


async def authenticate_user(username: str, password: str, db: DatabaseManager) -> Optional[Dict[str, Any]]:
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


async def create_user(username: str, password: str, db: DatabaseManager) -> bool:
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
    
    Args:
        credentials: HTTP authorization credentials containing the bearer token
        
    Returns:
        TokenData containing the username from the token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception
    
    return token_data


def get_current_active_user(token_data: TokenData = Depends(verify_token)) -> str:
    """
    Get the current authenticated user from the token.
    
    This function can be used as a dependency to protect endpoints.
    
    Args:
        token_data: Token data from verified JWT token
        
    Returns:
        Username of the authenticated user
    """
    # In a real implementation, you would fetch user details from a database
    # For now, we just return the username from the token
    return token_data.username


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
        security_level="internal",  # Using string instead of enum for compatibility
        session_token=session_token,
        created_at=time.time(),
        expires_at=time.time() + (8 * 3600),  # 8 hours
        allowed_resources=["*"],  # All resources allowed for now
    )
    
    return context