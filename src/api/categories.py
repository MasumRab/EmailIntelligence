
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.core.auth import get_current_active_user
from src.core.security import validate_user_input

router = APIRouter()

class Category(BaseModel):
    name: str
    color: str

@router.get("/categories")
async def get_categories(current_user: dict = Depends(get_current_active_user)):
    return []

@router.post("/categories")
async def create_category(category: Category, current_user: dict = Depends(get_current_active_user)):
    errors = validate_user_input(category.dict(), required_fields=["name", "color"])
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    return category
