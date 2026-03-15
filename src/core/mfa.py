"""
Multi-Factor Authentication (MFA) service for the Email Intelligence Platform.

This module provides TOTP-based multi-factor authentication functionality,
including secret generation, QR code generation, and token verification.
"""

import logging
import secrets
from typing import Optional, Tuple, List

import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode

logger = logging.getLogger(__name__)


class MFAService:
    """Service for handling multi-factor authentication operations"""

    def __init__(self, issuer_name: str = "EmailIntelligence"):
        """
        Initialize the MFA service.
        
        Args:
            issuer_name: Name of the service for TOTP QR codes
        """
        self.issuer_name = issuer_name

    def generate_secret(self) -> str:
        """
        Generate a new TOTP secret.
        
        Returns:
            Base32 encoded secret string
        """
        return pyotp.random_base32()

    def generate_qr_code(self, username: str, secret: str) -> str:
        """
        Generate a QR code for TOTP setup.
        
        Args:
            username: Username for the TOTP URI
            secret: TOTP secret
            
        Returns:
            Base64 encoded QR code image
        """
        try:
            totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=username,
                issuer_name=self.issuer_name
            )
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for easy transmission
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = b64encode(buffer.getvalue()).decode()
            
            return img_str
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            raise

    def verify_token(self, secret: str, token: str) -> bool:
        """
        Verify a TOTP token.
        
        Args:
            secret: TOTP secret
            token: Token to verify
            
        Returns:
            True if token is valid, False otherwise
        """
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)  # Allow 1 window of drift
        except Exception as e:
            logger.error(f"Error verifying TOTP token: {e}")
            return False

    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """
        Generate backup codes for MFA.
        
        Args:
            count: Number of backup codes to generate
            
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate a 16-character backup code
            code = secrets.token_urlsafe(12)  # 12 bytes = 16 characters
            codes.append(code)
        return codes

    def verify_backup_code(self, backup_codes: List[str], code: str) -> Tuple[bool, Optional[List[str]]]:
        """
        Verify a backup code and return updated list without the used code.
        
        Args:
            backup_codes: List of backup codes
            code: Code to verify
            
        Returns:
            Tuple of (is_valid, updated_backup_codes)
        """
        if code in backup_codes:
            updated_codes = [c for c in backup_codes if c != code]
            return True, updated_codes
        return False, backup_codes


# Global MFA service instance
mfa_service = MFAService()


def get_mfa_service() -> MFAService:
    """Get the global MFA service instance"""
    return mfa_service