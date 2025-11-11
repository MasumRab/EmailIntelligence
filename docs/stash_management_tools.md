# Stash Management Tools

This directory contains a comprehensive set of tools for managing Git stashes across multiple branches in the EmailIntelligence repository.

## Overview

The stash management system provides both automated and interactive tools to help resolve uncommitted work stored in Git stashes. Each stash contains work from various branches that needs to be properly applied to the correct branches.

## Available Scripts

### Core Stash Management
- `stash_manager.sh` - Main interface for all stash operations with interactive resolution capabilities
- `handle_stashes.sh` - Automated script to systematically process all stashes and apply them to correct branches
- `interactive_stash_resolver.sh` - Interactive conflict resolution when applying stashes with conflicts

### Analysis and Information
- `stash_analysis.sh` - Analyze stashes and provide recommendations on processing order
- `stash_details.sh` - Show detailed information about each stash before applying

## Usage

### Quick Start
```bash
# Get help with available commands
./scripts/stash_manager.sh help

# List all stashes
./scripts/stash_manager.sh list

# Show details of a specific stash
./scripts/stash_manager.sh show stash@{0}

# Apply a stash with interactive conflict resolution
./scripts/stash_manager.sh apply-interactive stash@{0}

# Process all stashes with interactive resolution
./scripts/stash_manager.sh process-all
```

### Systematic Stash Resolution
```bash
# 1. Analyze stashes and see processing recommendations
./scripts/stash_analysis.sh

# 2. Get detailed information about each stash
./scripts/stash_details.sh

# 3. Process all stashes automatically (with user confirmation)
./scripts/handle_stashes.sh

# 4. Or use the interactive resolver for more control
./scripts/interactive_stash_resolver.sh stash@{0}
```

## Documentation

- `docs/stash_resolution_procedure.md` - Basic procedure for resolving stashes
- `docs/complete_stash_resolution_procedure.md` - Complete procedure with all details
- `docs/interactive_stash_resolution.md` - Guide to using interactive conflict resolution

## Best Practices

1. **Start with analysis**: Always run `stash_analysis.sh` and `stash_details.sh` first
2. **Use interactive mode**: For important stashes, use interactive resolution to control conflicts
3. **Process systematically**: Follow the recommended order based on analysis
4. **Review changes**: Always review changes after applying stashes before committing
5. **Clean up**: Remove resolved stashes to keep the stash list clean

## Priority Processing Order

Based on the analysis, stashes should typically be processed in this order:
1. orchestration-tools (critical branch)
2. scientific (active development)
3. 002-validate-orchestration-tools (validation work)
4. feature/backend-to-src-migration (migration work)
5. Other branches as needed

## Troubleshooting

- If you encounter merge conflicts, use the interactive resolver
- If a target branch doesn't exist, the scripts will help you create it or find alternatives
- Always backup important work before starting the resolution process
- Check git status between operations to ensure clean state