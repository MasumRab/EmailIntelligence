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

This directory provides consistent launch and setup experiences across all branches of the project. The setup files are maintained centrally on the orchestration-tools branch and synchronized to other branches via Git hooks, ensuring a unified setup process.

## Branch Integration

**On orchestration-tools branch**:
- This setup directory is the authoritative source
- All scripts are maintained here
- Other branches sync from this branch

**On development branches** (scientific, main, etc.):
- Setup directory is synchronized via Git hooks
- `.taskmaster/` submodule provides task management
- Together they provide a complete development environment

## Usage

The launch scripts should be run from the project root directory:

```bash
# Using the launcher
python setup/launch.py

# Or via shell script (Unix)
bash setup/launch.sh

# Or via batch script (Windows)
setup\launch.bat
```

## Git Synchronization

These files are automatically synchronized across branches:
- Git hooks detect changes to setup/
- Changes are propagated to other branches
- No manual subtree commands needed
- Standard Git workflow applies