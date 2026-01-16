# Interactive Stash Resolution Process

## Overview
This document describes the enhanced stash resolution process that includes interactive conflict resolution capabilities. The new system provides users with granular control over how conflicts are resolved when applying git stashes.

## Key Components

### 1. Interactive Stash Resolver (`interactive_stash_resolver.sh`)
A script that provides line-by-line conflict resolution options when applying stashes with conflicts.

**Features:**
- Shows conflict markers with context
- Offers multiple resolution options:
  - Accept all "theirs" changes (stashed changes)
  - Accept all "ours" changes (current branch)
  - Keep both versions
  - Edit manually in default editor
  - Skip file for later resolution
  - Abort entire operation

### 2. Enhanced Stash Manager (`stash_manager.sh`)
A comprehensive tool that provides all stash management functions with interactive options.

**Commands:**
- `list` - List all stashes
- `show <stash>` - Show details of a specific stash
- `apply <stash>` - Apply a stash (non-interactive)
- `apply-interactive <stash>` - Apply a stash with interactive conflict resolution
- `pop <stash>` - Apply and drop a stash (non-interactive)
- `pop-interactive <stash>` - Apply and drop a stash with interactive conflict resolution
- `save [message]` - Save current changes to a new stash
- `drop <stash>` - Drop a stash
- `clear` - Clear all stashes
- `analyze` - Analyze stashes and suggest processing order
- `process-all` - Process all stashes with interactive resolution

## How to Use

### Basic Interactive Application
```bash
# Apply a specific stash with interactive conflict resolution
./scripts/stash_manager.sh apply-interactive stash@{0}

# Show details of a stash before applying
./scripts/stash_manager.sh show stash@{0}
```

### Process All Stashes Interactively
```bash
# Process all stashes with interactive resolution
./scripts/stash_manager.sh process-all
```

### Direct Interactive Resolution
```bash
# Use the interactive resolver directly
./scripts/interactive_stash_resolver.sh stash@{0}
```

## Conflict Resolution Options

When conflicts are detected, the system offers these options:

1. **Accept "theirs"** - Keep the stashed changes and discard current branch changes
2. **Accept "ours"** - Keep current branch changes and discard stashed changes
3. **Keep both** - Include both versions of the conflicting content
4. **Manual edit** - Open the file in an editor to resolve conflicts manually
5. **Skip** - Leave the file unresolved and continue with others
6. **Abort** - Cancel the entire stash application

## Benefits

1. **Granular Control**: Users can make informed decisions about each conflict
2. **Safety**: Prevents accidental loss of important changes
3. **Flexibility**: Supports various conflict resolution strategies
4. **Transparency**: Shows exactly what changes are being applied
5. **Workflow Integration**: Works with existing orchestration tools workflow

## Best Practices

1. **Always Review**: Use `show` command to understand stash contents before applying
2. **Interactive First**: Use interactive mode for important stashes to prevent data loss
3. **Incremental Processing**: Process stashes one by one rather than all at once for better control
4. **Backup Strategy**: Consider creating a backup branch before processing multiple stashes
5. **Commit After Resolution**: Always verify and commit changes after successful stash application

## Integration with Orchestration Workflow

The new stash resolution tools are designed to work seamlessly with the existing orchestration workflow:
- Automatic branch synchronization when switching between branches
- Hook file management to prevent cross-branch contamination
- Warning system for changes that require PRs to orchestration-tools
- Validation of changes against orchestration standards

## Troubleshooting

### If conflicts persist after resolution:
1. Check `git status` to see remaining unmerged files
2. Manually edit files with remaining conflict markers
3. Add resolved files with `git add`
4. Commit the changes

### If stash application fails completely:
1. Use `git reset --hard HEAD` to return to clean state
2. Use `git stash apply --abort` to abort conflicted merge
3. Try alternative resolution strategy

## File Locations

- `scripts/interactive_stash_resolver.sh` - Core interactive resolution engine
- `scripts/stash_manager.sh` - Main stash management interface

The interactive stash resolution system provides a robust, user-controlled approach to managing complex stash conflicts while maintaining the flexibility to integrate with automated workflows when needed.