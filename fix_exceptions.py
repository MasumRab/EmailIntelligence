filepath = "src/core/exceptions.py"
with open(filepath, "r") as f:
    content = f.read()

if "EmailNotFoundException" not in content:
    content += """
class EmailNotFoundException(Exception):
    pass
"""
    with open(filepath, "w") as f:
        f.write(content)
