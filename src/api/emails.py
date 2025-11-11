
from fastapi import APIRouter, Depends
from src.core.auth import get_current_active_user

router = APIRouter()

@router.get("/emails")
async def get_emails(current_user: dict = Depends(get_current_active_user)):
    return []
