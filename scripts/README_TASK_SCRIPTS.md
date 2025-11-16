# Task Master Backup Scripts

These scripts provide backup functionality for analyzing and managing tasks when the `task-master` CLI tool is not available or not working.

## Available Scripts

### 1. `list_tasks.py`
List all tasks from `tasks.json` with filtering options.

**Usage:**
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

**Options:**
- `--status STATUS` - Filter by status (pending, in-progress, done, etc.)
- `--priority PRIORITY` - Filter by priority (high, medium, low)
- `--tag TAG` - Task tag (default: master)
- `--show-subtasks` - Show detailed subtask information
- `--file PATH` - Path to tasks.json file (default: tasks/tasks.json)

---

### 2. `list_invalid_tasks.py`
List tasks from `tasks_invalid.json` (completed or invalidated tasks).

**Usage:**
```bash
# List all invalid tasks
python scripts/list_invalid_tasks.py

# Filter by status
python scripts/list_invalid_tasks.py --status done
```

**Options:**
- `--status STATUS` - Filter by status
- `--file PATH` - Path to tasks_invalid.json (default: tasks/tasks_invalid.json)

**Note:** This script handles malformed JSON in `tasks_invalid.json` using regex parsing as a fallback.

---

### 3. `show_task.py`
Show detailed information about a specific task.

**Usage:**
```bash
# Show task from tasks.json
python scripts/show_task.py 2

# Show task from tasks_invalid.json
python scripts/show_task.py 1 --invalid

# Use different file
python scripts/show_task.py 3 --file tasks/tasks_expanded.json
```

**Options:**
- `task_id` - Task ID to show (required)
- `--file PATH` - Path to tasks JSON file (default: tasks/tasks.json)
- `--tag TAG` - Task tag (default: master)
- `--invalid` - Search in tasks_invalid.json instead

---

### 4. `task_summary.py`
Generate a comprehensive summary of all tasks across all JSON files.

**Usage:**
```bash
python scripts/task_summary.py
```

**Output includes:**
- Task counts by file
- Status breakdown
- Priority breakdown
- Total subtask counts
- Task ID ranges
- Complete task list with metadata

---

### 5. `compare_task_files.py`
Compare tasks across different JSON files to identify differences.

**Usage:**
```bash
python scripts/compare_task_files.py
```

**Output shows:**
- Differences between `tasks.json` and `tasks_expanded.json`
- Overlap between `tasks.json` and `tasks_invalid.json`
- Tasks unique to each file
- Summary statistics

---

### 6. `next_task.py`
Find the next available task to work on (similar to `task-master next`).

**Usage:**
```bash
# Find next task
python scripts/next_task.py

# Use different tag
python scripts/next_task.py --tag master
```

**Selection criteria:**
1. Status is 'pending'
2. No unmet dependencies (dependencies exist in task list)
3. Priority order (high > medium > low)
4. Task ID (lower IDs preferred when priority is equal)

**Options:**
- `--tag TAG` - Task tag (default: master)
- `--file PATH` - Path to tasks.json file (default: tasks/tasks.json)

---

### 7. `search_tasks.py`
Search tasks by keyword in title, description, or details.

**Usage:**
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

**Options:**
- `keyword` - Keyword to search for (required)
- `--file PATH` - Path to tasks JSON file (default: tasks/tasks.json)
- `--tag TAG` - Task tag (default: master)
- `--case-sensitive` - Case-sensitive search
- `--show-context` - Show context around matches
- `--invalid` - Search in tasks_invalid.json instead

---

## Quick Reference

```bash
# Quick task overview
python scripts/task_summary.py

# List all pending high-priority tasks
python scripts/list_tasks.py --status pending --priority high

# Find next task to work on
python scripts/next_task.py

# Show details of a specific task
python scripts/show_task.py 2

# Check what's in invalid tasks
python scripts/list_invalid_tasks.py

# Compare all task files
python scripts/compare_task_files.py

# Search for tasks
python scripts/search_tasks.py "security" --show-context
```

## File Structure

These scripts expect the following structure:
```
.taskmaster/
├── tasks/
│   ├── tasks.json
│   ├── tasks_expanded.json
│   ├── tasks_new.json
│   └── tasks_invalid.json
└── scripts/
    ├── list_tasks.py
    ├── list_invalid_tasks.py
    ├── show_task.py
    ├── task_summary.py
    ├── compare_task_files.py
    ├── next_task.py
    └── search_tasks.py
```

## Notes

- All scripts are standalone Python 3 scripts with no external dependencies beyond the standard library
- Scripts handle malformed JSON gracefully (especially `tasks_invalid.json`)
- Paths are resolved relative to the `.taskmaster` directory
- Scripts work even if the `task-master` CLI is not installed or not working

## Troubleshooting

**Script not found:**
- Make sure you're running from the `.taskmaster` directory or adjust paths
- Use absolute paths if needed: `python /path/to/.taskmaster/scripts/list_tasks.py`

**JSON parsing errors:**
- `tasks_invalid.json` may be malformed - scripts use regex fallback parsing
- Other JSON files should be valid - check with `python -m json.tool tasks/tasks.json`

**No tasks found:**
- Verify the file exists: `ls tasks/tasks.json`
- Check the tag: `python scripts/list_tasks.py --tag master`
- Try different files: `python scripts/list_tasks.py --file tasks/tasks_expanded.json`
