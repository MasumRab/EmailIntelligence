with open("src/context_control/project.py", "r") as f:
    content = f.read()

content = content.replace('"""Load project configuration from various sources.\n        Returns:\n            ProjectConfig instance with merged settings', '"""Load project configuration from various sources.\n        Returns:\n            ProjectConfig instance with merged settings\n        """')

with open("src/context_control/project.py", "w") as f:
    f.write(content)
