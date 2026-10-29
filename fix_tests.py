import sys
with open('tests/core/test_security_sanitizer.py', 'r') as f:
    content = f.read()

content = content.replace("from src.core.security import DataSanitizer", "from src.core.security import DataSanitizer, sanitize_path")
content = content.replace("test_sanitize_path_invalid_chars(security_manager)", "test_sanitize_path_invalid_chars()")
content = content.replace("test_sanitize_path_unc(security_manager)", "test_sanitize_path_unc()")
content = content.replace("test_sanitize_path_traversal(security_manager)", "test_sanitize_path_traversal()")
content = content.replace("test_sanitize_path_null_byte(security_manager)", "test_sanitize_path_null_byte()")

with open('tests/core/test_security_sanitizer.py', 'w') as f:
    f.write(content)
