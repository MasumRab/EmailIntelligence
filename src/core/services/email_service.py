"""
Refactored Email Service for Email Intelligence Platform
Handles all email-related business logic with improved structure and error handling
"""

import logging
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from .base_service import BaseService, ServiceResponse
from ..models import EmailResponse, EmailCreate, EmailUpdate
from ..database import FIELD_ID, FIELD_MESSAGE_ID
from ..exceptions import EmailNotFoundException, DatabaseError

logger = logging.getLogger(__name__)


class EmailService(BaseService):
    """
    Service class for email operations with enhanced functionality.
    
    Features:
    - Comprehensive email management operations
    - Advanced search and filtering
    - Statistics and analytics
    - Batch operations
    - Enhanced error handling
    """
    
    def __init__(self):
        super().__init__()
        self._db = None
        
    async def get_email_by_id(self, email_id: int) -> ServiceResponse:
        """
        Get an email by its internal ID.
        
        Args:
            email_id: The internal ID of the email
            
        Returns:
            ServiceResponse with email data or error information
        """
        try:
            db = await self.get_db()
            email = await db.get_email_by_id(email_id)
            
            if email:
                return await self.handle_success(
                    data=EmailResponse(**email),
                    message=f"Email with ID {email_id} retrieved successfully"
                )
            else:
                return await self.handle_error(
                    EmailNotFoundException(email_id=email_id),
                    operation="get_email_by_id",
                    error_code="EMAIL_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "get_email_by_id")
    
    async def get_email_by_message_id(self, message_id: str) -> ServiceResponse:
        """
        Get an email by its message ID.
        
        Args:
            message_id: The message ID of the email
            
        Returns:
            ServiceResponse with email data or error information
        """
        try:
            if not message_id:
                return await self.handle_error(
                    ValueError("Message ID cannot be empty"),
                    operation="get_email_by_message_id",
                    error_code="INVALID_INPUT"
                )
            
            db = await self.get_db()
            email = await db.get_email_by_message_id(message_id)
            
            if email:
                return await self.handle_success(
                    data=EmailResponse(**email),
                    message=f"Email with message ID {message_id} retrieved successfully"
                )
            else:
                return await self.handle_error(
                    EmailNotFoundException(message_id=message_id),
                    operation="get_email_by_message_id",
                    error_code="EMAIL_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "get_email_by_message_id")
    
    async def get_all_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> ServiceResponse:
        """
        Get all emails with optional filtering, pagination, and sorting.
        
        Args:
            limit: Number of emails to return
            offset: Number of emails to skip
            category_id: Optional category ID to filter by
            is_unread: Optional flag to filter unread emails
            sort_by: Field to sort by (created_at, subject, sender)
            sort_order: Sort order (asc or desc)
            
        Returns:
            ServiceResponse with list of emails or error information
        """
        try:
            # Validate parameters
            if limit <= 0 or limit > 1000:
                return await self.handle_error(
                    ValueError("Limit must be between 1 and 1000"),
                    operation="get_all_emails",
                    error_code="INVALID_INPUT"
                )
            
            if offset < 0:
                return await self.handle_error(
                    ValueError("Offset must be non-negative"),
                    operation="get_all_emails",
                    error_code="INVALID_INPUT"
                )
            
            db = await self.get_db()
            emails = await db.get_emails(
                limit=limit,
                offset=offset,
                category_id=category_id,
                is_unread=is_unread
            )
            
            # Convert to EmailResponse objects
            email_responses = [EmailResponse(**email) for email in emails]
            
            return await self.handle_success(
                data=email_responses,
                message=f"Retrieved {len(email_responses)} emails",
                metadata={
                    "limit": limit,
                    "offset": offset,
                    "total_count": len(emails),
                    "category_id": category_id,
                    "is_unread": is_unread
                }
            )
            
        except Exception as e:
            return await self.handle_error(e, "get_all_emails")
    
    async def create_email(self, email_data: Union[EmailCreate, Dict[str, Any]]) -> ServiceResponse:
        """
        Create a new email.
        
        Args:
            email_data: Email data to create (EmailCreate object or dict)
            
        Returns:
            ServiceResponse with created email or error information
        """
        try:
            # Convert to dict if it's a Pydantic model
            if isinstance(email_data, EmailCreate):
                email_dict = email_data.model_dump()
            else:
                email_dict = email_data
            
            # Validate required fields
            required_fields = ["sender", "senderEmail", "subject", "content"]
            if not await self.validate_input(email_dict, required_fields):
                return await self.handle_error(
                    ValueError(f"Missing required fields: {required_fields}"),
                    operation="create_email",
                    error_code="INVALID_INPUT"
                )
            
            db = await self.get_db()
            created_email = await db.create_email(email_dict)
            
            if created_email:
                return await self.handle_success(
                    data=EmailResponse(**created_email),
                    message="Email created successfully"
                )
            else:
                return await self.handle_error(
                    Exception("Failed to create email"),
                    operation="create_email",
                    error_code="EMAIL_CREATION_FAILED"
                )
                
        except Exception as e:
            return await self.handle_error(e, "create_email")
    
    async def update_email(self, email_id: int, update_data: Union[EmailUpdate, Dict[str, Any]]) -> ServiceResponse:
        """
        Update an email by its ID.
        
        Args:
            email_id: The ID of the email to update
            update_data: Email update data (EmailUpdate object or dict)
            
        Returns:
            ServiceResponse with updated email or error information
        """
        try:
            # Convert to dict if it's a Pydantic model
            if isinstance(update_data, EmailUpdate):
                update_dict = update_data.model_dump(exclude_unset=True)
            else:
                update_dict = update_data
            
            # Validate email exists
            get_result = await self.get_email_by_id(email_id)
            if not get_result.success:
                return get_result  # Return the error from get_email_by_id
            
            db = await self.get_db()
            updated_email = await db.update_email(email_id, update_dict)
            
            if updated_email:
                return await self.handle_success(
                    data=EmailResponse(**updated_email),
                    message=f"Email with ID {email_id} updated successfully"
                )
            else:
                return await self.handle_error(
                    EmailNotFoundException(email_id=email_id),
                    operation="update_email",
                    error_code="EMAIL_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "update_email")
    
    async def update_email_by_message_id(self, message_id: str, update_data: Union[EmailUpdate, Dict[str, Any]]) -> ServiceResponse:
        """
        Update an email by its message ID.
        
        Args:
            message_id: The message ID of the email to update
            update_data: Email update data (EmailUpdate object or dict)
            
        Returns:
            ServiceResponse with updated email or error information
        """
        try:
            # Convert to dict if it's a Pydantic model
            if isinstance(update_data, EmailUpdate):
                update_dict = update_data.model_dump(exclude_unset=True)
            else:
                update_dict = update_data
            
            # Validate email exists
            get_result = await self.get_email_by_message_id(message_id)
            if not get_result.success:
                return get_result  # Return the error from get_email_by_message_id
            
            db = await self.get_db()
            updated_email = await db.update_email_by_message_id(message_id, update_dict)
            
            if updated_email:
                return await self.handle_success(
                    data=EmailResponse(**updated_email),
                    message=f"Email with message ID {message_id} updated successfully"
                )
            else:
                return await self.handle_error(
                    EmailNotFoundException(message_id=message_id),
                    operation="update_email_by_message_id",
                    error_code="EMAIL_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "update_email_by_message_id")
    
    async def delete_email(self, email_id: int) -> ServiceResponse:
        """
        Delete an email by its ID.
        
        Args:
            email_id: The ID of the email to delete
            
        Returns:
            ServiceResponse with success or error information
        """
        try:
            # Validate email exists
            get_result = await self.get_email_by_id(email_id)
            if not get_result.success:
                return get_result  # Return the error from get_email_by_id
            
            db = await self.get_db()
            
            # Find the email in the data list and remove it
            # Note: This is a simplified implementation - in a real system,
            # you would implement proper deletion in the database layer
            email_data = db.emails_data
            email_index = next((i for i, email in enumerate(email_data) if email.get("id") == email_id), -1)
            
            if email_index != -1:
                deleted_email = email_data.pop(email_index)
                
                # Update indexes
                if hasattr(db, 'indexes'):
                    db.indexes.remove_email_index(email_id, deleted_email.get("message_id"))
                
                # Mark data as dirty for saving
                await db._save_data("emails")
                
                return await self.handle_success(
                    message=f"Email with ID {email_id} deleted successfully"
                )
            else:
                return await self.handle_error(
                    EmailNotFoundException(email_id=email_id),
                    operation="delete_email",
                    error_code="EMAIL_NOT_FOUND"
                )
                
        except Exception as e:
            return await self.handle_error(e, "delete_email")
    
    async def search_emails(self, search_term: str, limit: int = 50) -> ServiceResponse:
        """
        Search emails by term with enhanced search capabilities.
        
        Args:
            search_term: Term to search for
            limit: Maximum number of results to return
            
        Returns:
            ServiceResponse with search results or error information
        """
        try:
            if not search_term:
                return await self.handle_error(
                    ValueError("Search term cannot be empty"),
                    operation="search_emails",
                    error_code="INVALID_INPUT"
                )
            
            if limit <= 0 or limit > 1000:
                return await self.handle_error(
                    ValueError("Limit must be between 1 and 1000"),
                    operation="search_emails",
                    error_code="INVALID_INPUT"
                )
            
            db = await self.get_db()
            emails = await db.search_emails(search_term, limit)
            
            # Convert to EmailResponse objects
            email_responses = [EmailResponse(**email) for email in emails]
            
            return await self.handle_success(
                data=email_responses,
                message=f"Found {len(email_responses)} emails matching '{search_term}'",
                metadata={
                    "search_term": search_term,
                    "limit": limit,
                    "result_count": len(email_responses)
                }
            )
            
        except Exception as e:
            return await self.handle_error(e, "search_emails")
    
    async def get_emails_by_category(self, category_id: int, limit: int = 50, offset: int = 0) -> ServiceResponse:
        """
        Get emails by category with pagination.
        
        Args:
            category_id: Category ID to filter by
            limit: Number of emails to return
            offset: Number of emails to skip
            
        Returns:
            ServiceResponse with emails or error information
        """
        try:
            if category_id <= 0:
                return await self.handle_error(
                    ValueError("Category ID must be positive"),
                    operation="get_emails_by_category",
                    error_code="INVALID_INPUT"
                )
            
            db = await self.get_db()
            emails = await db.get_emails_by_category(category_id, limit, offset)
            
            # Convert to EmailResponse objects
            email_responses = [EmailResponse(**email) for email in emails]
            
            return await self.handle_success(
                data=email_responses,
                message=f"Retrieved {len(email_responses)} emails for category {category_id}",
                metadata={
                    "category_id": category_id,
                    "limit": limit,
                    "offset": offset,
                    "result_count": len(email_responses)
                }
            )
            
        except Exception as e:
            return await self.handle_error(e, "get_emails_by_category")
    
    async def get_statistics(self) -> ServiceResponse:
        """
        Get email statistics and analytics.
        
        Returns:
            ServiceResponse with statistics data or error information
        """
        try:
            db = await self.get_db()
            
            # Get various statistics
            total_count = await db.get_total_emails_count()
            auto_labeled_count = await db.get_auto_labeled_count()
            categories_count = await db.get_categories_count()
            weekly_growth = await db.get_weekly_growth()
            
            # Calculate additional metrics
            unlabeled_count = total_count - auto_labeled_count
            labeled_percentage = (auto_labeled_count / total_count * 100) if total_count > 0 else 0
            
            statistics = {
                "total_emails": total_count,
                "auto_labeled": auto_labeled_count,
                "unlabeled": unlabeled_count,
                "labeled_percentage": round(labeled_percentage, 2),
                "categories": categories_count,
                "weekly_growth": weekly_growth
            }
            
            return await self.handle_success(
                data=statistics,
                message="Email statistics retrieved successfully"
            )
            
        except Exception as e:
            return await self.handle_error(e, "get_statistics")
    
    async def batch_update_emails(self, email_updates: List[Dict[str, Any]]) -> ServiceResponse:
        """
        Update multiple emails in a batch operation.
        
        Args:
            email_updates: List of dictionaries containing email_id and update_data
            
        Returns:
            ServiceResponse with batch update results or error information
        """
        try:
            if not email_updates:
                return await self.handle_error(
                    ValueError("Email updates list cannot be empty"),
                    operation="batch_update_emails",
                    error_code="INVALID_INPUT"
                )
            
            results = []
            success_count = 0
            error_count = 0
            
            db = await self.get_db()
            
            for update in email_updates:
                email_id = update.get("email_id")
                update_data = update.get("update_data", {})
                
                if not email_id:
                    results.append({
                        "email_id": None,
                        "success": False,
                        "error": "Missing email_id"
                    })
                    error_count += 1
                    continue
                
                try:
                    updated_email = await db.update_email(email_id, update_data)
                    if updated_email:
                        results.append({
                            "email_id": email_id,
                            "success": True,
                            "data": EmailResponse(**updated_email)
                        })
                        success_count += 1
                    else:
                        results.append({
                            "email_id": email_id,
                            "success": False,
                            "error": "Email not found"
                        })
                        error_count += 1
                except Exception as e:
                    results.append({
                        "email_id": email_id,
                        "success": False,
                        "error": str(e)
                    })
                    error_count += 1
            
            return await self.handle_success(
                data=results,
                message=f"Batch update completed: {success_count} succeeded, {error_count} failed",
                metadata={
                    "total_processed": len(email_updates),
                    "success_count": success_count,
                    "error_count": error_count
                }
            )
            
        except Exception as e:
            return await self.handle_error(e, "batch_update_emails")


# Dependency function for FastAPI
async def get_email_service() -> EmailService:
    """
    Dependency injection function for EmailService.
    
    Returns:
        EmailService instance
    """
    service = EmailService()
    return service