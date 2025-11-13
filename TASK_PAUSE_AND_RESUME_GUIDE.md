# Task Pause & Resume Guide

## Overview
This guide provides multiple strategies for pausing work, saving progress, and switching between tasks without losing context or momentum.

---

## Strategy 1: Task Master Integration (Recommended)

### Quick Status Update
```bash
# Update current task status to reflect exactly where you stopped
task-master set-status --id=<current-task-id> --status=in-progress

# Add detailed progress notes
task-master update-subtask --id=<current-task-id> --prompt="STOPPED HERE: 
- ✅ Completed: [list what you finished]
- 🔄 In progress: [what you were working on]
- ⏸️ Paused at: [specific point/line/file]
- 📝 Next steps: [what needs to be done next]
- 🐛 Blocking issues: [if any]
- 📊 Files modified: [list key files]
- ⏰ Time spent: [estimate]"

# Mark as ready for next session
task-master set-status --id=<current-task-id> --status=in-progress
```

### Example Progress Log
```bash
task-master update-subtask --id=T100 --prompt="PROGRESS UPDATE - PAUSING FOR BREAK:

✅ COMPLETED:
- Created basic Click CLI structure in src/cli/pr_resolve.py
- Added pr_resolve group command with init subcommand
- Added basic help documentation and error handling
- Tested CLI structure: emailintelligence-cli pr-resolve --help ✓

🔄 IN PROGRESS:
- Working on integrating CLI structure with main emailintelligence_cli.py

⏸️ PAUSED AT:
- Line 45 in emailintelligence_cli.py - need to add import and command registration

📝 NEXT STEPS (for resume):
1. Complete CLI integration in emailintelligence_cli.py
2. Test full integration with emailintelligence-cli pr-resolve init --help
3. Add verbose mode and session ID validation
4. Move to T101: Enhanced error handling

🐛 BLOCKING ISSUES: None
📊 FILES MODIFIED: 
- src/cli/pr_resolve.py (created)
- emailintelligence_cli.py (partial modification)

⏰ TIME SPENT: ~45 minutes
📍 RESUME POINT: Run 'git status' to see changes, continue from emailintelligence_cli.py line 45"
```

---

## Strategy 2: Git Worktree Approach (Parallel Development)

### Create Dedicated Worktree for Pause
```bash
# Create worktree for current task progress
git worktree add ../task-pause-t100-cli-foundation feature/task-t100-cli

# Commit current progress
git add .
git commit -m "feat: pause T100 CLI foundation at integration point

- ✅ Created pr_resolve CLI structure
- ✅ Added Click command groups and subcommands  
- 🔄 Paused at emailintelligence_cli.py integration
- Next: Complete CLI integration and testing

TASK: T100 - Create basic Click CLI structure
STATUS: 75% complete, ready for resume"

# Switch back to main worktree
git checkout main
```

### Resume from Worktree
```bash
# Resume work in paused worktree
git worktree list
git worktree add ../task-resume-t100-cli-foundation feature/task-t100-cli

# Or use existing worktree
cd ../task-pause-t100-cli-foundation
git checkout feature/task-t100-cli

# Continue work where you left off
# Files are exactly as you left them
```

---

## Strategy 3: File-Based Progress Tracking

### Create Pause Log
```bash
# Create progress log file
cat > TASK_PROGRESS_LOG.md << 'EOF'
# Task Progress Log - $(date +"%Y-%m-%d %H:%M:%S")

## Current Task: T100 - CLI Foundation

### Status: IN PROGRESS (Paused)
**Paused at**: $(date)
**Resume Point**: emailintelligence_cli.py line 45

### ✅ Completed Work
- Created src/cli/pr_resolve.py with basic structure
- Added @click.group() for pr_resolve namespace
- Implemented init subcommand with session management
- Added basic error handling and help documentation

### 🔄 In Progress
- Integrating CLI structure with main emailintelligence_cli.py
- Adding import statement and command registration

### ⏸️ Exact Pause Point
- File: emailintelligence_cli.py
- Line: 45 (after CLI import section)
- Action: Need to add `from src.cli.pr_resolve import pr_resolve`
- Next: Add `cli.add_command(pr_resolve, name='pr-resolve')`

### 📝 Files Modified
1. **Created**: src/cli/pr_resolve.py
   - Click CLI structure
   - pr_resolve command group
   - init subcommand
   - Basic error handling

2. **Modified**: emailintelligence_cli.py
   - Partial integration (line ~45)
   - Import needed
   - Command registration pending

### 🧪 Tests Passed
- `emailintelligence-cli pr-resolve --help` ✓
- `emailintelligence-cli pr-resolve init --help` ✓

### 📊 Next Steps (Priority Order)
1. **HIGH**: Complete CLI integration in emailintelligence_cli.py
2. **HIGH**: Test full integration: `emailintelligence-cli pr-resolve init --session-id test`
3. **MEDIUM**: Add verbose mode and enhanced error handling
4. **MEDIUM**: Add session ID validation
5. **LOW**: Add progress indicators

### 🐛 Issues/Blocking
- None currently blocking

### 💡 Notes & Context
- Using Click for CLI structure (following patterns in project)
- Session-based approach for worktree management
- Integration approach: namespace under 'pr-resolve'

### 🔄 Resume Commands
```bash
# 1. Check current state
git status
git diff

# 2. Continue from pause point
# Edit emailintelligence_cli.py at line 45
# Add import and command registration

# 3. Test integration
emailintelligence-cli pr-resolve init --session-id test-resume

# 4. Update TaskMaster when complete
task-master set-status --id=T100 --status=done
```

---
EOF

# Add to git for backup
git add TASK_PROGRESS_LOG.md
git commit -m "docs: pause progress log for T100 CLI foundation

- Progress: 75% complete, paused at CLI integration
- Resume point: emailintelligence_cli.py line 45
- All changes committed, ready for clean resume"
```

---

## Strategy 4: IDE-Specific Approaches

### VS Code Workspace
```json
// .vscode/tasks-pause.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Resume T100 CLI Foundation",
      "type": "shell",
      "command": "echo",
      "args": ["Resuming from emailintelligence_cli.py line 45"],
      "group": "build"
    },
    {
      "label": "Check T100 Progress",
      "type": "shell", 
      "command": "git",
      "args": ["status", "--porcelain"],
      "group": "build"
    }
  ]
}
```

### Vim/NeoVim Sessions
```bash
# Save vim session
:mksession ~/vim-session-t100.vim
# Add progress note to session file
echo "# RESUME POINT: emailintelligence_cli.py line 45" >> ~/vim-session-t100.vim

# Resume later
vim -S ~/vim-session-t100.vim
```

---

## Strategy 5: Automated Scripts

### Create Pause Script
```bash
#!/bin/bash
# pause-task.sh
TASK_ID="$1"
if [ -z "$TASK_ID" ]; then
    echo "Usage: ./pause-task.sh <TASK_ID>"
    exit 1
fi

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="task-pause-${TASK_ID}-${TIMESTAMP}.md"

# Create detailed pause log
cat > "$LOG_FILE" << EOF
# Task Pause Log: $TASK_ID
**Timestamp**: $(date)
**Status**: IN PROGRESS (Paused)

## Quick Status
- Task ID: $TASK_ID
- Pause Time: $(date)
- Files Modified: $(git status --porcelain | wc -l) files

## Progress Summary
$(git log --oneline -5)

## Files Currently Modified
$(git status --short)

## Next Actions
1. Review pause log and current state
2. Continue from exact pause point
3. Test functionality before proceeding
4. Update TaskMaster when complete

## Resume Commands
\`\`\`bash
# Check current state
git status

# Review pause details
cat $LOG_FILE

# Continue work...
\`\`\`
EOF

# Commit current progress
git add .
git commit -m "pause: checkpoint before task $TASK_ID pause

- Task: $TASK_ID
- Pause point: $(date)
- Progress: $(git log --oneline | head -1)

See $LOG_FILE for detailed resume information"

echo "✅ Task $TASK_ID paused successfully"
echo "📄 Pause log: $LOG_FILE"
echo "🔄 Resume: git log --oneline | head -5 (look for commit with 'pause: checkpoint')"
```

### Create Resume Script
```bash
#!/bin/bash
# resume-task.sh
LATEST_PAUSE=$(git log --grep="pause: checkpoint" --oneline -1)

if [ -z "$LATEST_PAUSE" ]; then
    echo "❌ No pause commit found"
    exit 1
fi

echo "🔄 Resuming from: $LATEST_PAUSE"
echo "📋 Pause details:"
git show --stat HEAD

# List pause files
echo "📄 Available pause logs:"
ls -la task-pause-*.md | tail -5
```

---

## Strategy 6: Quick CLI Resume Commands

### Basic Resume Workflow
```bash
# 1. Check current status
git status
task-master next

# 2. Review where you stopped
git log --oneline -3
cat $(ls -t task-pause-*.md | head -1)

# 3. Resume specific task
task-master show <task-id>  # See details
task-master set-status --id=<task-id> --status=in-progress

# 4. Continue work
# ... your implementation ...

# 5. Update when complete
task-master set-status --id=<task-id> --status=done
task-master update-subtask --id=<task-id> --prompt="Completed: [what you finished]"
```

---

## Best Practices Summary

### ✅ DO:
- **Commit progress** before pausing (even small commits)
- **Update TaskMaster** with detailed status notes
- **Document exact pause points** (file, line, function)
- **Include next steps** in pause notes
- **Tag commits** for easy recovery: `git tag pause-T100-before-integration`

### ❌ DON'T:
- Leave work uncommitted (risk of losing progress)
- Pause without documenting what needs to be done next
- Forget to update TaskMaster status
- Leave IDEs/files in inconsistent states
- Skip writing clear resume instructions

### 🎯 Quick Reference:
```bash
# FASTEST PAUSE (30 seconds)
git add . && git commit -m "pause: $(date)" && task-master update-subtask --id=<id> --prompt="PAUSED: continue from [point]"

# FASTEST RESUME (15 seconds)  
git status && task-master show <id> && task-master set-status --id=<id> --status=in-progress
```

This approach ensures you can pause work at any point and resume efficiently, maintaining context and momentum across multiple work sessions.