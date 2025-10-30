"""
Encryption utilities for data protection in the Email Intelligence Platform.
"""

import os
import base64
from typing import Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class DataEncryptionService:
    """
    Service for encrypting and decrypting sensitive data.
    """

    def __init__(self, password: str = None):
        """
        Initialize the encryption service.
        
        Args:
            password: Optional password to derive encryption key from.
                     If not provided, uses environment variable ENCRYPTION_KEY
                     or generates a new key.
        """
        if password:
            self.key = self._derive_key_from_password(password)
        elif os.getenv("ENCRYPTION_KEY"):
            key_from_env = os.getenv("ENCRYPTION_KEY")
            if len(key_from_env) != 44 or not all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_' for c in key_from_env):
                # If not in proper base64 format, derive from the string
                self.key = self._derive_key_from_password(key_from_env)
            else:
                self.key = key_from_env.encode()
        else:
            # Generate a new key
            self.key = Fernet.generate_key()
            # Save it to environment or a secure location for future use
            print(f"Generated encryption key: {self.key.decode()}")
            print("Please save this key in your environment variables as ENCRYPTION_KEY")

        self.cipher = Fernet(self.key)

    def _derive_key_from_password(self, password: str) -> bytes:
        """
        Derive encryption key from a password using PBKDF2.
        
        Args:
            password: Password to derive key from
            
        Returns:
            bytes: Encryption key
        """
        # In a real implementation, you'd want to use a more secure salt
        # that's unique per installation and stored separately
        salt = b'static_salt_for_demo_purposes_only'  # This should be unique per installation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # In production, adjust based on security needs
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt_data(self, data: Union[str, bytes]) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: Data to encrypt (string or bytes)
            
        Returns:
            str: Base64 encoded encrypted data
        """
        if isinstance(data, str):
            data = data.encode()
        encrypted_data = self.cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            str: Decrypted data
        """
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher.decrypt(encrypted_bytes)
        return decrypted_data.decode()


# Global instance for easy access
# In a real application, you would manage this differently to avoid global state
_encryption_service = None


def get_encryption_service() -> DataEncryptionService:
    """
    Get the global encryption service instance.
    
    Returns:
        DataEncryptionService: The encryption service instance
    """
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = DataEncryptionService()
    return _encryption_service


def encrypt_sensitive_data(data: Union[str, bytes]) -> str:
    """
    Convenience function to encrypt sensitive data using the global service.
    
    Args:
        data: Data to encrypt (string or bytes)
        
    Returns:
        str: Base64 encoded encrypted data
    """
    service = get_encryption_service()
    return service.encrypt_data(data)


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    Convenience function to decrypt sensitive data using the global service.
    
    Args:
        encrypted_data: Base64 encoded encrypted data
        
    Returns:
        str: Decrypted data
    """
    service = get_encryption_service()
    return service.decrypt_data(encrypted_data)