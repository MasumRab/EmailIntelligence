with open("src/backend/python_backend/main.py", "r") as f:
    content = f.read()

new_content = content.replace("    action_routes,\n", "")

with open("src/backend/python_backend/main.py", "w") as f:
    f.write(new_content)
