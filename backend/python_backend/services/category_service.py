"""
It will be removed in a future release.

Category service for the Email Intelligence Platform
Handles all category-related business logic
"""

from typing import List, Optional, Dict, Any
from .base_service import BaseService, BaseResponse
from src.core.database import FIELD_ID


class CategoryService(BaseService):
    """Service class for category operations"""

    def __init__(self):
        super().__init__()
        self._db = None

    async def get_db(self):
        """Get database instance"""
        if self._db is None:
            self._db = await super().get_db()
        return self._db

    async def get_all_categories(self) -> BaseResponse:
        """Get all categories"""
        try:
            db = await self.get_db()
            categories = await db.get_all_categories()
            return BaseResponse(
                success=True, message="Categories retrieved successfully", data=categories
            )
        except Exception as e:
            return await self.handle_error(e, "get_all_categories")

    async def create_category(self, category_data: Dict[str, Any]) -> BaseResponse:
        """Create a new category"""
        try:
            db = await self.get_db()
            created_category = await db.create_category(category_data)
            if created_category:
                return BaseResponse(
                    success=True, message="Category created successfully", data=created_category
                )
            else:
                return BaseResponse(
                    success=False,
                    message="Failed to create category",
                    error="Category creation failed",
                )
        except Exception as e:
            return await self.handle_error(e, "create_category")

    async def update_category(self, category_id: int, update_data: Dict[str, Any]) -> BaseResponse:
        """Update a category by its ID"""
        try:
            db = await self.get_db()
            updated_category = await db.update_category(category_id, update_data)
            if updated_category:
                return BaseResponse(
                    success=True, message="Category updated successfully", data=updated_category
                )
            else:
                return BaseResponse(
                    success=False,
                    message="Category not found",
                    error="Category with specified ID does not exist",
                )
        except Exception as e:
            return await self.handle_error(e, "update_category")

    async def delete_category(self, category_id: int) -> BaseResponse:
        """Delete a category by its ID"""
        try:
            db = await self.get_db()
            deleted = await db.delete_category(category_id)
            if deleted:
                return BaseResponse(
                    success=True, message="Category deleted successfully"
                )
            else:
                return BaseResponse(
                    success=False,
                    message="Category not found",
                    error="Category with specified ID does not exist",
                )
        except Exception as e:
            return await self.handle_error(e, "delete_category")
