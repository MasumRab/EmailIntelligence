filepath = "src/backend/python_backend/main.py"
with open(filepath, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'uvicorn.run("main:app", host=host, port=port, reload=reload, log_level="info")' in line:
        continue
    new_lines.append(line)

with open(filepath, "w") as f:
    f.writelines(new_lines)
