with open("src/context_control/core.py", "r") as f:
    content = f.read()

content = content.replace("from .project import load_project_config, ProjectConfigLoader", "from .project import ProjectConfigLoader")

with open("src/context_control/core.py", "w") as f:
    f.write(content)
