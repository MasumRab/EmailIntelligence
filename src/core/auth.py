"""
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
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
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
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Here, you might fetch user details from a database using `payload.get("sub")`
    # For this example, we'll just return the payload.
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # You could expand this to return a Pydantic model of the user
    return {"username": username}


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
