"""
<<<<<<< HEAD
Authentication module for the Email Intelligence Platform.

This module implements JWT-based authentication for API endpoints and integrates with the existing security framework.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import hashlib
import secrets
from argon2 import PasswordHasher

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Database imports removed - use dependency injection with create_database_manager
from .settings import settings

# Import the security framework components
from .security import SecurityContext, Permission, SecurityLevel

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """Data structure for JWT token payload"""
    username: Optional[str] = None
    role: Optional[str] = "user"


from enum import Enum


class UserRole(str, Enum):
    """User roles for role-based access control"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(BaseModel):
    """User model for authentication"""
    username: str
    hashed_password: str
    role: UserRole = UserRole.USER
    permissions: Optional[List[str]] = []


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
=======
Core authentication and authorization functionalities for the Email Intelligence Platform.
This module provides JWT-based token management, password hashing, and dependency
injection-based security for FastAPI endpoints.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

from .settings import settings

# --- Configuration ---
# In a real application, these should be loaded from a secure configuration source
SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- OAuth2 Scheme ---
# This defines the mechanism for the client to provide the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Token Management ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
<<<<<<< HEAD
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
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
    except argon2.exceptions.VerifyMismatchError:
        # Password verification failed
        return False
    except argon2.exceptions.InvalidHashError:
        # Invalid hash format
        logger.warning("Invalid password hash format")
        return False
    except Exception as e:
        # Other unexpected errors
        logger.error(f"Unexpected error during password verification: {e}")
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
    
    Args:
        credentials: HTTP authorization credentials containing the bearer token
        
    Returns:
        TokenData containing the username and role from the token
        
    Raises:
        HTTPException: If token is invalid or expired
=======
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except jwt.PyJWTError as e:
        logger.error(f"Error encoding JWT token: {e}")
        # In a real-world scenario, you might want to handle this more gracefully
        # or raise a specific internal server error.
        raise


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT access token and returns its payload.
    Returns None if the token is invalid, expired, or cannot be decoded.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return None


# --- Password Verification ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against its hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain password using the configured scheme (bcrypt).
    """
    return pwd_context.hash(password)


# --- FastAPI Dependencies for Security ---

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    A FastAPI dependency that verifies the JWT token from the request header
    and returns the user's data from the token payload.

    Raises HTTPException with a 401 status if the token is missing or invalid.
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
<<<<<<< HEAD
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        role: str = payload.get("role", "user")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
=======

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Here, you might fetch user details from a database using `payload.get("sub")`
    # For this example, we'll just return the payload.
    username: str = payload.get("sub")
    if username is None:
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
        raise credentials_exception

    # You could expand this to return a Pydantic model of the user
    return {"username": username}


<<<<<<< HEAD
def get_current_active_user(token_data: TokenData = Depends(verify_token)) -> TokenData:
    """
    Get the current authenticated user from the token.
    
    This function can be used as a dependency to protect endpoints.
    
    Args:
        token_data: Token data from verified JWT token
        
    Returns:
        TokenData containing username and role of the authenticated user
    """
    # In a real implementation, you would fetch user details from a database
    # For now, we just return the token data
    return token_data


def require_role(required_role: UserRole):
    """
    Dependency to require a specific role for accessing an endpoint.
    
    Args:
        required_role: The role required to access the endpoint
        
    Returns:
        A dependency function that checks the user's role
    """
    def role_checker(token_data: TokenData = Depends(verify_token)) -> TokenData:
        # In a real implementation, you would check the user's actual role from the database
        # For now, we'll check the role from the token
        if token_data.role != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. {required_role.value} role required."
            )
        return token_data
    return role_checker


def require_any_role(required_roles: List[UserRole]):
    """
    Dependency to require any of the specified roles for accessing an endpoint.
    
    Args:
        required_roles: List of roles that can access the endpoint
        
    Returns:
        A dependency function that checks the user's role
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
=======
async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Another FastAPI dependency that can be used to check if the user is active.
    This is a placeholder for more complex authorization logic.

    For example, you could check if `current_user.disabled` is true.
    """
    # In a real app, you would fetch the user from the database and check a flag like `is_active`
    # if current_user.get("disabled"):
    #     raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
