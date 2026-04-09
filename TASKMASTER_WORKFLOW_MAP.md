# Taskmaster Workflow Map

## Overview

This project uses **Taskmaster AI** as the primary task management system, integrated via both CLI and MCP (Model Context Protocol). The system enables AI-powered task creation, breakdown, and tracking with support for tagged task lists, complex dependency management, and iterative implementation logging.

The project also maintains **Backlog.md** as a secondary project management tool with its own CLI, providing board visualization, Kanban-style workflow, and Git-integrated task tracking.

---

## Task Files Structure

| Location | Purpose |
|----------|---------|
| `.taskmaster/` | Core Taskmaster configuration and tasks directory |
| `.taskmaster/config.json` | AI model configuration, parameters, and settings |
| `.taskmaster/tasks/tasks.json` | Main task data store (JSON) |
| `.taskmaster/tasks/` | Individual task markdown files (auto-generated) |
| `.taskmaster/reports/` | Complexity analysis and reporting outputs |
| `.taskmaster/docs/` | PRD files, research summaries, and guides |
| `backlog/` | Backlog.md project management system |
| `backlog/config.yml` | Backlog.md configuration |
| `backlog/tasks/` | Backlog.md task markdown files |
| `backlog/docs/` | Project documentation |
| `backlog/decisions/` | Architectural decision records |
| `backlog/sessions/` | Session tracking and notes |
| `specs/004-guided-workflow/tasks.md` | Main task specification for guided workflows |
| `AGENTS.md` | Agent integration guide with Taskmaster commands |
| `.mcp.json` | MCP server configuration for Taskmaster |

---

## Task Flow

### 1. Creation

**Via PRD Parsing (Recommended):**
```bash
# Create PRD file
touch task-migration-checklist.md

# Parse PRD into tasks
task-master parse-prd task-migration-checklist.md --append

# Analyze complexity
task-master analyze-complexity --research

# Expand into subtasks
task-master expand --all --research
```

**Via Direct Task Creation:**
```bash
# Add task via prompt (AI-structured)
task-master add-task --prompt="Implement user authentication"

# Add subtask to existing task
task-master add-subtask --parent 1 --title "Create OAuth flow"
```

### 2. Tracking

**View Tasks:**
```bash
# List all tasks
task-master list

# Show next available task
task-master next

# Show specific task details
task-master show 1

# Filter by status
task-master list --status pending,in-progress
```

**Via MCP Tools (for AI agents):**
- `get_tasks` - List all tasks
- `next_task` - Get next available task
- `get_task` - View specific task details

### 3. Implementation

**Iterative Workflow:**
```bash
# Log implementation plan
task-master update-subtask --id=1.1 --prompt="Plan: Explore codebase..."

# Update status to in-progress
task-master set-status --id=1.1 --status in-progress

# Log progress during implementation
task-master update-subtask --id=1.1 --prompt="What worked: X, What didn't: Y"

# Mark complete
task-master set-status --id=1.1 --status done

# Update dependent tasks if implementation differs
task-master update --from=2 --prompt="Implementation changed approach..."
```

### 4. Completion

**Definition of Done:**
1. All subtasks completed and marked `done`
2. Implementation notes added via `update-subtask`
3. Code tested (lint, typecheck, tests pass)
4. Task status set to `done`

**Git Integration:**
```bash
# Create PR for completed task
gh pr create --title "Complete task 1.2: Feature" --body "Implements task 1.2"

# Reference in commits
git commit -m "feat: implement auth (task 1.2)"
```

---

## CLI Tools Reference

### Core Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `task-master init` | Initialize Taskmaster in project | `task-master init --name "Project"` |
| `task-master parse-prd` | Parse PRD into tasks | `task-master parse-prd file.md --append` |
| `task-master list` | List all tasks | `task-master list --status pending` |
| `task-master next` | Show next available task | `task-master next` |
| `task-master show` | Display task details | `task-master show 1.2` |
| `task-master add-task` | Add new task via prompt | `task-master add-task --prompt="..."` |
| `task-master add-subtask` | Add subtask to parent | `task-master add-subtask --parent 1 --title "..."` |
| `task-master expand` | Break task into subtasks | `task-master expand --id=1 --research` |
| `task-master expand --all` | Expand all pending tasks | `task-master expand --all --research` |
| `task-master set-status` | Update task status | `task-master set-status --id=1 --status done` |
| `task-master update-subtask` | Log progress/notes | `task-master update-subtask --id=1.1 --prompt="..."` |
| `task-master update` | Update multiple tasks | `task-master update --from=2 --prompt="..."` |
| `task-master update-task` | Update single task | `task-master update-task --id=1 --prompt="..."` |
| `task-master generate` | Regenerate task markdown files | `task-master generate` |

### Dependency Management

| Command | Purpose | Usage |
|---------|---------|-------|
| `task-master add-dependency` | Add task dependency | `task-master add-dependency --id=2 --depends-on=1` |
| `task-master remove-dependency` | Remove dependency | `task-master remove-dependency --id=2 --depends-on=1` |
| `task-master validate-dependencies` | Check for issues | `task-master validate-dependencies` |
| `task-master fix-dependencies` | Auto-fix issues | `task-master fix-dependencies` |

### Analysis & Reporting

| Command | Purpose | Usage |
|---------|---------|-------|
| `task-master analyze-complexity` | Analyze task complexity | `task-master analyze-complexity --research` |
| `task-master complexity-report` | View complexity report | `task-master complexity-report` |
| `task-master models` | Configure AI models | `task-master models --setup` |

### Tag Management (Multi-Context)

| Command | Purpose | Usage |
|---------|---------|-------|
| `task-master tags` | List all tags | `task-master tags` |
| `task-master add-tag` | Create new tag | `task-master add-tag feature-auth` |
| `task-master use-tag` | Switch active tag | `task-master use-tag feature-auth` |
| `task-master delete-tag` | Delete tag | `task-master delete-tag experiment-v1` |

### Utility Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `task-master move` | Reorganize tasks | `task-master move --from=5 --to=10` |
| `task-master remove-task` | Delete task | `task-master remove-task --id=5 --yes` |
| `task-master clear-subtasks` | Clear subtasks | `task-master clear-subtasks --id=1` |
| `task-master sync-readme` | Export to README | `task-master sync-readme --status done` |

---

## MCP Tools

Taskmaster MCP server is configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "type": "stdio",
      "command": "npm",
      "args": ["exec", "task-master-ai"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "XAI_API_KEY": "${XAI_API_KEY}",
        "OPENROUTER_API_KEY": "${OPENROUTER_API_KEY}",
        "MISTRAL_API_KEY": "${MISTRAL_API_KEY}",
        "OLLAMA_API_KEY": "${OLLAMA_API_KEY}",
        "GITHUB_API_KEY": "${GITHUB_API_KEY}"
      },
      "alwaysAllow": ["add_task", "expand_task"]
    }
  }
}
```

### Available MCP Tools

| Tool | Function |
|------|-----------|
| `initialize_project` | Set up Taskmaster file structure |
| `parse_prd` | Parse PRD into tasks |
| `get_tasks` | List tasks with optional filtering |
| `next_task` | Get next available task |
| `get_task` | View specific task details |
| `add_task` | Create new task via AI |
| `add_subtask` | Add subtask to parent |
| `expand_task` | Break task into subtasks |
| `expand_all` | Expand all pending tasks |
| `set_task_status` | Update task status |
| `update_subtask` | Append timestamped notes |
| `update_task` | Modify specific task |
| `update` | Update multiple future tasks |
| `add_dependency` | Add task dependency |
| `remove_dependency` | Remove dependency |
| `validate_dependencies` | Check dependency integrity |
| `fix_dependencies` | Auto-fix dependency issues |
| `analyze_project_complexity` | Analyze task complexity |
| `complexity_report` | View formatted complexity report |
| `list_tags` | List all available tags |
| `add_tag` | Create new tag |
| `delete_tag` | Delete tag |
| `use_tag` | Switch active tag |
| `move_task` | Reorganize task hierarchy |
| `models` | Configure AI models |

---

## Backlog.md (Secondary System)

The project also maintains **Backlog.md** as an alternative task management system with different capabilities.

### Quick Reference

```bash
# List tasks
backlog task list --plain

# View task
backlog task 42 --plain

# Create task
backlog task create "Title" -d "Description" --ac "Criterion 1"

# Edit task
backlog task edit 42 -s "In Progress" -a @myself

# Check acceptance criteria
backlog task edit 42 --check-ac 1 --check-ac 2

# Add notes
backlog task edit 42 --notes "Implementation complete"

# Search tasks
backlog search "auth" --plain
```

### Comparison

| Feature | Taskmaster | Backlog.md |
|---------|------------|------------|
| AI-powered task generation | ✅ | ❌ |
| Tagged task lists | ✅ | ❌ |
| Complexity analysis | ✅ | ❌ |
| MCP integration | ✅ | ✅ |
| Kanban board | ❌ | ✅ |
| Acceptance criteria | Manual | Built-in |
| Git integration | Via conventions | Built-in |

---

## Important Notes

### AI-Powered Operations (may take up to a minute)
- `parse_prd` / `task-master parse-prd`
- `analyze_project_complexity` / `task-master analyze-complexity`
- `expand_task` / `task-master expand`
- `expand_all` / `task-master expand --all`
- `add_task` / `task-master add-task`
- `update` / `task-master update`
- `update_task` / `task-master update-task`
- `update_subtask` / `task-master update-subtask`

### File Management Rules
- **NEVER** manually edit `tasks.json` - use commands instead
- **NEVER** manually edit `.taskmaster/config.json` - use `task-master models`
- Task markdown files in `tasks/` are auto-generated
- Run `task-master generate` after manual changes to tasks.json

### API Key Configuration
- For CLI: Set in `.env` file in project root
- For MCP: Set in `.mcp.json` env section

### Research Mode
Add `--research` flag for AI-enhanced results using Perplexity:
```bash
task-master expand --id=1 --research
task-master analyze-complexity --research
```

---

## Troubleshooting

### AI Commands Failing
```bash
# Check API keys
cat .env

# Verify model configuration
task-master models

# Test with fallback model
task-master models --set-fallback gpt-4o-mini
```

### MCP Connection Issues
- Check `.mcp.json` configuration
- Verify Node.js installation
- Use `--mcp-debug` flag when starting Claude Code
- Use CLI as fallback if MCP unavailable

### Task File Sync Issues
```bash
# Regenerate task files
task-master generate

# Fix dependency issues
task-master fix-dependencies
```

---

## Related Documentation

- `AGENTS.md` - Agent integration guide
- `docs/guides/taskmaster_workflow_guide.md` - User-facing workflow guide
- `docs/guides/taskmaster_troubleshooting.md` - Troubleshooting guide
- `.github/instructions/taskmaster.instructions.md` - CLI command reference
- `.github/instructions/dev_workflow.instructions.md` - Development workflow patterns
- `specs/004-guided-workflow/tasks.md` - Main task specification
