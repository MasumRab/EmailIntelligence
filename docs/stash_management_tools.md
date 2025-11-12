# Stash Management Tools - Advanced Features

This directory contains a comprehensive set of tools for managing Git stashes across multiple branches in the EmailIntelligence repository.

## Overview

The stash management system provides both automated and interactive tools to help resolve uncommitted work stored in Git stashes. Each stash contains work from various branches that needs to be properly applied to the correct branches.

## Available Scripts

### Core Stash Management
- `stash_manager.sh` - Main interface for all stash operations with interactive resolution capabilities (deprecated, use optimized version)
- `stash_manager_optimized.sh` - Optimized main interface with improved performance and shared libraries
- `handle_stashes.sh` - Automated script to systematically process all stashes and apply them to correct branches (deprecated, use optimized version)
- `handle_stashes_optimized.sh` - Optimized automated script with improved performance and shared libraries
- `interactive_stash_resolver.sh` - Interactive conflict resolution when applying stashes with conflicts (deprecated, use optimized version)
- `interactive_stash_resolver_optimized.sh` - Optimized interactive resolver with improved performance and shared libraries

### Analysis and Information
- `stash_analysis.sh` - Analyze stashes and provide recommendations on processing order
- `stash_analysis_advanced.sh` - Advanced analysis with detailed statistics and recommendations
- `stash_details.sh` - Show detailed information about each stash before applying

### Shared Library
- `lib/stash_common.sh` - Common library with shared functions to avoid code duplication

## Advanced Features

### Enhanced Stash Manager Commands
```bash
# Advanced search for stashes containing specific patterns
./scripts/stash_manager_optimized.sh search "bugfix"

# Show which branch each stash belongs to
./scripts/stash_manager_optimized.sh branch-info

# Save current changes with branch information in the stash message
./scripts/stash_manager_optimized.sh save-with-branch feature/new-feature "WIP on feature/new-feature"
```

### Advanced Conflict Resolution
The optimized interactive resolver now includes:
- Detailed conflict visualization with color-coded sections
- Line-by-line conflict resolution options
- Preview mode to see conflicts before applying
- Advanced conflict resolution with specific line selection

### Enhanced Stash Processing
The optimized handle stashes script now includes:
- Better branch matching and creation logic
- Conflict detection with option for interactive resolution
- Stash statistics and age analysis
- Uncommitted changes handling on target branches

### Advanced Analysis
The new `stash_analysis_advanced.sh` provides:
- Detailed statistics by branch, age, and file type
- Processing recommendations based on priority
- Identification of potentially problematic stashes
- Content preview for each stash
- Cleanup suggestions for stale stashes

## Usage

### Quick Start
```bash
# Get help with available commands
./scripts/stash_manager_optimized.sh help

# List all stashes with branch information
./scripts/stash_manager_optimized.sh list

# Show details of a specific stash
./scripts/stash_manager_optimized.sh show stash@{0}

# Apply a stash with interactive conflict resolution
./scripts/stash_manager_optimized.sh apply-interactive stash@{0}

# Process all stashes with interactive resolution
./scripts/stash_manager_optimized.sh process-all

# Run advanced analysis
./scripts/stash_analysis_advanced.sh
```

### Advanced Stash Resolution Workflow
```bash
# 1. Run advanced analysis to understand your stashes
./scripts/stash_analysis_advanced.sh

# 2. Get detailed information about each stash
./scripts/stash_details.sh

# 3. Process all stashes with enhanced options
./scripts/handle_stashes_optimized.sh

# 4. Or use the interactive resolver for more control
./scripts/interactive_stash_resolver_optimized.sh --preview stash@{0}
```

## Documentation

- `docs/stash_resolution_procedure.md` - Basic procedure for resolving stashes
- `docs/complete_stash_resolution_procedure.md` - Complete procedure with all details
- `docs/interactive_stash_resolution.md` - Guide to using interactive conflict resolution

## Best Practices

1. **Start with analysis**: Always run `stash_analysis_advanced.sh` first to understand your stash landscape
2. **Use interactive mode**: For important stashes, use interactive resolution to control conflicts
3. **Process systematically**: Follow the recommended order based on analysis
4. **Review changes**: Always review changes after applying stashes before committing
5. **Clean up**: Remove resolved stashes to keep the stash list clean
6. **Use preview**: Use the preview option in interactive resolver to see conflicts before applying

## Priority Processing Order

Based on the analysis, stashes should typically be processed in this order:
1. orchestration-tools (critical branch)
2. scientific (active development)
3. 002-validate-orchestration-tools (validation work)
4. feature/backend-to-src-migration (migration work)
5. Other branches as needed

## Troubleshooting

- If you encounter merge conflicts, use the interactive resolver with preview mode
- If a target branch doesn't exist, the scripts will help you create it or find alternatives
- Always backup important work before starting the resolution process
- Check git status between operations to ensure clean state

## New Features Added

### Advanced Conflict Resolution
- Line-by-line conflict resolution options
- Preview mode to see conflicts before applying
- Color-coded conflict visualization
- Advanced conflict resolution with specific line selection

### Enhanced Analysis
- Detailed statistics by branch, age, and file type
- Processing recommendations based on priority
- Identification of potentially problematic stashes
- Content preview for each stash
- Cleanup suggestions for stale stashes

### Improved Processing
- Better branch matching and creation logic
- Conflict detection with option for interactive resolution
- Stash statistics and age analysis
- Uncommitted changes handling on target branches