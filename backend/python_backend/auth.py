"""
Authentication and authorization system for the Email Intelligence Platform.

This module implements JWT-based authentication for API endpoints.
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from .settings import settings


class TokenData(BaseModel):
    username: Optional[str] = None


# Initialize security scheme
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with the provided data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Verify the JWT token from the Authorization header.

    This function checks if the provided token is valid and returns the token data.
    If the token is invalid or expired, it raises an HTTPException.
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
    except jwt.PyJWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception

    return token_data


def get_current_user(token_data: TokenData = Depends(verify_token)):
    """
    Get the current authenticated user from the token.

    This function can be used as a dependency to protect endpoints.
    """
    # In a real implementation, you would fetch user details from a database
    # For now, we just return the username from the token
    return token_data.username


def create_authentication_middleware():
    """
    Create and return an authentication middleware.

    This is a placeholder function that could be expanded to implement
    custom authentication middleware if needed.
    """
    pass