with open("src/core/exceptions.py", "r") as f:
    content = f.read()

content += """
class EmailNotFoundException(AppException):
    def __init__(self, message="Email not found"):
        super().__init__(message=message, status_code=404)
"""

with open("src/core/exceptions.py", "w") as f:
    f.write(content)
