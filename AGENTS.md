# Task Master AI - Agent Integration Guide

## ⚠️ Branch-Specific Guidance

**Select your branch below to find the correct agent documentation:**

### 🌳 Scientific Branch
**If working on the `scientific` branch:** Use the scientific branch AGENTS.md instead
- Focuses on FastAPI backend, email processing, AI analysis, API routes
- Includes build/test commands (uv sync, pytest, coverage)
- Code style: absolute imports, PascalCase classes, snake_case functions
- Architecture: src/backend/, src/core/, modules/ (plugins), tests/
- **Switch to scientific branch documentation** for development guidance

### 📋 Main & orchestration-tools Branches
**If working on `main` or orchestration-tools-*:** Use this guide (below)

### 🛠️ Task Master Branch
**If working on the `taskmaster` branch:**
- Dedicated Task Master development worktree with isolated git history
- Must maintain strict branch isolation from orchestration-tools
- See `TASKMASTER_BRANCH_CONVENTIONS.md` for critical requirements
- **CRITICAL**: Taskmaster worktree files must never be committed on other branches

### Branch-Specific Extensions

For branch-specific agent guidance, check for `AGENTS_{branch-name}.md` files:

- `AGENTS_scientific.md` - Scientific branch extensions
- `AGENTS_orchestration-tools.md` - Orchestration tools branch extensions
- `AGENTS_[branch-name].md` - Other branch-specific guides (as they exist)

These files extend the core guidance in this file with branch-specific commands, workflows, and considerations. If a file exists for your current branch, it supplements this guide.

**IMPORTANT: Branch Isolation**
- See `TASKMASTER_BRANCH_CONVENTIONS.md` before working with taskmaster branch
- Prevents contamination between development environments
- Protects branch-specific configurations and worktree integrity

---

## Essential Commands

### Core Workflow Commands

```bash
# Project Setup
task-master init                                    # Initialize Task Master in current project
task-master parse-prd .taskmaster/docs/prd.txt      # Generate tasks from PRD document
task-master models --setup                        # Configure AI models interactively

# Daily Development Workflow
task-master list                                   # Show all tasks with status
task-master next                                   # Get next available task to work on
task-master show <id>                             # View detailed task information (e.g., task-master show 1.2)
task-master set-status --id=<id> --status=done    # Mark task complete

# Task Management
task-master add-task --prompt="description" --research        # Add new task with AI assistance
task-master expand --id=<id> --research --force              # Break task into subtasks
task-master update-task --id=<id> --prompt="changes"         # Update specific task
task-master update --from=<id> --prompt="changes"            # Update multiple tasks from ID onwards
task-master update-subtask --id=<id> --prompt="notes"        # Add implementation notes to subtask

# Analysis & Planning
task-master analyze-complexity --research          # Analyze task complexity
task-master complexity-report                      # View complexity analysis
task-master expand --all --research               # Expand all eligible tasks

# Dependencies & Organization
task-master add-dependency --id=<id> --depends-on=<id>       # Add task dependency
task-master move --from=<id> --to=<id>                       # Reorganize task hierarchy
task-master validate-dependencies                            # Check for dependency issues
task-master generate                                         # Update task markdown files (usually auto-called)
```

### Orchestration Control Commands

```bash
# Disable All Orchestration (with branch profile sync & push)
./scripts/disable-all-orchestration-with-branch-sync.sh      # Disable hooks, env vars, branch profiles, push to scientific/main
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push  # Same but don't auto-push

# Re-enable All Orchestration (with branch profile sync & push)
./scripts/enable-all-orchestration-with-branch-sync.sh       # Enable hooks, env vars, branch profiles, push to scientific/main
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push   # Same but don't auto-push

# Original Disable/Enable (no branch sync)
./scripts/disable-all-orchestration.sh                       # Disable hooks and env var only
./scripts/enable-all-orchestration.sh                        # Enable hooks and clear env var only

# Hook-only Control
./scripts/disable-orchestration-hooks.sh                     # Disable git hooks only
./scripts/restore-orchestration-hooks.sh                     # Restore git hooks only
```

## Key Files & Project Structure

### Core Files

- `.taskmaster/tasks/tasks.json` - Main task data file (auto-managed)
- `.taskmaster/config.json` - AI model configuration (use `task-master models` to modify)
- `.taskmaster/docs/prd.txt` - Product Requirements Document for parsing
- `.taskmaster/tasks/*.txt` - Individual task files (auto-generated from tasks.json)
- `.env` - API keys for CLI usage

### Directory Structure

```
project/
├── .taskmaster/
│   ├── tasks/              # Task files directory
│   │   ├── tasks.json      # Main task database
│   │   ├── task-1.md      # Individual task files
│   │   └── task-2.md
│   ├── docs/              # Documentation directory
│   │   ├── prd.txt        # Product requirements
│   ├── reports/           # Analysis reports directory
│   │   └── task-complexity-report.json
│   ├── templates/         # Template files
│   │   └── example_prd.txt  # Example PRD template
│   └── config.json        # AI models & settings
├── .claude/
│   ├── settings.json      # Claude Code configuration
│   └── commands/         # Custom slash commands
├── .env                  # API keys
├── .mcp.json            # MCP configuration
└── CLAUDE.md            # This file - auto-loaded by Claude Code
```

## MCP Integration

Task Master provides an MCP server that Claude Code can connect to. Configure in `.mcp.json`.

## Claude Code Workflow Integration

### Standard Development Workflow

1. **Project Initialization**: `task-master init`, `task-master parse-prd`
2. **Daily Development**: `task-master next`, `task-master show`, `task-master update-subtask`, `task-master set-status`

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and completion
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->
