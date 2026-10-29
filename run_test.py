import pytest
import sys
sys.exit(pytest.main(["-c", "/dev/null", "-q", "--disable-warnings", "tests/core/test_security_sanitizer.py"]))
