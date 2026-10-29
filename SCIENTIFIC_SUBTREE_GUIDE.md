# Git Subtree Integration for Scientific Branch

## Overview

This document explains how to properly implement and use git subtrees for managing shared launch and setup files in the scientific branch of the Email Intelligence Platform.

## Purpose

The goal of using git subtrees in the scientific branch is to:

1. Maintain shared launch and setup files with other branches
2. Allow the scientific branch to continue its specialized development
3. Provide a mechanism to receive setup improvements from the central setup
4. Maintain consistency in launch procedures across branches

## Implementation Process

### For Scientific Branch Setup

1. Add the setup subtree from launch-setup-fixes branch:

```bash
git subtree add --prefix=setup origin/launch-setup-fixes --squash
```

2. This creates a single commit that contains all the files from the launch-setup-fixes branch as a subdirectory

### Updating Subtrees in Scientific Branch

To pull updates from the setup branch to the scientific branch:

```bash
git subtree pull --prefix=setup origin/launch-setup-fixes --squash
```

### Pushing Changes from Scientific Branch

To push changes made in the scientific branch back to the setup branch:

```bash
git subtree push --prefix=setup origin launch-setup-fixes
```

## Scientific Branch Considerations

- The scientific branch may have additional dependencies beyond the standard setup
- Ensure that any scientific-specific configurations are properly integrated with the shared launch infrastructure
- Test that scientific-specific features continue to work after subtree integration

## Benefits for Scientific Branch

- Consistent setup experience with other branches
- Access to centralized launch improvements
- Reduced maintenance overhead for setup files
- Maintained independence for scientific-specific features