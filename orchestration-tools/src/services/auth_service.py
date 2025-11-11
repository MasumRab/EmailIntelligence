import yaml
import os
from typing import Optional, List
from cryptography.fernet import Fernet
from ..models.user import User, UserRole


class AuthService:
    """
    Authentication and authorization service for the verification system
    """
    
    def __init__(self, config_path: str = "config/auth_config.yaml"):
        self.config_path = config_path
        self.users = {}
        self.roles = {}
        self._load_config()
    
    def _load_config(self):
        """Load authentication configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                self.roles = config.get('roles', {})
    
    def authenticate(self, api_key: str) -> Optional[User]:
        """
        Authenticate a user based on API key
        
        Args:
            api_key: The API key to authenticate
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # In a real implementation, this would check against a database
        # For now, we'll simulate a simple check
        if api_key and len(api_key) > 10:  # Simple validation
            # Create a mock user based on the default role in config
            default_role = "RUN"  # Default from our config
            permissions = self.roles.get(default_role, {}).get('permissions', [])
            
            user = User(
                id="user_123",
                username="default_user",
                api_key=api_key,
                role=default_role,
                permissions=permissions
            )
            return user
        return None
    
    def authorize(self, user: User, permission: str) -> bool:
        """
        Check if a user has a specific permission
        
        Args:
            user: The user to check
            permission: The permission to check for
            
        Returns:
            True if user has permission, False otherwise
        """
        return permission in user.permissions
    
    def has_role(self, user: User, required_role: UserRole) -> bool:
        """
        Check if a user has the required role or higher
        
        Args:
            user: The user to check
            required_role: The minimum required role
            
        Returns:
            True if user has required role or higher, False otherwise
        """
        role_hierarchy = {
            UserRole.READ: 1,
            UserRole.RUN: 2,
            UserRole.REVIEW: 3,
            UserRole.ADMIN: 4
        }
        
        user_role_level = role_hierarchy.get(user.role, 0)
        required_role_level = role_hierarchy.get(required_role, 0)
        
        return user_role_level >= required_role_level
    
    def encrypt_api_key(self, api_key: str) -> str:
        """
        Encrypt an API key for secure storage
        
        Args:
            api_key: The API key to encrypt
            
        Returns:
            Encrypted API key
        """
        # In a real implementation, use a proper encryption key
        # This is just for demonstration
        return f"encrypted_{api_key}"
    
    def decrypt_api_key(self, encrypted_api_key: str) -> str:
        """
        Decrypt an API key
        
        Args:
            encrypted_api_key: The encrypted API key
            
        Returns:
            Decrypted API key
        """
        # In a real implementation, use a proper decryption
        # This is just for demonstration
        if encrypted_api_key.startswith("encrypted_"):
            return encrypted_api_key[10:]
        return encrypted_api_key