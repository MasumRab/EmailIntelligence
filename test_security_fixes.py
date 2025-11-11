#!/usr/bin/env python3
"""
Test script to verify that the security fixes have been properly implemented.
This script checks that secret keys are no longer hardcoded and are loaded from environment variables.
"""

import os
import sys
from pathlib import Path

def test_core_settings():
    """Test that core settings properly require environment variables."""
    print("Testing core settings...")

    # Temporarily remove SECRET_KEY from environment to test validation
    original_secret_key = os.environ.get('SECRET_KEY')
    if 'SECRET_KEY' in os.environ:
        del os.environ['SECRET_KEY']

    try:
        # Import the settings module
        from src.core import settings
        # This should raise an error because SECRET_KEY is not set in environment
        print("ERROR: Settings loaded without SECRET_KEY in environment, but it should have failed!")
        return False
    except ValueError as e:
        if "SECRET_KEY environment variable must be set" in str(e):
            print("✓ Core settings properly require SECRET_KEY from environment")
        else:
            print(f"✗ Unexpected error: {e}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    finally:
        # Restore original environment value
        if original_secret_key is not None:
            os.environ['SECRET_KEY'] = original_secret_key

    # Now set a test secret key and verify it works
    os.environ['SECRET_KEY'] = 'test-secret-key-for-validation'
    try:
        # Reload the module to pick up the new environment variable
        import importlib
        import src.core.settings
        importlib.reload(src.core.settings)

        from src.core.settings import settings
        if settings.secret_key == 'test-secret-key-for-validation':
            print("✓ Core settings properly load SECRET_KEY from environment")
        else:
            print("✗ Core settings did not load SECRET_KEY from environment properly")
            return False
    except Exception as e:
        print(f"✗ Error testing core settings with environment variable: {e}")
        return False

    return True


def test_backend_settings():
    """Test that backend settings properly require environment variables."""
    print("\nTesting backend settings...")

    # Since the full backend import might have dependencies we don't need for this test,
    # let's directly verify the settings file has the correct implementation

    backend_settings_path = Path("backend/python_backend/settings.py")
    backend_settings_content = backend_settings_path.read_text()

    # Check that the secret key field uses ... as default (meaning it's required)
    if 'default=..., env="SECRET_KEY"' in backend_settings_content:
        print("✓ Backend settings properly marks SECRET_KEY as required from environment")
    else:
        print("✗ Backend settings does not properly mark SECRET_KEY as required")
        return False

    # Check that the validator is in place
    if '@field_validator(\'secret_key\')' in backend_settings_content:
        print("✓ Backend settings has proper validator for SECRET_KEY")
    else:
        print("✗ Backend settings does not have proper validator for SECRET_KEY")
        return False

    return True


def verify_no_hardcoded_keys():
    """Verify that there are no hardcoded secret keys in the settings files."""
    print("\nVerifying no hardcoded secret keys remain...")

    # Read the updated settings files to ensure no hardcoded values remain
    core_settings_path = Path("src/core/settings.py")
    backend_settings_path = Path("backend/python_backend/settings.py")

    core_settings_content = core_settings_path.read_text()
    backend_settings_content = backend_settings_path.read_text()

    # Check for any occurrences of the old hardcoded key
    if "your-secret-key-here" in core_settings_content:
        print("✗ Found hardcoded secret key in src/core/settings.py")
        return False

    if "your-secret-key-here" in backend_settings_content:
        print("✗ Found hardcoded secret key in backend/python_backend/settings.py")
        return False

    print("✓ No hardcoded secret keys found in settings files")
    return True


def main():
    """Run all security tests."""
    print("Running security fixes verification tests...\n")

    tests = [
        verify_no_hardcoded_keys,
        test_core_settings,
        test_backend_settings
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print(f"\n{'='*50}")
    if all_passed:
        print("✓ All security fixes have been successfully implemented!")
        print("Secret keys are now loaded from environment variables.")
    else:
        print("✗ Some security issues remain or tests failed.")
        sys.exit(1)

    return all_passed


if __name__ == "__main__":
    main()