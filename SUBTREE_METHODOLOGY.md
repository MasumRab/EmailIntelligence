# Git Subtree Integration Methodology

## Overview

This document explains how to properly implement and use git subtrees for managing shared launch and setup files across different branches of the Email Intelligence Platform.

## Purpose

The goal of using git subtrees is to:

1. Maintain shared launch and setup files in a centralized location
2. Allow the main and scientific branches to diverge in their core functionality
3. Provide a mechanism to propagate setup improvements across branches
4. Reduce duplication of setup and launch code

## Directory Structure

After successful integration, the repository structure should look like:

```
EmailIntelligenceQwen/
├── src/
├── backend/
├── setup/          # This is the subtree containing shared launch/setup files
│   ├── launch.py
│   ├── launch.sh
│   ├── launch.bat
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── setup_environment_system.sh
│   ├── setup_environment_wsl.sh
│   └── README.md
└── other directories...
```

## Implementation Process

### For New Branch Setup

1. Create the setup subtree by adding the launch-setup-fixes branch as a subtree:

```bash
git subtree add --prefix=setup origin/launch-setup-fixes --squash
```

2. This creates a single commit that contains all the files from the launch-setup-fixes branch as a subdirectory

### Updating Subtrees

To pull updates from the setup branch to the current branch:

```bash
git subtree pull --prefix=setup origin/launch-setup-fixes --squash
```

### Pushing Changes to Subtree

To push changes made in the current branch back to the setup branch:

```bash
git subtree push --prefix=setup origin launch-setup-fixes
```

## Benefits

- Centralized management of launch and setup files
- Consistent setup experience across branches
- Independent development in main and scientific branches
- Clear separation of concerns

## Challenges

- Git subtree commands can be complex for team members
- Potential for merge conflicts when both parent and subtree branches change
- Requires discipline to use the correct workflow

## Alternative Approaches

If git subtrees prove too complex, other options include:

1. Git submodules - cleaner separation but more complex user workflow
2. Package management - distribute the setup as a separate package
3. Copy-based approach - manual copying with documentation of changes