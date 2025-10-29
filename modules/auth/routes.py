"""
Authentication routes for the Email Intelligence Platform.

This module provides authentication endpoints for the new modular architecture.
"""

import logging
from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.core.auth import authenticate_user, create_access_token, create_user, get_current_active_user
from src.core.database import get_db
from ..backend.python_backend.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login endpoint to get access token"""
    db = await get_db()
    user = await authenticate_user(user_credentials.username, user_credentials.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_credentials.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user"""
    db = await get_db()
    success = await create_user(user_data.username, user_data.password, db)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user_info(current_user: str = Depends(get_current_active_user)):
    """Get information about the current authenticated user"""
    return {"username": current_user}