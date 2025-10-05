"""
A setuptools-based setup module for the Email Intelligence project.

This script is used to build, distribute, and install the Python packages
that are part of this project. It reads metadata from this file and
dependencies from the requirements.txt file.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
import os

from setuptools import find_packages, setup


def parse_requirements(filename="requirements.txt"):
    """
    Loads requirements from a pip requirements file.

    Args:
        filename (str): The name of the requirements file.

    Returns:
        A list of strings, where each string is a requirement.
    """
    # Construct the full path to the requirements file
    req_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(req_file_path):
        print(
            f"Warning: {filename} not found at {req_file_path}. No dependencies will be installed via install_requires."
        )
        return []
    with open(req_file_path, "r") as f:
        lineiter = (line.strip() for line in f)
        return [line for line in lineiter if line and not line.startswith("#")]


# Attempt to get the long description from a README.md file
long_description = "A longer description of your project."  # Default
readme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
if os.path.exists(readme_path):
    try:
        with open(readme_path, encoding="utf-8") as f:
            long_description = f.read()
    except Exception as e:
        print(f"Warning: Could not read README.md: {e}")

setup(
    # The name of the project.
    name="email_intelligence_project",  # TODO: Replace with your project's actual name
    # The version of the project.
    version="0.1.0",  # TODO: Replace with your project's version
    # The author of the project.
    author="Your Name",  # TODO: Replace with your name
    # The author's email address.
    author_email="your.email@example.com",  # TODO: Replace with your email
    # A short, one-sentence summary of the project.
    description="An intelligent email processing application.",  # TODO: Replace with a short description
    # A long description for the project, typically from the README.
    long_description=long_description,
    # The content type of the long description.
    long_description_content_type="text/markdown",  # Assumes README.md is markdown
    # The URL for the project's home page.
    url="https://github.com/yourusername/email_intelligence_project",  # TODO: Replace with your project's URL
    # Finds all packages automatically.
    packages=find_packages(),
    # A list of dependencies required for the project to run.
    install_requires=parse_requirements("requirements.txt"),
    # A list of classifiers to categorize the project.
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",  # Example: Specify compatible Python versions
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",  # TODO: Choose your license
        "Operating System :: OS Independent",
    ],
    # The minimum version of Python required to run the project.
    python_requires=">=3.8",  # TODO: Specify your minimum Python version
)