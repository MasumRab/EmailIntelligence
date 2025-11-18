# Task Creation Guide: Duplicate Prevention & Dependency Analysis

## Overview

Before creating a new task, you **must** search the repository for existing tasks and documentation that might already address the same problem or have relevant dependencies. This guide provides a systematic approach to prevent duplicate effort, identify related work, and ensure proper task hierarchy.

---

## Why Check Existing Tasks?

1. **Avoid Duplicate Effort** - Don't create Task 14 if Task 6 already covers it
2. **Identify Dependencies** - Understand task ordering and blockers
3. **Reuse Documentation** - Reference existing implementation patterns
4. **Maintain Coherence** - Ensure new tasks fit project structure
5. **Leverage Completed Work** - Build on foundation tasks already done

---

## Task Files to Check

### Primary Task Database
```
.taskmaster/tasks/tasks.json          # Master task database (JSON)
.taskmaster/tasks/*.md               # Individual task markdown files (auto-generated)
```

### Secondary Task Sources
```
backlog/                             # Backlog markdown files (if exists)
*.md files matching task patterns    # Ad-hoc task documentation
.taskmaster/docs/                    # Task documentation
specs/                               # Specification documents (may contain planned tasks)
```

---

## Pre-Creation Checklist

Before writing a new task, complete this checklist:

- [ ] **Task Title Search** - Search all files for your task title keywords
- [ ] **Problem Domain Search** - Search for the problem area your task addresses
- [ ] **Technology Search** - Search for specific tech/tools mentioned in your task
- [ ] **Author/Team Search** - Find related tasks by same team/author
- [ ] **Dependency Search** - Identify tasks this one depends on
- [ ] **Status Review** - Check if related tasks are already in progress
- [ ] **Documentation Review** - Look for existing guides on this topic

---

## Step-by-Step Search Instructions

### Step 1: Search Task JSON for Keywords

```bash
# Search .taskmaster/tasks/tasks.json for your task concept
grep -i "keyword" .taskmaster/tasks/tasks.json | head -20

# Example: Looking for all branch-related tasks
grep -i "branch" .taskmaster/tasks/tasks.json

# Example: Looking for security-related tasks
grep -i "security\|hardening\|auth" .taskmaster/tasks/tasks.json
```

### Step 2: Search Markdown Files in All Directories

```bash
# Search all markdown files for keywords (recursive)
grep -r "your-keyword" --include="*.md" . | grep -v node_modules | grep -v venv

# Example: Search for all documentation about branches
grep -r "branch" --include="*.md" . | grep -v node_modules

# Example: Search for existing analysis tasks
grep -r "analyze" --include="*.md" . | head -20
```

### Step 3: Check Task Database Structure

```bash
# View all task IDs and titles (pretty-printed)
python3 << 'EOF'
import json
with open('.taskmaster/tasks/tasks.json', 'r') as f:
    data = json.load(f)
    for task in data['master']['tasks']:
        print(f"Task {task['id']}: {task['title']}")
        if task.get('subtasks'):
            for st in task['subtasks']:
                print(f"  └─ {st['id']}: {st['title']}")
EOF
```

### Step 4: Search Backlog and Specs Directories

```bash
# Search backlog for related work
find backlog -type f -name "*.md" -exec grep -l "your-keyword" {} \; 2>/dev/null

# Search specs for related requirements
find specs -type f -name "*.md" -exec grep -l "your-keyword" {} \; 2>/dev/null

# Search root-level task documentation
grep -r "your-keyword" --include="*.md" . --max-depth=1
```

### Step 5: Check for Similar Task Titles

```bash
# Get all unique task titles to spot similar names
python3 << 'EOF'
import json
with open('.taskmaster/tasks/tasks.json', 'r') as f:
    data = json.load(f)
    titles = [t['title'] for t in data['master']['tasks']]
    for title in sorted(titles):
        print(f"- {title}")
EOF
```

---

## Detailed Search Examples

### Example 1: Looking for "Branch Alignment" Tasks

```bash
# Search task database
grep -i "align\|branch" .taskmaster/tasks/tasks.json | grep -i "align"

# Search markdown files
grep -r "align.*branch\|branch.*align" --include="*.md" .

# Result: Finds Task 5 "Align Feature Branches with Scientific Branch"
#         and Task 9 "Align import-error-corrections Branch with Main Branch"
# Action: Don't create a duplicate branch alignment task
```

### Example 2: Looking for "Documentation" Tasks

```bash
# Search for doc-related tasks
grep -i "documentation\|document\|docs\|readme" .taskmaster/tasks/tasks.json

# Search for doc files
grep -r "document" --include="*.md" .taskmaster/tasks/

# Result: May find multiple doc update tasks
# Action: Check if your doc task is different in scope/purpose
```

### Example 3: Looking for "Analysis" Tasks

```bash
# Search for analysis-related work
grep -i "analyz\|analysis\|report\|audit" .taskmaster/tasks/tasks.json

# Search markdown for analysis docs
grep -r "complex.*analyz\|analyz.*complexity" --include="*.md" .

# Result: Finds Task 6 complexity analysis, Task 7 validation framework
# Action: Understand existing analysis structure before creating new analysis task
```

---

## Dependency Analysis

### View Task Dependencies

```bash
# Extract all dependencies from tasks.json
python3 << 'EOF'
import json
with open('.taskmaster/tasks/tasks.json', 'r') as f:
    data = json.load(f)
    print("Task Dependencies:")
    for task in data['master']['tasks']:
        deps = task.get('dependencies', [])
        if deps:
            print(f"Task {task['id']}: depends on {deps}")
EOF
```

### Find Tasks That Depend on Your New Task's Prerequisites

```bash
# Example: If your task depends on Task 7, find what else depends on 7
python3 << 'EOF'
import json
with open('.taskmaster/tasks/tasks.json', 'r') as f:
    data = json.load(f)
    task_num = 7  # Replace with your prerequisite task
    dependents = [t['id'] for t in data['master']['tasks'] 
                  if task_num in t.get('dependencies', [])]
    print(f"Tasks depending on Task {task_num}: {dependents}")
EOF
```

---

## Search Command Reference

### Quick Search Commands

```bash
# Find all files mentioning your concept
grep -r "concept" --include="*.md" --include="*.json" . 2>/dev/null

# Case-insensitive search
grep -ri "concept" --include="*.md" . 2>/dev/null

# Count matches
grep -ri "concept" --include="*.md" . 2>/dev/null | wc -l

# Show filenames only
grep -ril "concept" --include="*.md" . 2>/dev/null

# Show line numbers
grep -rn "concept" --include="*.md" . 2>/dev/null
```

### Advanced Search Patterns

```bash
# Search for task titles with specific words
grep -E "\"title\".*\"(branch|align|merge)" .taskmaster/tasks/tasks.json

# Find tasks by priority
grep -i "high\|medium\|low" .taskmaster/tasks/tasks.json | grep -i "priority"

# Find tasks in specific status
grep -i "pending\|in-progress\|done" .taskmaster/tasks/tasks.json

# Find tasks with descriptions containing multiple keywords
grep -iE "(security|hardening|password|auth|encryption)" .taskmaster/tasks/tasks.json
```

---

## Decision Tree: Should You Create This Task?

```
┌─ Does a task with similar title exist?
│  ├─ YES → Are they functionally identical?
│  │        ├─ YES → Don't create (duplicate)
│  │        └─ NO → Proceed with creation (different scope)
│  └─ NO → Continue...
│
├─ Is this work already in progress (status != pending)?
│  ├─ YES → Don't create (already assigned)
│  └─ NO → Continue...
│
├─ Does related documentation already exist?
│  ├─ YES → Does it already solve your problem?
│  │        ├─ YES → Don't create (documentation sufficient)
│  │        └─ NO → Enhance existing doc or create task
│  └─ NO → Continue...
│
├─ Will this task be blocked by incomplete prerequisites?
│  ├─ YES → Document dependencies clearly
│  └─ NO → Continue...
│
└─ Are you adding unique value?
   ├─ YES → CREATE THE TASK ✓
   └─ NO → Consider alternative (skip/enhance existing)
```

---

## Task Creation Workflow

Once you've cleared the checks above:

### 1. Prepare Your Task Definition

Create a markdown file with your task details:

```markdown
# [Task Title]

## Purpose
[What problem does this solve?]

## Scope
[What's included and excluded?]

## Dependencies
[Which tasks must be complete first?]

## Success Criteria
[How do we know this is done?]

## Subtasks
- [ ] Subtask 1
- [ ] Subtask 2
```

### 2. Run Pre-Creation Verification

```bash
# Before creating the task, run this verification script
cat > /tmp/verify_task.sh << 'EOF'
#!/bin/bash

TASK_TITLE="$1"
echo "Verifying task: $TASK_TITLE"
echo "================================"

echo -e "\n1. Searching task database..."
grep -i "$(echo $TASK_TITLE | head -c 5)" .taskmaster/tasks/tasks.json

echo -e "\n2. Searching markdown files..."
grep -ri "$(echo $TASK_TITLE | head -c 5)" --include="*.md" . | head -5

echo -e "\n3. Searching backlog..."
grep -ri "$(echo $TASK_TITLE | head -c 5)" backlog/ 2>/dev/null | head -5

echo -e "\n4. Unique task IDs currently in use:"
python3 -c "
import json
with open('.taskmaster/tasks/tasks.json') as f:
    data = json.load(f)
    ids = [t['id'] for t in data['master']['tasks']]
    print(f'Used IDs: {sorted(ids)}')
    print(f'Next available ID: {max(ids) + 1}')
"
EOF

chmod +x /tmp/verify_task.sh
/tmp/verify_task.sh "Your Task Title"
```

### 3. Use Task Master to Create

```bash
# Add new task via task-master CLI
task-master add-task --prompt="Task title and description" --research

# OR parse from PRD
task-master parse-prd new-task.md

# OR manually add to tasks.json and run generate
task-master generate
```

---

## Common Issues & Resolution

### Issue: "Task Already Exists"

```bash
# Verify it's truly a duplicate
grep -n "exact-title-here" .taskmaster/tasks/tasks.json

# Compare scope/description with existing task
task-master show <id>

# Decision: Enhance existing task OR create new task with different scope
```

### Issue: "Missing Dependencies"

```bash
# Check what prerequisites your task needs
grep -i "depends\|prerequisite\|requires" your-task-doc.md

# Verify those tasks exist
python3 << 'EOF'
import json
with open('.taskmaster/tasks/tasks.json') as f:
    data = json.load(f)
    ids = [t['id'] for t in data['master']['tasks']]
    print(f"Available task IDs: {ids}")
    # Now check your dependencies against this list
EOF

# Update dependencies field accordingly
```

### Issue: "Unclear Task Scope"

```bash
# Search for similar task scope statements
grep -ri "scope\|includes\|excludes" .taskmaster/tasks/

# Use complexity analysis to validate scope
task-master analyze-complexity --research

# Expand task definition based on analysis
```

---

## Checklist for Task Creation

Before committing a new task:

- [ ] Searched task database for duplicates
- [ ] Searched markdown files in repo root
- [ ] Searched backlog/ directory
- [ ] Checked if related work is in progress
- [ ] Identified all dependencies
- [ ] Verified this adds unique value
- [ ] Documented clear success criteria
- [ ] Created subtasks with specific descriptions
- [ ] Set appropriate priority
- [ ] Assigned correct dependencies
- [ ] Run `task-master generate` to finalize
- [ ] Commit with message: `task: add task-N <title>`

---

## Example: Creating the "Systematic Branch Analysis Task"

**Scenario:** You want to create a task for systematic branch analysis and documentation.

### Search Phase

```bash
# 1. Search for existing branch analysis tasks
grep -i "branch.*analyz\|analyz.*branch" .taskmaster/tasks/tasks.json
# → Finds Task 5 (alignment only, not analysis)

# 2. Search for documentation tasks
grep -i "document" .taskmaster/tasks/tasks.json
# → Finds Task 20 (comprehensive documentation update in Task 6)

# 3. Search for analysis/audit tasks
grep -i "audit\|analyz\|review" .taskmaster/tasks/tasks.json
# → Finds Task 13 (Security Audit)

# 4. Check if this is truly new
# → Conclusion: Branch analysis + documentation is NEW, not covered by existing tasks
```

### Decision

✅ **PROCEED** - This is a unique task that combines branch analysis with systematic documentation across all branches. No duplicates found.

### Creation Command

```bash
task-master add-task --prompt="\
Create a new task: 'Systematic Branch Analysis & Documentation'\
Purpose: Analyze all repository branches (main, scientific, feature/*, orchestration-tools) \
and create comprehensive branch-specific documentation including purpose, status, \
architecture decisions, and governance standards.\
Dependencies: Task 5 (branch alignment)\
Subtasks: 1) Inventory branches 2) Analyze each 3) Document 4) Create governance guide"
```

---

## References

- Task Master CLI: `.taskmaster/tasks/tasks.json`
- Existing Tasks: Run `task-master list`
- Task Details: Run `task-master show <id>`
- Task Complexity: Run `task-master analyze-complexity`

---

## Notes

- Always commit your search/analysis before task creation
- Document why a potentially similar task is different (in commit message)
- Use subtasks to break large tasks into manageable chunks
- Run `task-master expand` to auto-generate subtasks based on complexity
