"""
Authentication routes for the Email Intelligence Platform.

This module provides authentication endpoints for the new modular architecture.
"""

import logging
from datetime import timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.core.auth import authenticate_user, create_access_token, create_user, get_current_active_user, hash_password, TokenData, require_role, UserRole
from src.core.factory import get_data_source
from src.core.data_source import DataSource
from src.core.mfa import get_mfa_service
from src.core.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"
    permissions: Optional[List[str]] = []


class UserLogin(BaseModel):
    username: str
    password: str
    mfa_token: Optional[str] = None


class EnableMFARequest(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class MFASetupResponse(BaseModel):
    secret: str
    qr_code: str
    backup_codes: List[str]


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: DataSource = Depends(get_data_source)):
    """Login endpoint to get access token"""
    user = await authenticate_user(user_credentials.username, user_credentials.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user has MFA enabled
    if user.get("mfa_enabled", False):
        mfa_service = get_mfa_service()

        # If MFA token was not provided, return a special response indicating MFA is required
        if not user_credentials.mfa_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="MFA token required",
                headers={"WWW-Authenticate": "Bearer", "X-MFA-Required": "true"},
            )

        # Verify the MFA token
        secret = user.get("mfa_secret")
        if not secret:
            logger.error(f"MFA enabled for user {user_credentials.username} but no secret found")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error",
            )

        # First, try to verify with TOTP
        token_verified = mfa_service.verify_token(secret, user_credentials.mfa_token)

        # If TOTP failed, try backup codes
        if not token_verified:
            backup_codes = user.get("mfa_backup_codes", [])
            is_backup_code, updated_codes = mfa_service.verify_backup_code(
                backup_codes, user_credentials.mfa_token
            )

            if is_backup_code:
                # Update the user's backup codes to remove the used one
                for i, u in enumerate(db.users_data):
                    if u.get("username") == user_credentials.username:
                        db.users_data[i]["mfa_backup_codes"] = updated_codes
                        await db._save_data("users")
                        break
                token_verified = True

        # If neither TOTP nor backup code worked, deny access
        if not token_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_credentials.username, "role": user.get("role", "user")}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(current_user: TokenData = Depends(get_current_active_user), db: DataSource = Depends(get_data_source)):
    """Setup MFA for the current user"""

    # Get the user from database
    user = await db.get_user_by_username(current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    mfa_service = get_mfa_service()

    # Generate a new secret
    secret = mfa_service.generate_secret()

    # Generate QR code
    qr_code = mfa_service.generate_qr_code(current_user.username, secret)

    # Generate backup codes
    backup_codes = mfa_service.generate_backup_codes()

    # Update the user record with MFA data (but don't enable MFA yet)
    user_index = None
    for i, u in enumerate(db.users_data):
        if u.get("username") == current_user.username:
            user_index = i
            break

    if user_index is not None:
        # Update the user record
        db.users_data[user_index]["mfa_secret"] = secret
        # We don't enable MFA yet - user needs to verify the setup first
        # db.users_data[user_index]["mfa_enabled"] = True
        db.users_data[user_index]["mfa_backup_codes"] = backup_codes
        await db._save_data("users")

    return MFASetupResponse(
        secret=secret,
        qr_code=qr_code,
        backup_codes=backup_codes
    )


@router.post("/mfa/enable")
async def enable_mfa(
    mfa_request: EnableMFARequest,
    current_user: TokenData = Depends(get_current_active_user),
    db: DataSource = Depends(get_data_source)
):
    """Enable MFA after user has verified the setup"""

    # Get the user from database
    user = await db.get_user_by_username(current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if MFA is already enabled
    if user.get("mfa_enabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled for this user"
        )

    # Verify the token provided by user against their stored secret
    mfa_service = get_mfa_service()
    secret = user.get("mfa_secret")

    if not secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not properly set up for this user"
        )

    if not mfa_service.verify_token(secret, mfa_request.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA token. Please try again."
        )

    # Find and update the user record to enable MFA
    for i, u in enumerate(db.users_data):
        if u.get("username") == current_user.username:
            db.users_data[i]["mfa_enabled"] = True
            await db._save_data("users")
            break

    return {"message": "MFA enabled successfully"}


@router.post("/mfa/disable")
async def disable_mfa(
    current_user: TokenData = Depends(get_current_active_user),
    db: DataSource = Depends(get_data_source)
):
    """Disable MFA for the current user"""

    # Get the user from database
    user = await db.get_user_by_username(current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Find and update the user record to disable MFA
    for i, u in enumerate(db.users_data):
        if u.get("username") == current_user.username:
            db.users_data[i]["mfa_enabled"] = False
            db.users_data[i]["mfa_secret"] = None
            db.users_data[i]["mfa_backup_codes"] = []
            await db._save_data("users")
            break

    return {"message": "MFA disabled successfully"}


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: DataSource = Depends(get_data_source)):
    """Register a new user"""
    user_dict = {
        "username": user_data.username,
        "hashed_password": hash_password(user_data.password),
        "role": user_data.role,
        "permissions": user_data.permissions,
        "mfa_enabled": False,
        "mfa_secret": None,
        "mfa_backup_codes": []
    }
    success = await create_user(user_data.username, user_data.password, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_data.username, "role": user_data.role}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user_info(current_user: TokenData = Depends(get_current_active_user)):
    """Get information about the current authenticated user"""
    return {"username": current_user.username, "role": current_user.role}


@router.get("/admin-only")
async def admin_only_endpoint(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Protected endpoint that only admins can access"""
    return {"message": "Hello admin!", "user": current_user.username}