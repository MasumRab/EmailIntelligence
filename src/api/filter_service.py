
from fastapi import APIRouter

router = APIRouter()

@router.get("/filter_service")
async def get_filter_service():
    return {}
