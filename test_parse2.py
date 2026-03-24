import ast
try:
    with open('setup/services.py', 'r') as f:
        ast.parse(f.read())
    print("Parsed successfully!")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}, offset {e.offset}: {e.msg}")
