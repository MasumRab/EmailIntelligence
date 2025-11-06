
from fastapi import APIRouter

router = APIRouter()

@router.get("/performance_service")
async def get_performance_service():
    return {}
