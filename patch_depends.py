filepath = "src/backend/python_backend/training_routes.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("from fastapi import APIRouter, BackgroundTasks, HTTPException", "from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends")

with open(filepath, "w") as f:
    f.write(content)
