# Task: Create Setup Subtree Directory Structure

## Description
Create the directory structure that will house the setup files for the subtree approach. This involves creating a dedicated `/setup` directory and moving appropriate files into it.

## Steps
1. Create `/setup` directory in the repository root
2. Move identified setup and launch files into the `/setup` directory
3. Ensure all file paths and imports are updated accordingly
4. Create a README.md in the setup directory explaining its purpose

## Subtasks
- [x] Create `/setup` directory
- [x] Move launch files to `/setup` directory
- [x] Move setup script files to `/setup` directory
- [x] Move configuration files to `/setup` directory
- [x] Update README.md in setup directory
- [x] Update any relative paths in moved files if necessary

## Acceptance Criteria
- [x] All identified setup files are moved to `/setup` directory
- [x] Files function correctly from new location
- [x] README.md clearly explains the setup directory's purpose
- [x] No broken references to moved files remain

## Task Dependencies
- task-subtree-migration-1 - Identify-Core-Launch-Setup-Files.md

## Priority
High

## Effort Estimate
4 hours

## Status
Completed

## Completion Notes
Successfully created the `/setup` directory and moved all identified launch and setup files:
- launch.py, launch.sh, launch.bat
- setup_environment_system.sh, setup_environment_wsl.sh
- setup_python.sh
- pyproject.toml, requirements.txt, requirements-dev.txt
- .gitattributes
- Created setup/README.md with proper documentation
- Created setup/.env.example as a template

Also updated launch.py to:
- Modify import path to correctly access deployment/test_stages.py from its new location
- Update find_project_root() function to account for its new location in the setup directory