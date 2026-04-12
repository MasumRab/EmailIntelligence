with open("setup/launch.py", "r") as f:
    content = f.read()

# Add get_python_executable if it's missing or import it
if "from setup.environment import get_python_executable" not in content:
    content = content.replace("from setup.environment import (\n", "from setup.environment import (\n    get_python_executable,\n")

with open("setup/launch.py", "w") as f:
    f.write(content)
