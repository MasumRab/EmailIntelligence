# Constitution Synchronization Process

## Overview

This document describes the process for maintaining consistency of the constitution files across all repositories in the Email Intelligence Platform. The synchronization system ensures that all repositories use the same enhanced constitution while allowing for repository-specific extensions where needed.

## Synchronization Script

The `sync_constitution.py` script is responsible for copying the master constitution file to all other repositories. The script:

1. Identifies all `constitution.md` files in the project
2. Reads the master constitution file from `EmailIntelligence/constitution.md`
3. Updates each constitution file with the master content if different
4. Creates backup files (with `.backup` extension) before updating

### Usage

```bash
python sync_constitution.py [base_directory]
```

If no base directory is specified, the script will use the current working directory.

### Execution

The script will:
1. Show which master constitution file is being used
2. List all constitution files found in the directory structure
3. Update any constitution files that differ from the master
4. Create backups before making changes
5. Report which files were updated

## Master Constitution

The master constitution file is located at:
- `EmailIntelligence/constitution.md`

This file should be considered the canonical source for the constitution content. Any changes to the constitution should be made to this file first, then propagated to other repositories using the synchronization script.

## Synchronization Process

### Manual Synchronization

1. Make changes to the master constitution file in `EmailIntelligence/constitution.md`
2. Run the sync script: `python sync_constitution.py`
3. Verify the changes were propagated correctly
4. Commit the changes in each repository

### Before Committing Changes

1. Update the master constitution file with your changes
2. Run the synchronization script to propagate changes
3. Review the diff of the updated files to ensure correctness
4. Commit changes to each repository with consistent commit messages

## Automated Synchronization

To ensure consistency, consider adding the synchronization script to your CI/CD pipeline to:

1. Verify constitution consistency across repositories
2. Automatically update constitution files during builds
3. Alert when constitution files are out of sync

## File Locations

The synchronization script will update constitution files at these locations:

- `EmailIntelligence/.specify/memory/constitution.md`
- `EmailIntelligence/constitution.md` (master)
- `EmailIntelligenceQwen/.specify/memory/constitution.md`
- `EmailIntelligenceGem/.specify/memory/constitution.md`
- `EmailIntelligenceAuto/.specify/memory/constitution.md`

## Backup and Recovery

The synchronization script creates backup files (with `.backup` extension) before updating any constitution files. These backups can be used to recover previous versions if needed.

## Governance

Changes to the constitution should follow the governance process outlined in the constitution itself. The synchronization process supports this by:

1. Maintaining a single source of truth (the master constitution)
2. Preserving the version information in the constitution files
3. Creating backups before making changes
4. Allowing for verification of the synchronization process

## Best Practices

1. Always make changes to the master constitution file first
2. Run the synchronization script before committing changes
3. Review the diff of updated files before committing
4. Use consistent commit messages when updating constitution files
5. Update the version information in the constitution when making significant changes