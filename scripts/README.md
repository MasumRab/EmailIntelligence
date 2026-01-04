# Scripts Directory - Usage Guide

This directory contains automation and utility scripts for task management, Git operations, and orchestration workflow automation.

## Quick Start

```bash
# View all available scripts
ls -la scripts/

# Get task management help
python scripts/list_tasks.py --help

# Check next task to work on
python scripts/next_task.py

# Search for tasks
python scripts/search_tasks.py "keyword"

# Generate task summary
python scripts/task_summary.py
```

## Script Categories

### 1. Task Management Scripts (Python)

#### Core Task Operations

**List Tasks**
```bash
# List all tasks
python scripts/list_tasks.py

# Filter by status
python scripts/list_tasks.py --status pending

# Filter by priority
python scripts/list_tasks.py --priority high

# Show subtask details
python scripts/list_tasks.py --show-subtasks

# Use different tag
python scripts/list_tasks.py --tag master
```

**Show Task Details**
```bash
# Show task from tasks.json
python scripts/show_task.py 7

# Show task from tasks_invalid.json
python scripts/show_task.py 1 --invalid

# Use different file
python scripts/show_task.py 3 --file tasks/tasks_expanded.json
```

**Find Next Task**
```bash
# Find next available task
python scripts/next_task.py

# Use different tag
python scripts/next_task.py --tag master
```

**Search Tasks**
```bash
# Search for tasks containing "backend"
python scripts/search_tasks.py backend

# Case-sensitive search
python scripts/search_tasks.py Backend --case-sensitive

# Show context around matches
python scripts/search_tasks.py "migration" --show-context

# Search in invalid tasks
python scripts/search_tasks.py "recover" --invalid
```

**Task Summary**
```bash
# Generate comprehensive summary
python scripts/task_summary.py
```

**Compare Task Files**
```bash
# Compare tasks across different JSON files
python scripts/compare_task_files.py
```

**List Invalid Tasks**
```bash
# List all invalid/completed tasks
python scripts/list_invalid_tasks.py

# Filter by status
python scripts/list_invalid_tasks.py --status done
```

#### Task Generation & Enhancement

**Generate Clean Tasks**
```bash
# Generate clean sequential task files (001-020)
python scripts/generate_clean_tasks.py
```

**Enhance Tasks from Archive**
```bash
# Enhance clean tasks with archived content
python scripts/enhance_tasks_from_archive.py
```

**Split Enhanced Plan**
```bash
# Split enhanced plan into individual task files
python scripts/split_enhanced_plan.py

# Dry run to preview
python scripts/split_enhanced_plan.py --dry-run

# Specify input/output
python scripts/split_enhanced_plan.py --input ../new_task_plan/complete_new_task_outline_ENHANCED.md --output-dir ../new_task_plan/task_files
```

**Regenerate Tasks from Plan**
```bash
# Regenerate tasks.json from enhanced plan
python scripts/regenerate_tasks_from_plan.py

# Dry run to preview
python scripts/regenerate_tasks_from_plan.py --dry-run

# Validate only
python scripts/regenerate_tasks_from_plan.py --validate
```

#### Task Recovery

**Find Lost Tasks**
```bash
# Find tasks in git history not in current files
python scripts/find_lost_tasks.py

# Check up to 100 commits
python scripts/find_lost_tasks.py --commits 100

# Save results to file
python scripts/find_lost_tasks.py --output lost_tasks.json

# Verbose output
python scripts/find_lost_tasks.py --verbose
```

### 2. Orchestration & Setup Scripts (Bash)

#### Git Hooks Management

**Disable Hooks**
```bash
# Disable all orchestration hooks for independent development
./scripts/disable-hooks.sh

# Bypass hooks on single operations
DISABLE_ORCHESTRATION_CHECKS=1 git checkout <branch>
DISABLE_ORCHESTRATION_CHECKS=1 git merge <branch>
```

**Re-enable Hooks**
```bash
# Re-enable hooks (if enable-hooks.sh exists)
./scripts/enable-hooks.sh
```

#### Worktree Synchronization

**Sync Setup Files**
```bash
# Synchronize setup files between worktrees
./scripts/sync_setup_worktrees.sh

# Dry run to preview changes
./scripts/sync_setup_worktrees.sh --dry-run

# Verbose output
./scripts/sync_setup_worktrees.sh --verbose

# Show help
./scripts/sync_setup_worktrees.sh --help
```

#### Orchestration Branch Management

**Reverse Sync Orchestration**
```bash
# Pull approved changes from feature branch into orchestration-tools
./scripts/reverse_sync_orchestration.sh feature/fix-launch-bug abc123

# Dry run to preview
./scripts/reverse_sync_orchestration.sh feature/fix-launch-bug abc123 --dry-run
```

**Update Configuration**
```bash
# Update .flake8 in orchestration-tools branch
./scripts/update_flake8_orchestration.sh

# Skip confirmation
./scripts/update_flake8_orchestration.sh --yes
```

## Common Workflows

### Daily Task Management

```bash
# 1. Check next task
python scripts/next_task.py

# 2. View task details
python scripts/show_task.py <task_id>

# 3. Mark task in progress (using task-master CLI)
task-master set-status --id=<task_id> --status=in-progress

# 4. Work on task...

# 5. Mark task complete
task-master set-status --id=<task_id> --status=done

# 6. Generate summary
python scripts/task_summary.py
```

### Task Search and Discovery

```bash
# Search for specific topics
python scripts/search_tasks.py "security" --show-context
python scripts/search_tasks.py "validation" --case-sensitive
python scripts/search_tasks.py "orchestration" --invalid

# List pending high-priority tasks
python scripts/list_tasks.py --status pending --priority high

# Show invalid tasks
python scripts/list_invalid_tasks.py --status done
```

### Task File Management

```bash
# Compare different task files
python scripts/compare_task_files.py

# Find lost tasks in git history
python scripts/find_lost_tasks.py --commits 50 --output lost_tasks.json

# Generate new task structure
python scripts/generate_clean_tasks.py
python scripts/enhance_tasks_from_archive.py

# Regenerate from plan
python scripts/regenerate_tasks_from_plan.py --dry-run
python scripts/regenerate_tasks_from_plan.py
```

### Orchestration Workflow

```bash
# Sync setup files before starting work
./scripts/sync_setup_worktrees.sh --dry-run
./scripts/sync_setup_worktrees.sh

# Disable hooks for independent development
./scripts/disable-hooks.sh

# Work on changes...

# Update orchestration-tools with approved changes
./scripts/reverse_sync_orchestration.sh feature/my-fix abc123 --dry-run
./scripts/reverse_sync_orchestration.sh feature/my-fix abc123

# Update configuration
./scripts/update_flake8_orchestration.sh --yes
```

## Security Considerations

### Path Security
All Python scripts validate file paths before operations:
- Prevents directory traversal attacks
- Detects URL encoding bypass attempts
- Validates against suspicious patterns

### File Size Limits
- Maximum file size: 50MB
- Prevents memory exhaustion
- Validates before loading

### Backup Mechanisms
- Scripts create backups before destructive operations
- Uses timestamp and UUID for unique backup names
- Verifies backup integrity

### Git Operations
- All Git operations are validated
- Branch existence checked before operations
- Commit SHA validation for reverse sync

## Troubleshooting

### Script Not Found
```bash
# Make sure you're in the .taskmaster directory
cd /home/masum/github/PR/.taskmaster

# Use absolute paths
python /home/masum/github/PR/.taskmaster/scripts/list_tasks.py
```

### JSON Parsing Errors
```bash
# Validate JSON files
python -m json.tool tasks/tasks.json
python -m json.tool tasks/tasks_invalid.json

# Scripts handle malformed JSON gracefully
# tasks_invalid.json uses regex parsing as fallback
```

### No Tasks Found
```bash
# Verify file exists
ls tasks/tasks.json

# Check different files
python scripts/list_tasks.py --file tasks/tasks_expanded.json

# Check tag
python scripts/list_tasks.py --tag master
```

### Git Hook Issues
```bash
# Disable hooks temporarily
./scripts/disable-hooks.sh

# Use environment variable
DISABLE_ORCHESTRATION_CHECKS=1 git checkout <branch>

# Re-enable hooks
./scripts/enable-hooks.sh
```

### Permission Errors
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run with bash explicitly
bash scripts/sync_setup_worktrees.sh
```

## File Structure

```
scripts/
├── README.md                          # This file
├── README_TASK_SCRIPTS.md             # Legacy documentation
│
├── Task Management (Python)
│   ├── list_tasks.py                  # List tasks with filtering
│   ├── show_task.py                   # Show task details
│   ├── next_task.py                   # Find next available task
│   ├── search_tasks.py                # Search tasks by keyword
│   ├── task_summary.py                # Generate task summary
│   ├── compare_task_files.py          # Compare task files
│   ├── list_invalid_tasks.py          # List invalid tasks
│   ├── generate_clean_tasks.py        # Generate clean task files
│   ├── enhance_tasks_from_archive.py  # Enhance tasks from archive
│   ├── split_enhanced_plan.py         # Split plan into task files
│   ├── regenerate_tasks_from_plan.py  # Regenerate tasks.json
│   └── find_lost_tasks.py             # Find tasks in git history
│
└── Orchestration (Bash)
    ├── disable-hooks.sh               # Disable Git hooks
    ├── sync_setup_worktrees.sh        # Sync setup files
    ├── reverse_sync_orchestration.sh  # Reverse sync to orchestration-tools
    └── update_flake8_orchestration.sh # Update .flake8 configuration
```

## Dependencies

### Python Scripts
- Python 3.x
- Standard library only (no external dependencies)
- Shared utilities from `task_scripts/taskmaster_common.py`:
  - `SecurityValidator` - Path and file validation
  - `FileValidator` - JSON loading with security checks
  - `TaskValidator` - Task search and validation
  - `TaskComparison` - Task file comparison
  - `TaskSummary` - Task statistics

### Bash Scripts
- Bash 4.x or higher
- Git (for Git operations)
- Standard Unix utilities (cmp, grep, etc.)

## Best Practices

### Task Management
1. Always check task dependencies before starting work
2. Use `--dry-run` for generation scripts to preview changes
3. Generate summaries regularly to track progress
4. Search tasks by keyword to find relevant work
5. Use task filtering to focus on specific priorities

### Orchestration
1. Always use `--dry-run` before sync operations
2. Review changes before applying reverse sync
3. Disable hooks only when necessary for independent work
4. Re-enable hooks after independent development is complete
5. Update orchestration-tools only with approved changes

### Security
1. Never bypass security validation
2. Always validate file paths before operations
3. Use backup mechanisms for destructive operations
4. Review git history before reverse sync
5. Keep scripts updated with security patches

### Development
1. Test scripts with `--dry-run` or `--verbose` flags
2. Read script documentation before use
3. Check script dependencies before execution
4. Validate output files after generation
5. Monitor script execution for errors

## Integration with Agent Documentation

These scripts are referenced in:
- **AGENT.md** - Task Master AI integration guide
- **AGENTS.md** - Multi-agent coordination documentation
- **CLAUDE.md** - Claude Code integration
- **GEMINI.md** - Gemini integration

Agents can use these scripts for:
- Task discovery and management
- Workflow automation
- Orchestration operations
- Git operations
- File management

## Support

### Documentation
- `README_TASK_SCRIPTS.md` - Legacy script documentation
- `../task_scripts/taskmaster_common.py` - Shared utilities documentation
- `../tasks/README.md` - Task system documentation

### Help Commands
```bash
# Python script help
python scripts/list_tasks.py --help
python scripts/search_tasks.py --help
python scripts/find_lost_tasks.py --help

# Bash script help
./scripts/sync_setup_worktrees.sh --help
./scripts/reverse_sync_orchestration.sh
```

### Common Issues
- See "Troubleshooting" section above
- Check script-specific help messages
- Review error messages for guidance
- Validate file paths and permissions

## Version History

- **v1.0** - Initial script collection
- **v1.1** - Added security validation
- **v1.2** - Enhanced task recovery features
- **v1.3** - Added orchestration scripts
- **v1.4** - Improved error handling and documentation

## Contributing

When adding new scripts:
1. Follow existing naming conventions
2. Include comprehensive help messages
3. Implement security validation
4. Add documentation to this README
5. Test thoroughly before deployment

## License

These scripts are part of the EmailIntelligence project. See project LICENSE for details.