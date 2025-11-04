"""
Action Routes for the Email Intelligence Platform.

This module defines API routes for handling various email actions such as
archiving, moving, flagging, deleting, and other custom actions.
"""
import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from .dependencies import get_ai_engine, get_db
from .database import DatabaseManager
from .ai_engine import AdvancedAIEngine
from .models import ActionRequest, ActionResponse, EmailResponse
from src.core.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()


async def get_db():
    """Database dependency for backward compatibility"""
    from .database import get_db as get_database
    return await get_database()


@router.post("/api/actions/archive", response_model=ActionResponse)
async def archive_email(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Archives one or more emails.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        success_count = 0
        failed_ids = []
        
        for email_id in request.email_ids:
            try:
                # Archive the email in the database
                updated_email = await db.update_email(email_id, {"archived": True})
                if updated_email:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to archive email {email_id}: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully archived {success_count}/{len(request.email_ids)} emails"
        if failed_ids:
            message += f". Failed to archive: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error archiving emails: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to archive emails")


@router.post("/api/actions/delete", response_model=ActionResponse)
async def delete_email(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Deletes one or more emails permanently.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        success_count = 0
        failed_ids = []
        
        for email_id in request.email_ids:
            try:
                # Delete the email from the database
                deleted = await db.delete_email(email_id)
                if deleted:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to delete email {email_id}: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully deleted {success_count}/{len(request.email_ids)} emails"
        if failed_ids:
            message += f". Failed to delete: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error deleting emails: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete emails")


@router.post("/api/actions/mark_read", response_model=ActionResponse)
async def mark_read_email(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Marks one or more emails as read.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        success_count = 0
        failed_ids = []
        
        for email_id in request.email_ids:
            try:
                # Mark the email as read in the database
                updated_email = await db.update_email(email_id, {"is_read": True})
                if updated_email:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to mark email {email_id} as read: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully marked {success_count}/{len(request.email_ids)} emails as read"
        if failed_ids:
            message += f". Failed to mark as read: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error marking emails as read: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to mark emails as read")


@router.post("/api/actions/mark_unread", response_model=ActionResponse)
async def mark_unread_email(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Marks one or more emails as unread.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        success_count = 0
        failed_ids = []
        
        for email_id in request.email_ids:
            try:
                # Mark the email as unread in the database
                updated_email = await db.update_email(email_id, {"is_read": False})
                if updated_email:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to mark email {email_id} as unread: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully marked {success_count}/{len(request.email_ids)} emails as unread"
        if failed_ids:
            message += f". Failed to mark as unread: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error marking emails as unread: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to mark emails as unread")


@router.post("/api/actions/flag", response_model=ActionResponse)
async def flag_email(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Flags one or more emails for attention.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        success_count = 0
        failed_ids = []
        
        for email_id in request.email_ids:
            try:
                # Flag the email in the database
                updated_email = await db.update_email(email_id, {"flagged": True})
                if updated_email:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to flag email {email_id}: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully flagged {success_count}/{len(request.email_ids)} emails"
        if failed_ids:
            message += f". Failed to flag: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error flagging emails: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to flag emails")


@router.post("/api/actions/unflag", response_model=ActionResponse)
async def unflag_email(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Removes flag from one or more emails.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        success_count = 0
        failed_ids = []
        
        for email_id in request.email_ids:
            try:
                # Remove flag from the email in the database
                updated_email = await db.update_email(email_id, {"flagged": False})
                if updated_email:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to unflag email {email_id}: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully unflagged {success_count}/{len(request.email_ids)} emails"
        if failed_ids:
            message += f". Failed to unflag: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error unflagging emails: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to unflag emails")


@router.post("/api/actions/custom", response_model=ActionResponse)
async def perform_custom_action(
    request: ActionRequest,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """
    Performs a custom action based on the provided action name and parameters.
    Requires authentication.
    """
    try:
        if not request.email_ids:
            raise HTTPException(status_code=400, detail="Email IDs are required")
        
        if not request.action_name:
            raise HTTPException(status_code=400, detail="Action name is required")
        
        success_count = 0
        failed_ids = []
        messages = []
        
        for email_id in request.email_ids:
            try:
                # Process the custom action based on the action name
                if request.action_name == "spam":
                    updated_email = await db.update_email(email_id, {"is_spam": True, "archived": True})
                elif request.action_name == "important":
                    updated_email = await db.update_email(email_id, {"priority": "high"})
                elif request.action_name == "move_to_folder":
                    if request.action_params and "folder" in request.action_params:
                        updated_email = await db.update_email(email_id, {"folder": request.action_params["folder"]})
                    else:
                        failed_ids.append(email_id)
                        continue
                elif request.action_name == "add_label":
                    if request.action_params and "label" in request.action_params:
                        email = await db.get_email_by_id(email_id)
                        if email:
                            labels = email.get("labels", [])
                            if request.action_params["label"] not in labels:
                                labels.append(request.action_params["label"])
                            updated_email = await db.update_email(email_id, {"labels": labels})
                        else:
                            failed_ids.append(email_id)
                            continue
                    else:
                        failed_ids.append(email_id)
                        continue
                else:
                    # Unknown action
                    failed_ids.append(email_id)
                    messages.append(f"Unknown action: {request.action_name}")
                    continue
                
                if updated_email:
                    success_count += 1
                else:
                    failed_ids.append(email_id)
            except Exception as e:
                logger.error(f"Failed to perform custom action {request.action_name} on email {email_id}: {str(e)}", exc_info=True)
                failed_ids.append(email_id)
        
        message = f"Successfully performed custom action '{request.action_name}' on {success_count}/{len(request.email_ids)} emails"
        if messages:
            message += "; " + "; ".join(messages)
        if failed_ids:
            message += f". Failed for: {failed_ids}"
        
        return ActionResponse(
            success=len(failed_ids) == 0,
            message=message,
            processedCount=success_count,
            failedIds=failed_ids
        )
    except Exception as e:
        logger.error(f"Error performing custom action {request.action_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to perform custom action {request.action_name}")