#!/usr/bin/env python3
"""
Setup script for installing Python linting and formatting tools.
Run this script to set up code quality tools for the EmailIntelligence project.
"""

import os
import subprocess
import sys


def install_packages():
    """Install required packages for code quality."""
    packages = ["black", "flake8", "isort", "pylint", "mypy"]

    print("Installing code quality packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + packages)
        print("Successfully installed packages.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

    return True


def create_config_files():
    """Create configuration files for linting tools."""
    # Create .flake8 configuration
    flake8_config = """[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist
ignore = E203, W503
"""

    # Create .pylintrc configuration
    pylintrc_config = """[MASTER]
disable=
    C0111, # missing-docstring
    C0103, # invalid-name
    C0303, # trailing-whitespace
    C0330, # bad-continuation
    C1801, # len-as-condition
    W0511, # fixme
    R0903, # too-few-public-methods
    R0913, # too-many-arguments

[FORMAT]
max-line-length=100

[SIMILARITIES]
min-similarity-lines=7
ignore-comments=yes
ignore-docstrings=yes
ignore-imports=yes
"""

    # Create pyproject.toml for Black and isort
    pyproject_toml = """[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
"""

    # Write configuration files
    with open(".flake8", "w") as f:
        f.write(flake8_config)

    with open(".pylintrc", "w") as f:
        f.write(pylintrc_config)

    # Append to existing pyproject.toml if it exists, otherwise create new
    if os.path.exists("pyproject.toml"):
        with open("pyproject.toml", "r") as f:
            existing_content = f.read()

        # Check if black and isort configs already exist
        if "[tool.black]" not in existing_content and "[tool.isort]" not in existing_content:
            with open("pyproject.toml", "a") as f:
                f.write("\n\n" + pyproject_toml)
    else:
        with open("pyproject.toml", "w") as f:
            f.write(pyproject_toml)

    print("Created configuration files for linting tools.")
    return True


def main():
    """Main function to set up linting tools."""
    print("Setting up Python linting and formatting tools...")

    if not install_packages():
        print("Failed to install packages. Exiting.")
        return 1

    if not create_config_files():
        print("Failed to create configuration files. Exiting.")
        return 1

    print("\nSetup complete! You can now use the following commands:")
    print("  - black . : Format code with Black")
    print("  - flake8 . : Check code style with Flake8")
    print("  - pylint server : Run Pylint on the server directory")
    print("  - isort . : Sort imports with isort")
    print("\nThese tools are also configured in VSCode settings.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
