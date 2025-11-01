"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Email service for the Email Intelligence Platform
Handles all email-related business logic
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from .base_service import BaseService, BaseResponse
from src.core.models import EmailResponse, EmailCreate, EmailUpdate
from src.core.database import FIELD_ID, FIELD_MESSAGE_ID


class EmailService(BaseService):
    """Service class for email operations"""

    def __init__(self):
        super().__init__()
        self._db = None

    async def get_db(self):
        """Get database instance"""
        if self._db is None:
            self._db = await super().get_db()
        return self._db

    async def get_email_by_id(self, email_id: int) -> BaseResponse:
        """Get an email by its internal ID"""
        try:
            db = await self.get_db()
            email = await db.get_email_by_id(email_id)
            if email:
                return BaseResponse(
                    success=True, message="Email retrieved successfully", data=email
                )
            else:
                return BaseResponse(
                    success=False,
                    message=f"Email with ID {email_id} not found",
                    error="Email not found",
                )
        except Exception as e:
            return await self.handle_error(e, "get_email_by_id")

    async def get_email_by_message_id(self, message_id: str) -> BaseResponse:
        """Get an email by its message ID"""
        try:
            db = await self.get_db()
            email = await db.get_email_by_message_id(message_id)
            if email:
                return BaseResponse(
                    success=True, message="Email retrieved successfully", data=email
                )
            else:
                return BaseResponse(
                    success=False,
                    message=f"Email with message ID {message_id} not found",
                    error="Email not found",
                )
        except Exception as e:
            return await self.handle_error(e, "get_email_by_message_id")

    async def get_all_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> BaseResponse:
        """Get all emails with optional filtering and pagination"""
        try:
            db = await self.get_db()
            emails = await db.get_emails(
                limit=limit, offset=offset, category_id=category_id, is_unread=is_unread
            )
            return BaseResponse(success=True, message="Emails retrieved successfully", data=emails)
        except Exception as e:
            return await self.handle_error(e, "get_all_emails")

    async def create_email(self, email_data: Dict[str, Any]) -> BaseResponse:
        """Create a new email"""
        try:
            db = await self.get_db()
            created_email = await db.create_email(email_data)
            if created_email:
                return BaseResponse(
                    success=True, message="Email created successfully", data=created_email
                )
            else:
                return BaseResponse(
                    success=False, message="Failed to create email", error="Email creation failed"
                )
        except Exception as e:
            return await self.handle_error(e, "create_email")

    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> BaseResponse:
        """Update an email by its ID"""
        try:
            db = await self.get_db()
            updated_email = await db.update_email(email_id, update_data)
            if updated_email:
                return BaseResponse(
                    success=True, message="Email updated successfully", data=updated_email
                )
            else:
                return BaseResponse(
                    success=False,
                    message=f"Email with ID {email_id} not found",
                    error="Email not found",
                )
        except Exception as e:
            return await self.handle_error(e, "update_email")

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> BaseResponse:
        """Update an email by its message ID"""
        try:
            db = await self.get_db()
            updated_email = await db.update_email_by_message_id(message_id, update_data)
            if updated_email:
                return BaseResponse(
                    success=True, message="Email updated successfully", data=updated_email
                )
            else:
                return BaseResponse(
                    success=False,
                    message=f"Email with message ID {message_id} not found",
                    error="Email not found",
                )
        except Exception as e:
            return await self.handle_error(e, "update_email_by_message_id")

    async def search_emails(self, search_term: str, limit: int = 50) -> BaseResponse:
        """Search emails by term"""
        try:
            db = await self.get_db()
            emails = await db.search_emails(search_term, limit)
            return BaseResponse(
                success=True,
                message=f"Found {len(emails)} emails matching '{search_term}'",
                data=emails,
            )
        except Exception as e:
            return await self.handle_error(e, "search_emails")

    async def get_total_emails_count(self) -> int:
        """Get the total count of emails in the system."""
        try:
            db = await self.get_db()
            count = await db.get_total_emails_count()
            return count
        except Exception:
            # Return a default value in case of error
            return 0

    async def get_auto_labeled_count(self) -> int:
        """Get the count of emails that have been auto-labeled."""
        try:
            db = await self.get_db()
            count = await db.get_auto_labeled_count()
            return count
        except Exception:
            # Return a default value in case of error
            return 0

    async def get_categories_count(self) -> int:
        """Get the total number of categories."""
        try:
            db = await self.get_db()
            count = await db.get_categories_count()
            return count
        except Exception:
            # Return a default value in case of error
            return 0

    async def get_weekly_growth(self) -> Dict[str, Any]:
        """Get the weekly growth statistics."""
        try:
            db = await self.get_db()
            growth_data = await db.get_weekly_growth()
            return growth_data
        except Exception:
            # Return default values in case of error
            return {"emails": 0, "percentage": 0.0}
