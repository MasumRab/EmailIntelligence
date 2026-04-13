with open("src/core/audit_logger.py", "r") as f:
    content = f.read()

import re

# Fix PytestUnhandledThreadExceptionWarning where asyncio.TimeoutError is caught instead of queue.Empty
content = content.replace("import asyncio", "import asyncio\nimport queue")
content = content.replace("except asyncio.TimeoutError:", "except queue.Empty:")

with open("src/core/audit_logger.py", "w") as f:
    f.write(content)
