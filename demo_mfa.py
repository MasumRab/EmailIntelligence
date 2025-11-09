"""
Demo script for MFA implementation
"""

import asyncio
from src.core.mfa import MFAService
import pyotp


async def demo_mfa():
    print("Email Intelligence Platform - MFA Demo")
    print("=" * 50)

    # Initialize MFA service
    mfa_service = MFAService()

    # 1. Generate MFA secret
    print("\n1. Generating MFA secret...")
    secret = mfa_service.generate_secret()
    print("   Secret generated and handled securely. (Not displayed)")

    # 2. Generate QR code for authenticator app
    print("\n2. Generating QR code for authenticator app setup...")
    username = "demo_user"
    qr_code_data = mfa_service.generate_qr_code(username, secret)
    print(f"   QR code generated (base64 length: {len(qr_code_data)} chars)")

    # 3. Generate backup codes
    print("\n3. Generating backup codes...")
    backup_codes = mfa_service.generate_backup_codes(5)
    print("   Backup codes:")
    for i, code in enumerate(backup_codes, 1):
        print(f"     {i}. {code}")

    # 4. Simulate TOTP verification
    print("\n4. Simulating TOTP verification...")
    totp = pyotp.TOTP(secret)
    current_token = totp.now()
    print(f"   Current TOTP token: {current_token}")

    # Verify the token
    is_valid = mfa_service.verify_token(secret, current_token)
    print(f"   Token verification result: {is_valid}")

    # Also test with an invalid token
    is_invalid = mfa_service.verify_token(secret, "123456")
    print(f"   Invalid token verification result: {is_invalid}")

    # 5. Test backup code verification
    print("\n5. Testing backup code verification...")
    print(f"   Original backup codes: {len(backup_codes)}")

    # Use the first backup code
    used_code = backup_codes[0]
    print(f"   Using backup code: {used_code}")

    is_valid, updated_codes = mfa_service.verify_backup_code(backup_codes, used_code)
    print(f"   Backup code verification result: {is_valid}")
    print(f"   Remaining backup codes: {len(updated_codes)}")

    print("\nMFA Demo completed successfully!")
    print("\nNote: In a real application:")
    print(
        "- The QR code would be displayed to the user to scan with their authenticator app"
    )
    print("- The secret would be stored securely in the user's record")
    print("- Backup codes would be shown to the user only once during setup")
    print("- All codes would be verified during the login process")


if __name__ == "__main__":
    asyncio.run(demo_mfa())
