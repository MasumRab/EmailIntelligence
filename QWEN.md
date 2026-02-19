# Taskmaster - AI-Powered Task Management System

## Project Overview

Taskmaster is an AI-powered task management system designed for specification-driven development workflows. It provides automated task generation, analysis, and tracking with deep integration into Git workflows and AI assistants.

**Current Project Focus:** Branch Alignment Tooling - Git branch clustering, merge automation, and validation systems.

**⚠️ CRITICAL:** This is NOT an EmailIntelligence project. EmailIntelligence materials exist separately in `tasks/mvp/` only. See [PROJECT_IDENTITY.md](PROJECT_IDENTITY.md) for details.

### Core Capabilities

- **AI-Powered Task Generation:** Parse PRD documents into structured, actionable tasks
- **Task Expansion:** Break high-level tasks into detailed subtasks with AI assistance
- **Git Integration:** Advanced conflict detection and resolution using worktrees
- **Constitutional Analysis:** Specification-driven development and compliance checking
- **Session Management:** Documented development sessions with full state tracking
- **MCP Integration:** Model Context Protocol support for AI assistant integration

---

## Quick Start

### Setup

```bash
# Install dependencies
pip install poetry
poetry install

# Configure API keys (at least one required)
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
echo "PERPLEXITY_API_KEY=your_key_here" >> .env

# Initialize Taskmaster (if not already done)
task-master init
```

### Daily Workflow

```bash
# Get next task to work on
task-master next

# View task details
task-master show <id>

# Mark task complete
task-master set-status --id=<id> --status=done

# List all tasks
task-master list
```

---

## Project Structure

```
.taskmaster/
├── tasks/                    # Task specifications (14-section standard)
│   ├── tasks.json           # Task database (auto-managed)
│   ├── task_001.md          # Individual task files
│   ├── task_002.1.md        # Subtask files (ID.subtask format)
│   └── mvp/                 # Separate EmailIntelligence project
├── docs/                     # Documentation
│   ├── prd.md               # Product Requirements Document
│   ├── master-prd.txt       # Master PRD
│   └── branch-alignment-framework-prd.txt
├── src/                      # Source code
│   ├── analysis/            # Constitutional & conflict analysis
│   ├── core/                # Core interfaces & models
│   ├── git/                 # Git operations & conflict detection
│   ├── resolution/          # Auto-resolution & semantic merging
│   ├── strategy/            # Strategy generation & risk assessment
│   ├── validation/          # Validation components
│   └── main.py              # FastAPI application
├── scripts/                  # Automation utilities
├── archive/                  # Archived documentation (historical)
├── backups/                  # Backup files
├── complexity_reports/       # Task complexity analysis
├── guidance/                 # Implementation guidance
├── templates/                # Task templates
├── tests/                    # Test suite
├── .qwen/                    # Session management
│   ├── session_manager.py   # Session state management
│   └── session_cli.py       # CLI for sessions
├── CLAUDE.md                # Auto-loaded agent context
├── AGENT.md                 # Agent integration guide
├── taskmaster_cli.py        # Main CLI tool
├── emailintelligence_cli.py # Git worktree conflict resolution CLI
└── QWEN.md                  # This file
```

---

## Building and Running

### Prerequisites

- Python 3.8+
- Git with worktree support
- API keys for AI providers (Anthropic, OpenAI, Gemini, Perplexity, etc.)

### Installation

```bash
# Using Poetry (recommended)
pip install poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

### Running the Application

```bash
# Run FastAPI application
python src/main.py

# Or with uvicorn
uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000

# Run CLI tool
python taskmaster_cli.py --help

# Run EmailIntelligence CLI (git conflict resolution)
python emailintelligence_cli.py --help
```

### Session Management

```bash
# Start a new session with goals
python .qwen/session_cli.py start --goals "Implement feature X,Fix bug Y"

# Show current session
python .qwen/session_cli.py show

# View project context
python .qwen/session_cli.py context

# End session
python .qwen/session_cli.py end
```

---

## Core Commands Reference

### Project Setup

```bash
task-master init                                    # Initialize Task Master
task-master parse-prd .taskmaster/docs/prd.md       # Generate tasks from PRD
task-master models --setup                          # Configure AI models
```

### Task Management

```bash
task-master list                                    # Show all tasks
task-master next                                    # Get next task
task-master show <id>                               # View task details
task-master set-status --id=<id> --status=done     # Mark complete
task-master add-task --prompt="desc" --research     # Add task with AI
task-master expand --id=<id> --research             # Expand to subtasks
task-master update-subtask --id=<id> --prompt=".."  # Log implementation notes
```

### Analysis & Planning

```bash
task-master analyze-complexity --research           # Analyze complexity
task-master complexity-report                       # View complexity report
task-master expand --all --research                 # Expand all tasks
task-master validate-dependencies                   # Check dependencies
```

### Git Worktree Operations (EmailIntelligence CLI)

```bash
eai setup-resolution --pr 123 --source-branch feature --target-branch main
eai analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml
eai develop-spec-kit-strategy --pr 123 --worktrees --interactive
eai align-content --pr 123 --interactive --checkpoint-each-step
eai validate-resolution --pr 123 --comprehensive
eai auto-resolve --pr 123
```

---

## Task Structure Standard

All tasks follow a **14-section standard format** (see [TASK_STRUCTURE_STANDARD.md](TASK_STRUCTURE_STANDARD.md)):

1. **Task Header** - ID, title, status, priority, effort, complexity, dependencies
2. **Overview/Purpose** - What this task accomplishes and why
3. **Success Criteria** - Detailed, complete checklist of done conditions
4. **Prerequisites & Dependencies** - What must be done before starting
5. **Sub-subtasks Breakdown** - Detailed breakdown with effort estimates
6. **Specification Details** - Technical specification (interfaces, schemas)
7. **Implementation Guide** - Step-by-step how-to for each sub-subtask
8. **Configuration Parameters** - Externalized, non-hardcoded parameters
9. **Performance Targets** - Clear performance requirements
10. **Testing Strategy** - Unit tests, integration tests, coverage targets
11. **Common Gotchas & Solutions** - Prevent common mistakes
12. **Integration Checkpoint** - Gate for moving to next task
13. **Done Definition** - Complete checklist for "done"
14. **Next Steps** - What to do after this task

### Task ID Format

- Main tasks: `001`, `002`, `007`, etc.
- Subtasks: `002.1`, `002.2`, `007.3`, etc.
- Sub-subtasks: `002.1.1`, `002.1.2`, etc.

### Task Status Values

- `pending` - Ready to work on
- `in-progress` - Currently being worked on
- `done` - Completed and verified
- `deferred` - Postponed
- `cancelled` - No longer needed
- `blocked` - Waiting on external factors

---

## Current Active Tasks (Phase 3)

**⚠️ Old task numbering (task-001 through task-020) is DEPRECATED.**

### Active Tasks:

| Task ID | Title | Status |
|---------|-------|--------|
| `001` | Align and Architecturally Integrate Feature Branches | Ready |
| `002` | Analysis Stage (Clustering Pipeline) | Pending |
| `003` | Clustering Stage | Pending |
| `004` | Integration Stage | Pending |
| `005` | Branch Clustering System | In Progress |
| `007` | Branch Alignment Strategy Framework | Ready |
| `075.1-5` | Alignment Analyzers | Ready |
| `079` | Orchestration Framework | Ready |
| `080` | Validation Integration | Ready |
| `083` | E2E Testing & Reporting | Ready |

**See:** [PROJECT_STATE_PHASE_3_READY.md](PROJECT_STATE_PHASE_3_READY.md) for full status.

---

## MCP Integration

Taskmaster provides an MCP server for AI assistant integration. Configure in `.mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "TASK_MASTER_TOOLS": "core",
        "ANTHROPIC_API_KEY": "your_key_here",
        "PERPLEXITY_API_KEY": "your_key_here",
        "OPENAI_API_KEY": "your_key_here",
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

### MCP Tool Tiers

| Tier | Count | Tools |
|------|-------|-------|
| `core` | 7 | `get_tasks`, `next_task`, `get_task`, `set_task_status`, `update_subtask`, `parse_prd`, `expand_task` |
| `standard` | 14 | core + `initialize_project`, `analyze_project_complexity`, `expand_all`, `add_subtask`, `remove_task`, `add_task`, `complexity_report` |
| `all` | 44+ | standard + dependencies, tags, research, autopilot, scoping, models, rules |

---

## Development Conventions

### Code Quality

- **Python:** PEP 8 compliant with type hints
- **Docstrings:** Google-style comprehensive documentation
- **Testing:** Minimum 95% code coverage target
- **Error Handling:** Comprehensive exception handling throughout

### Git Workflows

- Use git worktrees for parallel development
- Constitutional analysis for code reviews
- Worktree-based conflict resolution
- Safe branching and merging with validation

### Task Management

- Use `--research` flag for complex technical tasks requiring AI assistance
- Update subtasks with implementation notes using `update-subtask`
- Follow the 14-section task structure standard
- Track dependencies to manage task relationships

### Content Duplication Prevention

**Critical:** Follow guidelines in [CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md](CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md):

- Pre-processing validation for content uniqueness
- Template application controls (single application only)
- Atomic operations with backup mechanisms
- Clear content boundary management
- Source attribution for all content

---

## AI Model Configuration

Configure models interactively:

```bash
task-master models --setup
```

### Required API Keys

At least **one** of these must be configured in `.env`:

- `ANTHROPIC_API_KEY` (Claude models) - **Recommended**
- `PERPLEXITY_API_KEY` (Research features) - **Highly recommended**
- `OPENAI_API_KEY` (GPT models)
- `GOOGLE_API_KEY` (Gemini models)
- `MISTRAL_API_KEY` (Mistral models)
- `OPENROUTER_API_KEY` (Multiple models)
- `XAI_API_KEY` (Grok models)

### Model Tiers

- **Main Model:** Primary AI for task operations
- **Research Model:** Enhanced research capabilities (Perplexity recommended)
- **Fallback Model:** Backup when primary unavailable

---

## Troubleshooting

### AI Commands Failing

```bash
# Check API keys configured
cat .env

# Verify model configuration
task-master models

# Test with different model
task-master models --set-fallback gpt-4o-mini
```

### MCP Connection Issues

- Check `.mcp.json` configuration
- Verify Node.js installation
- Use CLI as fallback if MCP unavailable

### Task File Sync Issues

```bash
# Regenerate task files from tasks.json
task-master generate

# Fix dependency issues
task-master validate-dependencies
```

### Common Issues

| Issue | Solution |
|-------|----------|
| AI commands timeout | Check API key, try fallback model |
| Task files out of sync | Run `task-master generate` |
| Dependency errors | Run `task-master validate-dependencies` |
| MCP not connecting | Check `.mcp.json`, restart MCP server |

---

## Important Notes

### AI-Powered Operations

These commands make AI calls and may take up to a minute:

- `parse_prd` / `task-master parse-prd`
- `analyze_project_complexity` / `task-master analyze-complexity`
- `expand_task` / `task-master expand`
- `expand_all` / `task-master expand --all`
- `add_task` / `task-master add-task`
- `update` / `task-master update`
- `update_task` / `task-master update-task`
- `update_subtask` / `task-master update-subtask`

### File Management

- **Never** manually edit `tasks.json` - use commands instead
- **Never** manually edit `.taskmaster/config.json` - use `task-master models`
- Task markdown files in `tasks/` are auto-generated
- Run `task-master generate` after manual changes to tasks.json

### DO NOT

- **DO NOT** re-initialize (adds nothing new)
- **DO NOT** merge non-alignment content into alignment tasks
- **DO NOT** treat historical pivot proposals as canonical
- **DO NOT** use old task numbering (task-001 through task-020 deprecated)

---

## Key Documentation

### Essential Reading

| Document | Purpose | Audience |
|----------|---------|----------|
| [CLAUDE.md](CLAUDE.md) | Auto-loaded agent context | AI agents |
| [AGENT.md](AGENT.md) | Agent integration guide | All agents |
| [PROJECT_IDENTITY.md](PROJECT_IDENTITY.md) | **CRITICAL:** Project scope & identity | Everyone |
| [PROJECT_STATE_PHASE_3_READY.md](PROJECT_STATE_PHASE_3_READY.md) | Current phase status | Everyone |
| [TASK_STRUCTURE_STANDARD.md](TASK_STRUCTURE_STANDARD.md) | Task format standard | Developers |
| [CURRENT_DOCUMENTATION_MAP.md](CURRENT_DOCUMENTATION_MAP.md) | Documentation navigation | Everyone |

### Reference Documents

| Document | Purpose |
|----------|---------|
| [CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md](CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md) | Prevent content corruption |
| [OLD_TASK_NUMBERING_DEPRECATED.md](OLD_TASK_NUMBERING_DEPRECATED.md) | Why old numbering deprecated |
| [SESSION_MANAGEMENT_IMPLEMENTATION.md](SESSION_MANAGEMENT_IMPLEMENTATION.md) | Session system details |
| [COMPLETE_TASK_WORKFLOW.md](COMPLETE_TASK_WORKFLOW.md) | Full task workflow guide |

---

## Session Management System

Taskmaster includes comprehensive session management for documented development:

### Features

- **State Management:** Tracks current session and command history
- **Session Lifecycle:** Start, run, and end development sessions
- **Project Context:** Captures documentation and pending handoffs
- **Cross-Project Registration:** Maintains project registry

### Usage

```python
from .qwen.session_manager import SessionManager

# Initialize for current project
sm = SessionManager("/path/to/project")

# Start session with goals
session_info = sm.start_session(
    goals=["Implement feature X", "Fix bug Y"]
)

# Get current session info
current = sm.get_current_session()

# End session
sm.end_session()
```

---

## Best Practices

### Task Workflow

1. Start with `task-master next` to get next task
2. Use `task-master show <id>` to review details
3. Expand complex tasks: `task-master expand --id=<id> --research`
4. Log progress: `task-master update-subtask --id=<id> --prompt="notes"`
5. Mark complete: `task-master set-status --id=<id> --status=done`

### Multi-Claude Workflows

For complex projects, use multiple sessions:

```bash
# Terminal 1: Main implementation
cd project && claude

# Terminal 2: Testing
cd project-test-worktree && claude

# Terminal 3: Documentation
cd project-docs-worktree && claude
```

### Git Integration

```bash
# Create worktrees for parallel development
git worktree add ../project-auth feature/auth-system
git worktree add ../project-api feature/api-refactor

# Create PR for completed task
gh pr create --title "Complete task 002.1" --body "Implements clustering"

# Reference task in commits
git commit -m "feat: implement clustering (task 002.1)"
```

---

## Resources

- [Task Master AI Documentation](https://taskmaster.ai/docs)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Claude Code Integration](CLAUDE.md)
- [Git Worktree Documentation](docs/branch-alignment-framework-prd.txt)

---

**Last Updated:** February 19, 2026
**Project Status:** Phase 3 - Specifications Complete, Implementation Ready
**Active Tasks:** 9 tasks (007, 075.1-5, 079-083)
