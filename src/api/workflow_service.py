
from fastapi import APIRouter

router = APIRouter()

@router.get("/workflow_service")
async def get_workflow_service():
    return {}
