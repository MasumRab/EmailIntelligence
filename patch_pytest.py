with open("pyproject.toml", "r") as f:
    content = f.read()

if "[tool.pytest.ini_options]" not in content:
    content += "\n[tool.pytest.ini_options]\naddopts = \"--ignore=src/backend/python_backend/tests --ignore=scripts\"\ntestpaths = [\"tests\", \"src/backend/python_nlp/tests\"]\n"

with open("pyproject.toml", "w") as f:
    f.write(content)
