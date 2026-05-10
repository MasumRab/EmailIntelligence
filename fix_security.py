with open("src/core/security.py", "r") as f:
    content = f.read()

import re

# Fix syntax error in security.py
old_block = """                data = re.sub(
                    rf'(\\b{re.escape(key)}\\b\\s*:\\s*)[^\\s,]+',
                    r'\\1[REDACTED]',
                    data,
                    flags=re.IGNORECASE
                    rf"(\\b{re.escape(key)}\\b\\s*:\\s*)[^\\s,]+",
                    r"\\1[REDACTED]",
                    data,
                    flags=re.IGNORECASE,
                )"""

new_block = """                data = re.sub(
                    rf'(\\b{re.escape(key)}\\b\\s*:\\s*)[^\\s,]+',
                    r'\\1[REDACTED]',
                    data,
                    flags=re.IGNORECASE,
                )"""

content = content.replace(old_block, new_block)

with open("src/core/security.py", "w") as f:
    f.write(content)
