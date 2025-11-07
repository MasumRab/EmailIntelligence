
from fastapi import APIRouter

router = APIRouter()

@router.get("/action_service")
async def get_action_service():
    return {}
