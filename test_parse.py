import ast
try:
    with open("setup/launch.py", "r") as f:
        content = f.read()
    ast.parse(content)
    print("Parsed launch.py successfully")
except Exception as e:
    import traceback
    traceback.print_exc()

try:
    with open("setup/services.py", "r") as f:
        content = f.read()
    ast.parse(content)
    print("Parsed services.py successfully")
except Exception as e:
    import traceback
    traceback.print_exc()
