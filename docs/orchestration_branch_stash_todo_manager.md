# Human-in-the-Loop Stash Resolution Todo Manager

## Overview

The `stash_todo_manager.sh` script provides a structured workflow for managing unpushed Git stashes with human oversight. It creates a todo list of stashes that need resolution and allows users to work through them systematically with various resolution options.

## Features

- **Todo List Management**: Create, view, and manage a todo list of unpushed stashes
- **Human-in-the-Loop**: Each stash requires explicit user action before being marked as resolved
- **Multiple Resolution Options**: Apply interactively, apply directly, drop, or save to branch
- **Progress Tracking**: Monitor resolution progress with status reports
- **Import/Export**: Save and restore todo lists between sessions
- **Backup System**: Automatic backup of todo lists on exit

## Usage

### Initialize Todo List
```bash
./scripts/stash_todo_manager.sh init
```
Creates a todo list from all unpushed stashes in the repository.

### List Todo Items
```bash
./scripts/stash_todo_manager.sh list
```
Displays all todo items with their current status (pending, resolved, skipped).

### Resolve Specific Item
```bash
./scripts/stash_todo_manager.sh resolve <item_id>
```
Work on a specific stash with interactive resolution options:
1. Apply interactively (resolve conflicts)
2. Apply without conflicts (if possible)
3. Drop the stash
4. Save to branch and push
5. Skip for now

### Show Item Details
```bash
./scripts/stash_todo_manager.sh show <item_id>
```
Display detailed information about a specific todo item, including stash contents.

### Skip Item
```bash
./scripts/stash_todo_manager.sh skip <item_id>
```
Mark an item as skipped without taking any action on the stash.

### Remove Item
```bash
./scripts/stash_todo_manager.sh remove <item_id>
```
Remove an item from the todo list completely.

### Check Progress
```bash
./scripts/stash_todo_manager.sh status
```
Show resolution progress with statistics.

### Export/Import Todo List
```bash
./scripts/stash_todo_manager.sh export <file>
./scripts/stash_todo_manager.sh import <file>
```
Save or restore todo lists to/from files.

### Reset Todo List
```bash
./scripts/stash_todo_manager.sh reset
```
Clear the current todo list and start over.

## Workflow

1. **Initialize**: Run `init` to create todo list from unpushed stashes
2. **Review**: Use `list` and `show` to examine items
3. **Resolve**: Work through items with `resolve` command
4. **Track**: Monitor progress with `status`
5. **Complete**: Continue until all items are resolved or skipped

## Resolution Options

When resolving a stash, you can choose from several approaches:

1. **Apply Interactively**: Use the advanced interactive resolver to handle conflicts
2. **Apply Directly**: Try to apply the stash without conflict resolution
3. **Drop**: Remove the stash from the repository
4. **Save to Branch**: Create a new branch with the stashed changes for later work
5. **Skip**: Leave the stash for later without marking as resolved

## File Locations

- **Todo List**: Stored temporarily in `/tmp/stash_resolution_todo_$$`
- **Backups**: Automatically saved to `~/.stash_resolution_backups/`
- **Logs**: Progress information displayed to terminal

## Integration with Existing Tools

The script integrates with existing orchestration tools:
- Uses the same color output system as other scripts
- Leverages the interactive stash resolver for conflict handling
- Follows the same common library patterns

## Best Practices

1. **Regular Maintenance**: Run the todo manager regularly to keep stashes organized
2. **Backup Important Stashes**: Use the "save to branch" option for important changes
3. **Review Before Dropping**: Always review stashes before dropping them
4. **Track Progress**: Use the status command to monitor resolution progress
5. **Export Before Major Changes**: Save todo lists before making significant changes

This tool helps maintain a clean repository by ensuring all stashes are intentionally resolved rather than forgotten.