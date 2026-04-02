# Task Creation Workflow with Duplicate Prevention

## Overview

This document explains the complete workflow for creating new tasks while systematically checking all existing task documentation to prevent duplicates and identify dependencies.

You have two tools available:

1. **TASK_CREATION_GUIDE.md** - Manual guide with detailed instructions
2. **task-creation-validator.sh** - Automated script for systematic checking

---

## Quick Start: 30 Seconds

```bash
# 1. Run the validator (automatically checks all task files)
./scripts/bash/task-creation-validator.sh "Your Task Title" keyword1 keyword2

# 2. Review results
# If no duplicates → proceed
# If duplicates → clarify scope or enhance existing task

# 3. Create task
task-master add-task --prompt="Your task description"

# 4. Expand with subtasks
task-master expand --id=<new-id> --research
```

---

## Detailed Workflow

### Step 1: Run the Automated Validator

```bash
./scripts/bash/task-creation-validator.sh "Systematic Branch Analysis and Documentation" branch analyze
```

**What this does:**
- ✓ Checks task database (.taskmaster/tasks/tasks.json)
- ✓ Searches all task markdown files
- ✓ Searches backlog/ directory
- ✓ Searches specs/ directory
- ✓ Searches root-level .md files
- ✓ Analyzes task dependencies
- ✓ Shows in-progress tasks
- ✓ Suggests next available task ID
- ✓ Searches for additional keywords

**Output shows:**
```
✓ Task database found
✓ All task files identified
→ Current tasks (with potential matches highlighted)
→ Dependencies between tasks
→ Next available task ID
→ Keyword search results
```

### Step 2: Review Search Results

The validator outputs:

1. **Task Database Results** - Shows all existing tasks
   - Look for any with similar titles
   - Check status (pending, in-progress, done)

2. **Markdown Search Results** - Searches task documentation
   - Shows matching lines from task files

3. **Backlog Results** - Checks backlog directory
   - Some work may be tracked there instead

4. **Dependency Analysis** - Shows task relationships
   - Your new task may depend on others
   - Other tasks may depend on your new task

5. **In-Progress Tasks** - Shows active work
   - Avoid creating tasks already being worked on

6. **Next Task ID** - Suggested ID for new task
   - Use this when creating

### Step 3: Make Decision

```
DUPLICATE FOUND?
├─ YES → Don't create
│   └─ Instead: Enhance existing task or clarify how yours differs
└─ NO → Proceed to creation
```

### Step 4: Create the Task

#### Option A: Use Task Master CLI

```bash
# Interactive task creation
task-master add-task --prompt="\
Task: Systematic Branch Analysis and Documentation
Purpose: Create comprehensive documentation for all repository branches
Scope: Inventory all branches, analyze purposes, document architecture
Dependencies: Task 5 (branch alignment)
Priority: medium"
```

#### Option B: Manual File Addition

```bash
# Edit .taskmaster/tasks/tasks.json
# Add new task object with ID, title, description, etc.

# Then regenerate markdown files
task-master generate
```

### Step 5: Expand with Subtasks

```bash
# Auto-expand based on complexity
task-master expand --id=14 --research

# Manually expand
task-master expand --id=14 --prompt="Provide 5-7 specific subtasks for this work"
```

### Step 6: Commit

```bash
git add .taskmaster/
git commit -m "task: add task-14 Systematic Branch Analysis and Documentation"
```

---

## Files Checked by the Validator

The validator searches these locations:

```
.taskmaster/tasks/tasks.json          Main task database
.taskmaster/tasks/*.md                Individual task markdown files
backlog/                              Backlog items (optional)
specs/                                Specifications (optional)
*.md (root level)                     Root documentation
docs/                                 Documentation directory
agents/                               Agent-related tasks
modules/                              Module tasks
resolution-workspace/                 Resolution tasks
```

---

## Understanding the Validator Output

### Example Output: Task Already Exists

```
→ Searching Task Database
⚠ Task 5: Align Feature Branches with Scientific Branch
   Status: pending
   Priority: high

→ Keyword Search: 'branch'
⚠ Found 425 matches for 'branch'
```

**Decision:** This existing Task 5 is similar. Check if your task:
- Duplicates Task 5? → Don't create
- Is different scope? → Proceed with different title
- Enhances Task 5? → Add subtask to Task 5 instead

### Example Output: No Conflicts Found

```
→ Searching Markdown Files
✓ No matching task markdown files found

→ Searching Backlog Directory
✓ No matches in backlog/

→ Checking In-Progress Tasks
No tasks currently in progress.
```

**Decision:** ✅ SAFE TO CREATE

---

## Manual Process (Without Script)

If you prefer to manually check:

```bash
# 1. Search task database
grep -i "your-keyword" .taskmaster/tasks/tasks.json

# 2. Search task markdown
grep -ri "your-keyword" .taskmaster/tasks/ --include="*.md"

# 3. Search backlog
grep -ri "your-keyword" backlog/ 2>/dev/null

# 4. Search root markdown
grep -ri "your-keyword" . --include="*.md" \
  --exclude-dir=.taskmaster --exclude-dir=.git

# 5. View all tasks
python3 << 'EOF'
import json
with open('.taskmaster/tasks/tasks.json') as f:
    for task in json.load(f)['master']['tasks']:
        print(f"Task {task['id']}: {task['title']}")
EOF
```

---

## Common Scenarios

### Scenario 1: "I Want to Create a Security Task"

```bash
# Run validator
./scripts/bash/task-creation-validator.sh "Security Hardening for API" security auth api

# Expected findings:
# → Task 3: Enhanced Security (RBAC, MFA, Session Management)
# → Task 13: Security Audit and Hardening for Production

# Decision:
# - Task 3 covers authentication/RBAC
# - Task 13 covers production hardening
# - Your task about API security might enhance Task 3 or Task 13
# - OR clarify if it's different (e.g., API token validation only)
```

### Scenario 2: "I Want to Create a Documentation Task"

```bash
# Run validator
./scripts/bash/task-creation-validator.sh "Update API Documentation" documentation api

# Expected findings:
# → Task 6: Comprehensive Documentation Update (subtask)
# → Task 12: Subtasks include API documentation

# Decision:
# - Documentation work may already be in progress
# - Check status of Task 6/12
# - If not yet started → create new task
# - If in progress → collaborate on existing task
```

### Scenario 3: "Completely New Domain"

```bash
# Run validator
./scripts/bash/task-creation-validator.sh "Mobile App Development Setup" mobile app setup

# Expected findings:
# → No matching tasks
# → No dependencies identified

# Decision:
# ✅ SAFE TO CREATE new task
# → Get next available ID from validator
# → Create with `task-master add-task`
```

---

## Checklist Before Creating

- [ ] Ran validator: `./scripts/bash/task-creation-validator.sh "Title"`
- [ ] Reviewed all search results
- [ ] No exact duplicate found
- [ ] Identified dependencies (from validator output)
- [ ] Confirmed priority level
- [ ] Verified next available task ID
- [ ] Prepared task description
- [ ] Understand scope and success criteria
- [ ] Created task with `task-master add-task`
- [ ] Expanded with subtasks: `task-master expand --id=<id>`
- [ ] Committed changes

---

## Integration with Task Master

The validator integrates with Task Master AI:

```bash
# Show all tasks
task-master list

# Show specific task details
task-master show 6

# Check complexity
task-master analyze-complexity

# Create new task
task-master add-task --prompt="..."

# Expand task
task-master expand --id=14 --research

# Mark complete
task-master set-status --id=14 --status=done
```

---

## Tips & Best Practices

### 1. Use Specific Keywords

❌ Bad: "New task"
✅ Good: "Systematic Branch Analysis and Documentation"

### 2. Provide Context Keywords

```bash
./scripts/bash/task-creation-validator.sh "Your Title" keyword1 keyword2 keyword3
```

### 3. Review Dependencies

```
Task Dependencies:
Task 6: depends on [1, 2, 3, 4]
```
Your new task should probably also depend on tasks 1-4 if it follows task 6.

### 4. Check Priority Alignment

Examine existing high-priority tasks to understand what's urgent.

### 5. Document Your Decision

Commit message should explain if similar task found:

```bash
# Good commit message
git commit -m "task: add task-14 Branch Analysis

Found Task 5 (Align Feature Branches) but it's limited to alignment.
Task 14 is new: comprehensive analysis + documentation of ALL branches
across repo. Depends on Task 5 completion."
```

---

## Troubleshooting

### Script Permission Denied

```bash
chmod +x ./scripts/bash/task-creation-validator.sh
```

### Script Not Found

```bash
# Run from repo root
cd /path/to/EmailIntelligenceAuto
./scripts/bash/task-creation-validator.sh "Title"
```

### Task Already Exists, Different Scope

Clarify in commit message how your task differs:

```bash
git commit -m "task: add task-14 Enhanced Task 6 Documentation

This is NOT a duplicate of Task 6.
Task 6: Alignment of feature branches
Task 14: Analysis and documentation of ALL branches (main, scientific, etc.)

Task 14 depends on Task 6 completion but covers different scope."
```

### Too Many Search Results

Use more specific keywords:

```bash
# Instead of:
./scripts/bash/task-creation-validator.sh "New Feature" feature

# Use:
./scripts/bash/task-creation-validator.sh "Email Notification System" email notify webhook
```

---

## References

- **Manual Guide:** TASK_CREATION_GUIDE.md
- **Validator Script:** scripts/bash/task-creation-validator.sh
- **Task Database:** .taskmaster/tasks/tasks.json
- **Task Master CLI:** task-master help

---

## Examples

### Example 1: Creating the Branch Analysis Task

```bash
# Step 1: Validate
./scripts/bash/task-creation-validator.sh "Systematic Branch Analysis and Documentation" branch analyze

# Step 2: Review results (findings: Task 5 similar but different scope)

# Step 3: Create
task-master add-task --prompt="\
Title: Systematic Branch Analysis and Documentation
Purpose: Inventory and analyze all repository branches
Description: Create comprehensive branch documentation including purpose, \
status, architecture decisions, and governance standards.
Dependencies: Task 5
Subtasks: 
1) Inventory all branches (git branch -r)
2) Analyze each branch (history, purpose, unique work)
3) Document findings
4) Create branch governance guide"

# Step 4: Expand
task-master expand --id=14 --research

# Step 5: Commit
git add .taskmaster/
git commit -m "task: add task-14 Systematic Branch Analysis and Documentation

Found Task 5 (Align Feature Branches) but scope is limited to alignment only.
Task 14 expands this with comprehensive analysis and documentation of
ALL branches, creating governance standards and branch inventory."
```

---

## Final Checklist Before Committing Tasks

```bash
# Verify task structure
task-master show 14

# Check it appears in list
task-master list | grep "14:"

# Verify dependencies are correct
grep '"dependencies"' .taskmaster/tasks/tasks.json | grep -A1 "id.*14"

# Commit
git add .taskmaster/ TASK_CREATION_*.md
git commit -m "task: add task-14 [title]"
```

---

_Last Updated: 2025-11-18_
_Created by: Amp Agent_
