import re

with open("src/context_control/models.py", "r") as f:
    content = f.read()

content = content.replace("from datetime import datetime", "from datetime import datetime, timezone")

# Replace default_factory=datetime.utcnow with lambda: datetime.now(timezone.utc)
content = re.sub(r"default_factory=datetime\.utcnow", "default_factory=lambda: datetime.now(timezone.utc)", content)

with open("src/context_control/models.py", "w") as f:
    f.write(content)
