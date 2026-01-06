# Scripts and Tools Integration for Isolated Environment

**Purpose:** Define how scripts, CLI tools, and executable utilities integrate into the new_task_plan isolated environment  
**Scope:** All executable code, scripts, and command-line tools  
**Version:** 1.0  
**Created:** January 6, 2026  

---

## Current Script Inventory

### Location 1: Task Scripts (`/home/masum/github/PR/.taskmaster/task_scripts/`)

**Purpose:** Core task execution and management scripts

| Script | Purpose |
|--------|---------|
| `merge_task_manager.py` | Git merge operations with branch tracking |
| `secure_merge_task_manager.py` | Safe merge with conflict detection |
| `test_merge_manager.py` | Test merge operations |
| `add_status.py` | Add status to tasks |
| `consolidate_completed_tasks.py` | Consolidate completed task data |
| `extract_completed_tasks.py` | Extract completed tasks |
| `finalize_task_move.py` | Finalize task movements |
| `fix_relative_deps.py` | Fix relative dependencies |
| `fix_tasks.py` | Fix task issues |
| `move_completed_tasks.py` | Move completed tasks |
| `move_specific_tasks.py` | Move specific task ranges |
| `move_tasks_64_to_69.py` | Move specific task range |
| `quick_start.py` | Quick start helper |
| `remove_duplicates.py` | Remove duplicate entries |

### Location 2: Utility Scripts (`/home/masum/github/PR/.taskmaster/scripts/`)

**Purpose:** Supporting utilities and automation

| Script | Purpose |
|--------|---------|
| `list_tasks.py` | List and filter tasks |
| `show_task.py` | Show task details |
| `next_task.py` | Find next available task |
| `search_tasks.py` | Search tasks by keyword |
| `task_summary.py` | Generate task summary |
| `compare_task_files.py` | Compare task files |
| `list_invalid_tasks.py` | List invalid/completed tasks |
| `find_lost_tasks.py` | Find lost tasks in git |
| `generate_clean_tasks.py` | Generate clean task files |
| `enhance_tasks_from_archive.py` | Enhance tasks from archive |
| `regenerate_tasks_from_plan.py` | Regenerate from plan |
| `compress_progress.py` | Compress progress data |
| `query_findings.py` | Query findings database |
| `markdownlint_check.py` | Lint markdown files |

### Location 3: Shell Scripts (`/home/masum/github/PR/.taskmaster/scripts/`)

| Script | Purpose |
|--------|---------|
| `format_code.sh` | Code formatting |
| `compress_progress.sh` | Compress progress |
| `disable-hooks.sh` | Disable git hooks |
| `sync_setup_worktrees.sh` | Sync worktrees |
| `reverse_sync_orchestration.sh` | Reverse sync to orchestration |

### Location 4: Guidance Code (`/home/masum/github/PR/.taskmaster/guidance/src/`)

| Path | Purpose |
|------|---------|
| `src/main.py` | Factory pattern for branch integration |
| `src/context_control/` | Context control patterns |

---

## Proposed Integration Structure

### Target: new_task_plan/tools/

```
new_task_plan/
├── tools/                                    (NEW: executable utilities)
│   ├── README.md                             Tool usage guide
│   │
│   ├── implementation/                       (Implementation scripts for tasks)
│   │   ├── README.md
│   │   ├── commit_history_analyzer.py        # Task 002-1 implementation
│   │   ├── codebase_structure_analyzer.py    # Task 002-2 implementation
│   │   ├── diff_distance_calculator.py       # Task 002-3 implementation
│   │   ├── branch_clusterer.py               # Task 002-4 implementation
│   │   ├── integration_target_assigner.py    # Task 002-5 implementation
│   │   └── pipeline_orchestrator.py          # Task 002-6 implementation
│   │
│   ├── management/                           (Task management scripts)
│   │   ├── list_tasks.py                     (from scripts/)
│   │   ├── show_task.py                      (from scripts/)
│   │   ├── next_task.py                      (from scripts/)
│   │   ├── search_tasks.py                   (from scripts/)
│   │   └── task_summary.py                   (from scripts/)
│   │
│   ├── utilities/                            (Utility scripts)
│   │   ├── format_code.sh
│   │   ├── disable-hooks.sh
│   │   └── compress_progress.sh
│   │
│   ├── git/                                  (Git operations)
│   │   ├── sync_setup_worktrees.sh
│   │   ├── reverse_sync_orchestration.sh
│   │   └── update_flake8_orchestration.sh
│   │
│   └── validation/                           (Validation scripts)
│       ├── markdownlint_check.py
│       ├── query_findings.py
│       └── validate_integration.sh
│
├── task_files/                               (Task definitions)
│   └── subtasks/
│       └── task-002-*.md                     (Reference to implementation in tools/)
│
└── guidance/                                 (Reference implementations)
    └── src/
        └── main.py                           (Factory pattern reference)
```

---

## Script Integration Rules

### Rule 1: Task Implementation Scripts

**Location:** `tools/implementation/`

**Pattern:** Each task that produces code should have an implementation script

| Task | Script | Purpose |
|------|--------|---------|
| 002-1 | `commit_history_analyzer.py` | Extract commit metrics |
| 002-2 | `codebase_structure_analyzer.py` | Analyze structure similarity |
| 002-3 | `diff_distance_calculator.py` | Calculate diff metrics |
| 002-4 | `branch_clusterer.py` | Cluster branches |
| 002-5 | `integration_target_assigner.py` | Assign integration targets |
| 002-6 | `pipeline_orchestrator.py` | Orchestrate full pipeline |

**Template:**
```python
#!/usr/bin/env python3
"""
[Task ID]: [Title]
[Purpose]

Usage:
    python tools/implementation/[script].py --repo PATH --branch BRANCH
    python tools/implementation/[script].py --help
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class [AnalyzerName]:
    """Description of analyzer."""
    
    def __init__(self, repo_path: str, main_branch: str = "main"):
        self.repo_path = repo_path
        self.main_branch = main_branch
    
    def analyze(self, branch_name: str) -> dict:
        """Main analysis method."""
        pass

def main():
    parser = argparse.ArgumentParser(description="[Description]")
    parser.add_argument("--repo", required=True, help="Repository path")
    parser.add_argument("--branch", required=True, help="Branch name")
    parser.add_argument("--output", help="Output file (JSON)")
    args = parser.parse_args()
    
    analyzer = [AnalyzerName](args.repo)
    result = analyzer.analyze(args.branch)
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print(result)

if __name__ == "__main__":
    main()
```

---

### Rule 2: Task Management Scripts

**Location:** `tools/management/`

These scripts should work with `task_files/subtasks/` instead of `tasks.json`.

**Update pattern:**
```python
# Old pattern (tasks.json based)
python scripts/list_tasks.py

# New pattern (task file based)
python tools/management/list_tasks.py --dir task_files/subtasks
```

**Modified scripts should:**
1. Accept `--dir` parameter for task file location
2. Parse markdown task files instead of JSON
3. Support filtering by task ID pattern (e.g., `task-002-*`)

---

### Rule 3: Git Operations

**Location:** `tools/git/`

Shell scripts for Git operations. Should be executable:

```bash
chmod +x tools/git/*.sh
```

**Usage:**
```bash
./tools/git/sync_setup_worktrees.sh --dry-run
./tools/git/reverse_sync_orchestration.sh feature/fix abc123
```

---

### Rule 4: Validation Scripts

**Location:** `tools/validation/`

Scripts for validating the isolated environment:

```bash
# Validate directory structure
python tools/validation/validate_structure.py

# Check all task files exist
python tools/validation/check_task_files.py

# Validate cross-references
python tools/validation/check_links.py
```

---

## Pipeline Integration

### Execution Flow

```
1. Developer picks task (e.g., Task 002-1)
   ↓
2. Reads task-002-1.md for specifications
   ↓
3. Implements using tools/implementation/commit_history_analyzer.py
   ↓
4. Tests with python tools/implementation/commit_history_analyzer.py --repo . --branch feature/test
   ↓
5. Validates output against task-002-1.md success criteria
   ↓
6. Updates progress in progress/COMPLETION_STATUS.md
```

### Batch Pipeline Execution

```bash
# Run full clustering pipeline
python tools/implementation/pipeline_orchestrator.py --repo . --branches "feature/*"

# Run specific stages
python tools/implementation/pipeline_orchestrator.py --stage 1  # Stage One only
python tools/implementation/pipeline_orchestrator.py --stage 2  # Stage Two only
```

---

## Migration Plan for Scripts

### Phase 1: Create tools/ Directory Structure

```bash
cd /home/masum/github/PR/.taskmaster/new_task_plan/

# Create directory structure
mkdir -p tools/implementation
mkdir -p tools/management
mkdir -p tools/utilities
mkdir -p tools/git
mkdir -p tools/validation

# Copy existing scripts
cp ../scripts/list_tasks.py tools/management/
cp ../scripts/show_task.py tools/management/
cp ../scripts/next_task.py tools/management/
cp ../scripts/search_tasks.py tools/management/
cp ../scripts/task_summary.py tools/management/

cp ../scripts/*.sh tools/utilities/
cp ../scripts/sync_setup_worktrees.sh tools/git/
cp ../scripts/reverse_sync_orchestration.sh tools/git/
```

### Phase 2: Update Script Paths

**For each script in tools/management/:**

1. Add `--dir` parameter for task file location
2. Update file path resolution
3. Test with task file pattern

**Example update to list_tasks.py:**
```python
# Add after argument parsing
parser.add_argument("--dir", default="task_files/subtasks",
                   help="Directory containing task files")

# Update file discovery
task_dir = Path(args.dir)
task_files = list(task_dir.glob("task-*.md"))
```

### Phase 3: Create Implementation Scripts

For each Task 002 subtask, create the implementation script template:

```bash
# Create script template
cat > tools/implementation/commit_history_analyzer.py << 'EOF'
#!/usr/bin/env python3
"""
Task 002-1: CommitHistoryAnalyzer Implementation

See: task_files/subtasks/task-002-1.md for specifications
"""
EOF
```

### Phase 4: Create Validation Scripts

```bash
# Validate structure
cat > tools/validation/validate_structure.py << 'EOF'
#!/usr/bin/env python3
"""Validate isolated environment structure."""
import sys
from pathlib import Path

REQUIRED_DIRS = [
    "task_files/main_tasks",
    "task_files/subtasks",
    "guidance",
    "execution",
    "progress",
    "reference",
    "archive",
    "tools/implementation",
    "tools/management",
]

def main():
    root = Path(__file__).parent.parent
    missing = []
    for dir in REQUIRED_DIRS:
        if not (root / dir).exists():
            missing.append(dir)
    
    if missing:
        print(f"Missing directories: {', '.join(missing)}")
        sys.exit(1)
    else:
        print("Structure validated ✓")

if __name__ == "__main__":
    main()
EOF
```

---

## Script Reference by Task

### Task 002 (Clustering System) Implementation Scripts

| Subtask | Script | Entry Point |
|---------|--------|-------------|
| 002-1 | `commit_history_analyzer.py` | `python tools/implementation/commit_history_analyzer.py --repo . --branch feature/auth` |
| 002-2 | `codebase_structure_analyzer.py` | `python tools/implementation/codebase_structure_analyzer.py --repo . --branch feature/auth` |
| 002-3 | `diff_distance_calculator.py` | `python tools/implementation/diff_distance_calculator.py --repo . --branch feature/auth` |
| 002-4 | `branch_clusterer.py` | `python tools/implementation/branch_clusterer.py --input analysis.json` |
| 002-5 | `integration_target_assigner.py` | `python tools/implementation/integration_target_assigner.py --input clusters.json` |
| 002-6 | `pipeline_orchestrator.py` | `python tools/implementation/pipeline_orchestrator.py --repo . --branches "feature/*"` |

### Task Management Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `list_tasks.py` | List available tasks | `python tools/management/list_tasks.py --dir task_files/subtasks` |
| `show_task.py` | Show task details | `python tools/management/show_task.py 002-1` |
| `next_task.py` | Find next task | `python tools/management/next_task.py` |
| `search_tasks.py` | Search tasks | `python tools/management/search_tasks.py "analyzer"` |

---

## Environment Variables

Scripts should support these environment variables:

```bash
# Repository configuration
export TASKMASTER_REPO_PATH="/path/to/repo"
export TASKMASTER_MAIN_BRANCH="main"

# Output configuration
export TASKMASTER_OUTPUT_DIR="output"
export TASKMASTER_CACHE_DIR=".taskmaster/cache"

# Task file location
export TASKMASTER_TASK_DIR="task_files/subtasks"
```

---

## Validation Commands

### Quick Validation

```bash
# Check tools directory exists
ls -la tools/

# Check implementation scripts exist
ls tools/implementation/

# Check management scripts exist
ls tools/management/

# Run structure validation
python tools/validation/validate_structure.py
```

### Full Validation

```bash
# Run all validation scripts
python tools/validation/validate_structure.py
python tools/validation/check_task_files.py
python tools/validation/check_links.py

# Test task management scripts
python tools/management/list_tasks.py --dir task_files/subtasks | head -20
python tools/management/next_task.py

# Test implementation scripts (if implemented)
python tools/implementation/commit_history_analyzer.py --help
```

---

## Rollback Plan

If scripts need to be rolled back:

```bash
# Remove tools directory
rm -rf tools/

# Scripts are not deleted, just copied
# Original scripts remain in:
# - /home/masum/github/PR/.taskmaster/scripts/
# - /home/masum/github/PR/.taskmaster/task_scripts/
```

---

## Success Criteria

- [ ] `tools/` directory created with all subdirectories
- [ ] All management scripts work with `--dir` parameter
- [ ] Implementation scripts exist for Tasks 002-1 through 002-6
- [ ] Validation scripts run without errors
- [ ] Documentation (README.md) explains usage
- [ ] Scripts are executable (`chmod +x` where applicable)

---

**Document Version:** 1.0  
**Status:** Ready for Implementation  
**Next Action:** Execute Phase 1 - Create tools/ directory structure
