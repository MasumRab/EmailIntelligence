"""
Category Service for Email Intelligence Platform
Handles all category-related business logic
"""

import logging
from typing import List, Optional, Dict, Any, Union

from .base_service import BaseService, ServiceResponse
from ..models import CategoryResponse, CategoryCreate, CategoryUpdate
from ..exceptions import CategoryNotFoundException, DatabaseError

logger = logging.getLogger(__name__)


class CategoryService(BaseService):
    """
    Service class for category operations with enhanced functionality.
    
    Features:
    - Comprehensive category management
    - Category statistics and analytics
    - Batch operations
    - Enhanced error handling
    """
    
    def __init__(self):
        super().__init__()
        self._db = None
        
    async def get_category_by_id(self, category_id: int) -> ServiceResponse:
        """
        Get a category by its ID.
        
        Args:
            category_id: The ID of the category
            
        Returns:
            ServiceResponse with category data or error information
        """
        try:
            db = await self.get_db()
            # Get all categories and find the one with matching ID
            categories = await db.get_all_categories()
            category = next((cat for cat in categories if cat.get("id") == category_id), None)
            
            if category:
                return await self.handle_success(
                    data=CategoryResponse(**category),
                    message=f"Category with ID {category_id} retrieved successfully"
                )
            else:
                return await self.handle_error(
                    CategoryNotFoundException(category_id=category_id),
                    operation="get_category_by_id",
                    error_code="CATEGORY_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "get_category_by_id")
    
    async def get_category_by_name(self, name: str) -> ServiceResponse:
        """
        Get a category by its name.
        
        Args:
            name: The name of the category
            
        Returns:
            ServiceResponse with category data or error information
        """
        try:
            if not name:
                return await self.handle_error(
                    ValueError("Category name cannot be empty"),
                    operation="get_category_by_name",
                    error_code="INVALID_INPUT"
                )
            
            db = await self.get_db()
            # Get all categories and find the one with matching name
            categories = await db.get_all_categories()
            category = next((cat for cat in categories if cat.get("name", "").lower() == name.lower()), None)
            
            if category:
                return await self.handle_success(
                    data=CategoryResponse(**category),
                    message=f"Category '{name}' retrieved successfully"
                )
            else:
                return await self.handle_error(
                    CategoryNotFoundException(name=name),
                    operation="get_category_by_name",
                    error_code="CATEGORY_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "get_category_by_name")
    
    async def get_all_categories(self, sort_by: str = "name", sort_order: str = "asc") -> ServiceResponse:
        """
        Get all categories with sorting options.
        
        Args:
            sort_by: Field to sort by (name, count, created_at)
            sort_order: Sort order (asc or desc)
            
        Returns:
            ServiceResponse with list of categories or error information
        """
        try:
            db = await self.get_db()
            categories = await db.get_all_categories()
            
            # Sort categories
            if sort_by == "count":
                categories.sort(key=lambda x: x.get("count", 0), reverse=(sort_order == "desc"))
            elif sort_by == "name":
                categories.sort(key=lambda x: x.get("name", ""), reverse=(sort_order == "desc"))
            # Default sorting by name if sort_by is not recognized
            
            # Convert to CategoryResponse objects
            category_responses = [CategoryResponse(**cat) for cat in categories]
            
            return await self.handle_success(
                data=category_responses,
                message=f"Retrieved {len(category_responses)} categories",
                metadata={
                    "total_count": len(category_responses),
                    "sort_by": sort_by,
                    "sort_order": sort_order
                }
            )
            
        except Exception as e:
            return await self.handle_error(e, "get_all_categories")
    
    async def create_category(self, category_data: Union[CategoryCreate, Dict[str, Any]]) -> ServiceResponse:
        """
        Create a new category.
        
        Args:
            category_data: Category data to create (CategoryCreate object or dict)
            
        Returns:
            ServiceResponse with created category or error information
        """
        try:
            # Convert to dict if it's a Pydantic model
            if isinstance(category_data, CategoryCreate):
                category_dict = category_data.model_dump()
            else:
                category_dict = category_data
            
            # Validate required fields
            required_fields = ["name"]
            if not await self.validate_input(category_dict, required_fields):
                return await self.handle_error(
                    ValueError(f"Missing required fields: {required_fields}"),
                    operation="create_category",
                    error_code="INVALID_INPUT"
                )
            
            # Check if category with same name already exists
            existing_category = await self.get_category_by_name(category_dict["name"])
            if existing_category.success:
                return await self.handle_error(
                    ValueError(f"Category with name '{category_dict['name']}' already exists"),
                    operation="create_category",
                    error_code="CATEGORY_EXISTS"
                )
            
            db = await self.get_db()
            created_category = await db.create_category(category_dict)
            
            if created_category:
                return await self.handle_success(
                    data=CategoryResponse(**created_category),
                    message="Category created successfully"
                )
            else:
                return await self.handle_error(
                    Exception("Failed to create category"),
                    operation="create_category",
                    error_code="CATEGORY_CREATION_FAILED"
                )
                
        except Exception as e:
            return await self.handle_error(e, "create_category")
    
    async def update_category(self, category_id: int, update_data: Union[CategoryUpdate, Dict[str, Any]]) -> ServiceResponse:
        """
        Update a category by its ID.
        
        Args:
            category_id: The ID of the category to update
            update_data: Category update data (CategoryUpdate object or dict)
            
        Returns:
            ServiceResponse with updated category or error information
        """
        try:
            # Convert to dict if it's a Pydantic model
            if isinstance(update_data, CategoryUpdate):
                update_dict = update_data.model_dump(exclude_unset=True)
            else:
                update_dict = update_data
            
            # Validate category exists
            get_result = await self.get_category_by_id(category_id)
            if not get_result.success:
                return get_result  # Return the error from get_category_by_id
            
            db = await self.get_db()
            updated_category = await db.update_category(category_id, update_dict)
            
            if updated_category:
                return await self.handle_success(
                    data=CategoryResponse(**updated_category),
                    message=f"Category with ID {category_id} updated successfully"
                )
            else:
                return await self.handle_error(
                    CategoryNotFoundException(category_id=category_id),
                    operation="update_category",
                    error_code="CATEGORY_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "update_category")
    
    async def delete_category(self, category_id: int) -> ServiceResponse:
        """
        Delete a category by its ID.
        
        Args:
            category_id: The ID of the category to delete
            
        Returns:
            ServiceResponse with success or error information
        """
        try:
            # Validate category exists
            get_result = await self.get_category_by_id(category_id)
            if not get_result.success:
                return get_result  # Return the error from get_category_by_id
            
            db = await self.get_db()
            success = await db.delete_category(category_id)
            
            if success:
                return await self.handle_success(
                    message=f"Category with ID {category_id} deleted successfully"
                )
            else:
                return await self.handle_error(
                    CategoryNotFoundException(category_id=category_id),
                    operation="delete_category",
                    error_code="CATEGORY_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "delete_category")
    
    async def get_category_statistics(self) -> ServiceResponse:
        """
        Get category statistics and analytics.
        
        Returns:
            ServiceResponse with statistics data or error information
        """
        try:
            db = await self.get_db()
            categories = await db.get_all_categories()
            
            # Calculate statistics
            total_categories = len(categories)
            total_emails = sum(cat.get("count", 0) for cat in categories)
            
            # Find largest and smallest categories
            if categories:
                largest_category = max(categories, key=lambda x: x.get("count", 0))
                smallest_category = min(categories, key=lambda x: x.get("count", 0))
                
                # Calculate average emails per category
                avg_emails = total_emails / total_categories if total_categories > 0 else 0
                
                statistics = {
                    "total_categories": total_categories,
                    "total_emails_categorized": total_emails,
                    "average_emails_per_category": round(avg_emails, 2),
                    "largest_category": {
                        "name": largest_category.get("name"),
                        "id": largest_category.get("id"),
                        "count": largest_category.get("count")
                    },
                    "smallest_category": {
                        "name": smallest_category.get("name"),
                        "id": smallest_category.get("id"),
                        "count": smallest_category.get("count")
                    },
                    "categories_with_emails": sum(1 for cat in categories if cat.get("count", 0) > 0),
                    "empty_categories": sum(1 for cat in categories if cat.get("count", 0) == 0)
                }
            else:
                statistics = {
                    "total_categories": 0,
                    "total_emails_categorized": 0,
                    "average_emails_per_category": 0,
                    "categories_with_emails": 0,
                    "empty_categories": 0
                }
            
            return await self.handle_success(
                data=statistics,
                message="Category statistics retrieved successfully"
            )
            
        except Exception as e:
            return await self.handle_error(e, "get_category_statistics")
    
    async def batch_update_categories(self, category_updates: List[Dict[str, Any]]) -> ServiceResponse:
        """
        Update multiple categories in a batch operation.
        
        Args:
            category_updates: List of dictionaries containing category_id and update_data
            
        Returns:
            ServiceResponse with batch update results or error information
        """
        try:
            if not category_updates:
                return await self.handle_error(
                    ValueError("Category updates list cannot be empty"),
                    operation="batch_update_categories",
                    error_code="INVALID_INPUT"
                )
            
            results = []
            success_count = 0
            error_count = 0
            
            db = await self.get_db()
            
            for update in category_updates:
                category_id = update.get("category_id")
                update_data = update.get("update_data", {})
                
                if not category_id:
                    results.append({
                        "category_id": None,
                        "success": False,
                        "error": "Missing category_id"
                    })
                    error_count += 1
                    continue
                
                try:
                    updated_category = await db.update_category(category_id, update_data)
                    if updated_category:
                        results.append({
                            "category_id": category_id,
                            "success": True,
                            "data": CategoryResponse(**updated_category)
                        })
                        success_count += 1
                    else:
                        results.append({
                            "category_id": category_id,
                            "success": False,
                            "error": "Category not found"
                        })
                        error_count += 1
                except Exception as e:
                    results.append({
                        "category_id": category_id,
                        "success": False,
                        "error": str(e)
                    })
                    error_count += 1
            
            return await self.handle_success(
                data=results,
                message=f"Batch update completed: {success_count} succeeded, {error_count} failed",
                metadata={
                    "total_processed": len(category_updates),
                    "success_count": success_count,
                    "error_count": error_count
                }
            )
            
        except Exception as e:
            return await self.handle_error(e, "batch_update_categories")


# Dependency function for FastAPI
async def get_category_service() -> CategoryService:
    """
    Dependency injection function for CategoryService.
    
    Returns:
        CategoryService instance
    """
    service = CategoryService()
    return service