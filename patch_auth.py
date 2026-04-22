import re
with open("src/backend/python_backend/main.py", "r") as f:
    content = f.read()

content = content.replace("db = await get_db()\n    user = await authenticate_user(username, password, db)", "from .database import get_db\n    db = await get_db()\n    user = await authenticate_user(username, password, db)")

with open("src/backend/python_backend/main.py", "w") as f:
    f.write(content)
