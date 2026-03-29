# Task Creation Quick Reference

## 3-Step Process

### 1️⃣ Validate (Check for Duplicates)
```bash
./scripts/bash/task-creation-validator.sh "Your Task Title" keyword1 keyword2
```

### 2️⃣ Create (If No Duplicates)
```bash
task-master add-task --prompt="Your task description"
task-master expand --id=<new-id> --research
```

### 3️⃣ Commit
```bash
git add .taskmaster/
git commit -m "task: add task-<id> Your Task Title"
```

---

## What the Validator Checks

| File/Location | What it Searches | When to Care |
|---|---|---|
| `.taskmaster/tasks/tasks.json` | All task metadata | Always - main database |
| `.taskmaster/tasks/*.md` | Task documentation | Check for existing docs |
| `backlog/` | Backlog items | May duplicate backlog work |
| `specs/` | Specifications | May have planned tasks |
| Root `.md` files | Project documentation | Check for existing approaches |
| Task dependencies | Task relationships | See what must be done first |

---

## Decision Tree

```
Run validator
    ↓
Found exact title match?
├─ YES → Don't create (duplicate)
└─ NO → Continue
    ↓
Found similar work in progress?
├─ YES → Enhance existing task
└─ NO → Continue
    ↓
Found different approach documented?
├─ YES → Clarify scope difference
└─ NO → Continue
    ↓
✅ SAFE TO CREATE
```

---

## Validator Output Summary

| Output | Meaning | Action |
|--------|---------|--------|
| `✓ Task database found` | System ready | Continue |
| `⚠ Found X matches for 'keyword'` | Similar work exists | Review carefully |
| `✓ No matches in backlog/` | Not in backlog | Good sign |
| `Task X: depends on [Y, Z]` | Dependency info | Note prerequisites |
| `Next available ID: 14` | Use this ID | When creating |

---

## Search Commands (Manual)

```bash
# Quick: Find all tasks with keyword
grep -i "keyword" .taskmaster/tasks/tasks.json

# Deep: Search all markdown files
grep -ri "keyword" --include="*.md" .

# List all tasks
task-master list

# Show task details
task-master show <id>

# Check next available ID
python3 -c "import json; d=json.load(open('.taskmaster/tasks/tasks.json')); print(f'Next ID: {max([t[\"id\"] for t in d[\"master\"][\"tasks\"]]) + 1}')"
```

---

## Common Tasks

### Create Security Task
```bash
./scripts/bash/task-creation-validator.sh "Security Hardening" security auth hardening
# Check: Task 3, Task 13 may be related
```

### Create Documentation Task
```bash
./scripts/bash/task-creation-validator.sh "Update Documentation" documentation api
# Check: Task 6 has documentation subtask
```

### Create Branch-Related Task
```bash
./scripts/bash/task-creation-validator.sh "Branch Analysis" branch analyze document
# Check: Task 5 (alignment), Task 8 (setup)
```

### Create Infrastructure Task
```bash
./scripts/bash/task-creation-validator.sh "Production Infrastructure" deployment ci-cd
# Check: Task 12 (deployment setup)
```

---

## Task Structure

```json
{
  "id": 14,
  "title": "Task Title",
  "description": "Short description",
  "details": "Long detailed description",
  "status": "pending",
  "priority": "high|medium|low",
  "dependencies": [1, 2, 3],
  "subtasks": [
    {
      "id": 1,
      "title": "Subtask title",
      "description": "What to do",
      "dependencies": [],
      "status": "pending"
    }
  ]
}
```

---

## Task Master Commands

```bash
# List all tasks
task-master list

# View task details
task-master show <id>

# Create new task
task-master add-task --prompt="description"

# Expand task into subtasks
task-master expand --id=<id> --research

# Analyze complexity
task-master analyze-complexity --research

# Mark task complete
task-master set-status --id=<id> --status=done

# Update task info
task-master update-task --id=<id> --prompt="changes"

# Generate markdown files
task-master generate
```

---

## Files to Read

| File | Purpose |
|------|---------|
| `TASK_CREATION_GUIDE.md` | Full step-by-step guide (detailed) |
| `TASK_CREATION_WORKFLOW.md` | Complete workflow with examples |
| `TASK_CREATION_QUICK_REF.md` | This file - quick lookup |
| `scripts/bash/task-creation-validator.sh` | Automated checker script |

---

## Example: Create "Branch Analysis Task"

```bash
# 1. Validate
./scripts/bash/task-creation-validator.sh "Systematic Branch Analysis and Documentation" branch analyze

# Output: No duplicates found ✅

# 2. Create
task-master add-task --prompt="\
Systematic Branch Analysis and Documentation\

Purpose: Analyze all repository branches (main, scientific, feature/*, etc.) \
and create comprehensive documentation.\

Scope:\
- Inventory all branches\
- Analyze purpose of each\
- Document architecture decisions\
- Create governance standards\

Priority: medium\
Dependencies: Task 5"

# 3. Expand (let AI suggest subtasks)
task-master expand --id=14 --research

# 4. Check
task-master show 14

# 5. Commit
git add .taskmaster/
git commit -m "task: add task-14 Systematic Branch Analysis and Documentation"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Permission denied` on script | `chmod +x scripts/bash/task-creation-validator.sh` |
| Script not found | Run from repo root: `cd /repo && ./scripts/bash/task-creation-validator.sh ...` |
| Task Master not found | Install: `npm install -g task-master-ai` |
| Too many search results | Use more specific keywords |
| Duplicate found | Review scope, enhance existing or clarify difference |
| Task ID missing | Use next available from validator output |

---

## Quick Checklist

```
Before Creating Task:
☐ Run validator script
☐ Review all search results
☐ Check for duplicates
☐ Identify dependencies
☐ Verify next task ID
☐ Prepare description
☐ Create with task-master
☐ Expand with subtasks
☐ Commit changes

Before Committing:
☐ task-master show <id> (verify structure)
☐ .taskmaster/tasks/tasks.json contains new task
☐ git status (verify changes)
☐ git add .taskmaster/
☐ git commit -m "task: add task-<id> ..."
```

---

## Links

- Full Guide: [TASK_CREATION_GUIDE.md](./TASK_CREATION_GUIDE.md)
- Workflow: [TASK_CREATION_WORKFLOW.md](./TASK_CREATION_WORKFLOW.md)
- Validator Script: [scripts/bash/task-creation-validator.sh](./scripts/bash/task-creation-validator.sh)
- Task Database: [.taskmaster/tasks/tasks.json](./.taskmaster/tasks/tasks.json)

---

**Remember:** Always validate before creating! 🚀
