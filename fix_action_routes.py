filepath = "src/backend/python_backend/main.py"
with open(filepath, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "action_routes" in line and "import" not in line and "ai_engine =" not in line and "app.include_router" not in line:
        continue
    if "app.include_router(action_routes.router)" in line:
        continue
    new_lines.append(line)

with open(filepath, "w") as f:
    f.writelines(new_lines)
