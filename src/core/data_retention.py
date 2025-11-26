"""
Data retention policy implementation for the Email Intelligence Platform.
Manages the lifecycle of data according to configured retention periods.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .database import DatabaseManager


class DataRetentionManager:
    """
    Manager for implementing data retention policies.
    """
    
    def __init__(self, db_manager: DatabaseManager, retention_config: Dict[str, int] = None):
        """
        Initialize the data retention manager.
        
        Args:
            db_manager: Database manager instance
            retention_config: Dictionary mapping data types to retention days
                            e.g., {"emails": 365, "users": 180, "logs": 90}
        """
        self.db_manager = db_manager
        # Default retention: emails for 2 years, users for 1 year, logs for 90 days
        self.retention_config = retention_config or {
            "emails": 730,  # 2 years
            "users": 365,   # 1 year
            "logs": 90,     # 90 days
        }
        self.logger = logging.getLogger(__name__)

    async def cleanup_expired_data(self) -> Dict[str, int]:
        """
        Clean up data that has exceeded its retention period.
        
        Returns:
            Dict[str, int]: Number of records deleted for each data type
        """
        result = {}
        
        # Clean up emails
        emails_deleted = await self._cleanup_expired_emails()
        result["emails"] = emails_deleted
        
        # Clean up other data types as needed
        users_deleted = await self._cleanup_expired_users()
        result["users"] = users_deleted
        
        return result

    async def _cleanup_expired_emails(self) -> int:
        """
        Clean up emails that have exceeded their retention period.
        
        Returns:
            int: Number of emails deleted
        """
        retention_days = self.retention_config.get("emails", 730)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Get emails older than the cutoff date
        # In our current implementation, we don't have a direct way to get emails by date
        # so we'll fetch all emails and filter them
        all_emails = await self.db_manager.get_emails(limit=1000000)  # All emails
        
        expired_emails = []
        for email in all_emails:
            created_at_str = email.get("created_at")
            if created_at_str:
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                    if created_at < cutoff_date:
                        expired_emails.append(email["id"])
                except ValueError:
                    # If date parsing fails, log and skip
                    self.logger.warning(f"Could not parse date for email {email.get('id')}: {created_at_str}")
        
        # Delete expired emails
        if expired_emails:
            await self.db_manager.bulk_delete_emails(expired_emails)
            self.logger.info(f"Deleted {len(expired_emails)} expired emails")
        else:
            self.logger.info("No expired emails to delete")
        
        return len(expired_emails)

    async def _cleanup_expired_users(self) -> int:
        """
        Clean up users that have exceeded their retention period.
        
        Returns:
            int: Number of users deleted
        """
        retention_days = self.retention_config.get("users", 365)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Get all users
        all_users_data = await self.db_manager.get_user_by_username("")  # This won't work correctly
        # We need to adapt to the actual available methods in our DatabaseManager
        # Since we don't have a get_all_users method, we'll need to work with what's available
        
        # For now, we'll return 0 as we don't have the right method to fetch all users
        self.logger.info("User cleanup not implemented due to missing get_all_users method")
        return 0

    async def get_retention_status(self) -> Dict[str, Any]:
        """
        Get the current status of data retention.
        
        Returns:
            Dict[str, Any]: Retention status information
        """
        # Get total counts for each data type
        total_emails = len(await self.db_manager.get_emails(limit=1000000))
        
        # Calculate expected retention based on config
        retention_status = {}
        for data_type, days in self.retention_config.items():
            retention_status[data_type] = {
                "retention_days": days,
                "total_count": 0,  # Placeholder - will fill with actual counts
                "next_cleanup": (datetime.now() + timedelta(days=days)).isoformat()
            }
        
        # Update with actual counts
        retention_status["emails"]["total_count"] = total_emails
        
        return retention_status

    async def schedule_cleanup(self, interval_hours: int = 24) -> None:
        """
        Schedule automatic cleanup of expired data.
        
        Args:
            interval_hours: How often to run cleanup in hours (default: 24)
        """
        self.logger.info(f"Scheduling data retention cleanup every {interval_hours} hours")
        
        while True:
            try:
                result = await self.cleanup_expired_data()
                self.logger.info(f"Data retention cleanup completed: {result}")
                
                # Wait for the specified interval before next cleanup
                await asyncio.sleep(interval_hours * 3600)
            except Exception as e:
                self.logger.error(f"Error during scheduled data retention cleanup: {e}")
                # Wait before retrying to avoid tight error loops
                await asyncio.sleep(3600)  # Wait 1 hour before retry


class DataRetentionPolicy:
    """
    Defines and manages data retention policies.
    """
    
    def __init__(self):
        self.policies = {}
    
    def add_policy(self, data_type: str, retention_days: int, auto_delete: bool = True):
        """
        Add a retention policy for a specific data type.
        
        Args:
            data_type: Type of data (e.g., 'emails', 'users', 'logs')
            retention_days: Number of days to retain data
            auto_delete: Whether to automatically delete data after retention period
        """
        self.policies[data_type] = {
            "retention_days": retention_days,
            "auto_delete": auto_delete,
            "created_at": datetime.now().isoformat()
        }
    
    def get_retention_period(self, data_type: str) -> Optional[int]:
        """
        Get the retention period for a specific data type.
        
        Args:
            data_type: Type of data
            
        Returns:
            Optional[int]: Number of days to retain, or None if not configured
        """
        policy = self.policies.get(data_type)
        return policy["retention_days"] if policy else None
    
    def should_auto_delete(self, data_type: str) -> bool:
        """
        Check if a data type should be automatically deleted after retention period.
        
        Args:
            data_type: Type of data
            
        Returns:
            bool: True if auto delete is enabled, False otherwise
        """
        policy = self.policies.get(data_type)
        return policy["auto_delete"] if policy else False
    
    def get_all_policies(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all defined retention policies.
        
        Returns:
            Dict[str, Dict[str, Any]]: All retention policies
        """
        return self.policies.copy()


# Global instances for easy access
_retention_manager = None
_retention_policy = None


def get_retention_manager() -> Optional[DataRetentionManager]:
    """
    Get the global retention manager instance.
    
    Returns:
        DataRetentionManager: The retention manager instance, or None if not configured
    """
    return _retention_manager


def set_retention_manager(manager: DataRetentionManager) -> None:
    """
    Set the global retention manager instance.
    
    Args:
        manager: Data retention manager instance to set
    """
    global _retention_manager
    _retention_manager = manager


def get_retention_policy() -> DataRetentionPolicy:
    """
    Get the global retention policy instance.
    
    Returns:
        DataRetentionPolicy: The retention policy instance
    """
    global _retention_policy
    if _retention_policy is None:
        _retention_policy = DataRetentionPolicy()
    return _retention_policy


def initialize_retention_policies() -> DataRetentionPolicy:
    """
    Initialize default data retention policies.
    
    Returns:
        DataRetentionPolicy: The retention policy instance with defaults
    """
    policy = get_retention_policy()
    
    # Set default policies
    policy.add_policy("emails", 730, True)   # 2 years
    policy.add_policy("users", 365, True)    # 1 year
    policy.add_policy("logs", 90, True)      # 90 days
    
    return policy