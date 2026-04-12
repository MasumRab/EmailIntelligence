import re

with open("src/main.py", "r") as f:
    content = f.read()

content = re.sub(r"__import__\('datetime'\)\.datetime\.utcnow\(\)", "datetime.now(timezone.utc)", content)
content = content.replace("import time\nimport hashlib\nimport os", "import time\nimport hashlib\nimport os\nfrom datetime import datetime, timezone")

with open("src/main.py", "w") as f:
    f.write(content)
