with open("src/core/exceptions.py", "r") as f:
    content = f.read()

content = content.replace("class EmailNotFoundException(AppException):", "class EmailNotFoundException(Exception):\n    pass")

with open("src/core/exceptions.py", "w") as f:
    f.write(content)
