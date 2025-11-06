
from fastapi import APIRouter

router = APIRouter()

@router.get("/gmail_service")
async def get_gmail_service():
    return {}
