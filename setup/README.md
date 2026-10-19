# Setup Directory

This directory contains all the launch and setup files for the Email Intelligence Platform. These files are branch-agnostic and can be used across different branches of the project (main, scientific, etc.).

## Contents

- `launch.py` - Main launcher script for the Email Intelligence Platform
- `launch.sh` - Unix launch script
- `launch.bat` - Windows launch script
- `setup_environment_system.sh` - System-specific setup script
- `setup_environment_wsl.sh` - WSL-specific setup script
- `setup_python.sh` - Python setup script
- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - Runtime dependencies
- `requirements-dev.txt` - Development dependencies

## Purpose

This directory is designed to be used as a git subtree that can be easily integrated into different branches of the project. This allows for consistent launch and setup experiences across all branches while keeping the setup files separate from the main application logic.

## Usage

When using this as a subtree in other branches:

1. The launch scripts should be run from the project root directory
2. Update the paths in the setup scripts if needed to access the main project code
3. Ensure that the requirements files are properly referenced in the project's setup process