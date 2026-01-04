# Gemini CLI-Specific Instructions

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only Gemini CLI-specific features and integrations.

## MCP Configuration for Gemini CLI

Configure Task Master MCP server in `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"]
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## Gemini CLI-Specific Features

### Session Management

Built-in session commands:

- `/chat` - Start new conversation while keeping context
- `/checkpoint save <name>` - Save session state
- `/checkpoint load <name>` - Resume saved session
- `/memory show` - View loaded context

Both `AGENTS.md` and `GEMINI.md` are auto-loaded on every Gemini CLI session.

### Headless Mode for Automation

Non-interactive mode for scripts:

```bash
# Simple text response
gemini -p "What's the next task?"

# JSON output for parsing
gemini -p "List all pending tasks" --output-format json

# Stream events for long operations
gemini -p "Expand all tasks" --output-format stream-json
```

### Token Usage Monitoring

```bash
# In Gemini CLI session
/stats

# Shows: token usage, API costs, request counts
```

### Google Search Grounding

Leverage built-in Google Search as an alternative to Perplexity research mode:
- Best practices research
- Library documentation
- Security vulnerability checks
- Implementation patterns

## Important Differences from Other Agents

### No Slash Commands
Gemini CLI does not support custom slash commands (unlike Claude Code). Use natural language instead.

### No Tool Allowlist
Security is managed at the MCP level, not via agent configuration.

### Session Persistence
Use `/checkpoint` instead of git worktrees for managing multiple work contexts.

### Configuration Files
- Global: `~/.gemini/settings.json`
- Project: `.gemini/settings.json`
- **Not**: `.mcp.json` (that's for Claude Code)

## Recommended Model Configuration

For Gemini CLI users:

```bash
# Set Gemini as primary model
task-master models --set-main gemini-2.0-flash-exp
task-master models --set-fallback gemini-1.5-flash

# Optional: Use Perplexity for research (or rely on Google Search)
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
```

## Your Role with Gemini CLI

As a Gemini CLI assistant with Task Master:

1. **Use MCP tools naturally** - They integrate transparently in conversation

## Script Integration

The `.taskmaster/scripts/` directory provides automation utilities that Gemini CLI can use for task management, Git operations, and orchestration workflows.

### Task Management Scripts

**Core Operations:**
```bash
# List tasks with filtering
python scripts/list_tasks.py --status pending --priority high
python scripts/list_tasks.py --show-subtasks

# Show task details
python scripts/show_task.py 7
python scripts/show_task.py 1 --invalid

# Find next task
python scripts/next_task.py

# Search tasks
python scripts/search_tasks.py "security" --show-context
python scripts/search_tasks.py "validation" --case-sensitive

# Generate summary
python scripts/task_summary.py

# Compare task files
python scripts/compare_task_files.py

# List invalid tasks
python scripts/list_invalid_tasks.py --status done
```

**Task Generation & Enhancement:**
```bash
# Generate clean sequential task files
python scripts/generate_clean_tasks.py

# Enhance tasks from archive
python scripts/enhance_tasks_from_archive.py

# Split enhanced plan into task files
python scripts/split_enhanced_plan.py --dry-run
python scripts/split_enhanced_plan.py

# Regenerate tasks.json from plan
python scripts/regenerate_tasks_from_plan.py --validate
python scripts/regenerate_tasks_from_plan.py
```

**Task Recovery:**
```bash
# Find lost tasks in git history
python scripts/find_lost_tasks.py --commits 50
python scripts/find_lost_tasks.py --output lost_tasks.json --verbose
```

### Orchestration Scripts

**Git Hooks Management:**
```bash
# Disable hooks for independent development
./scripts/disable-hooks.sh

# Bypass hooks on single operations
DISABLE_ORCHESTRATION_CHECKS=1 git checkout <branch>
DISABLE_ORCHESTRATION_CHECKS=1 git merge <branch>
```

**Worktree Synchronization:**
```bash
# Sync setup files between worktrees
./scripts/sync_setup_worktrees.sh --dry-run
./scripts/sync_setup_worktrees.sh --verbose
```

**Orchestration Branch Management:**
```bash
# Reverse sync approved changes to orchestration-tools
./scripts/reverse_sync_orchestration.sh feature/fix abc123 --dry-run
./scripts/reverse_sync_orchestration.sh feature/fix abc123

# Update configuration
./scripts/update_flake8_orchestration.sh --yes
```

### Gemini CLI Integration

**Using Scripts with Gemini CLI:**

```bash
# Natural language command to run script
gemini -p "Run search_tasks.py to find all tasks about security"

# Headless mode with JSON output
gemini -p "Generate task summary using task_summary.py" --output-format json

# Stream events for long operations
gemini -p "Find lost tasks in git history" --output-format stream-json
```

**Session-Based Workflow:**

```bash
# Start session
gemini

# Use MCP tools
> next_task
> get_task --id=7

# Use scripts for advanced operations
> Run python scripts/search_tasks.py "branch alignment" --show-context
> Run python scripts/task_summary.py
> Run ./scripts/sync_setup_worktrees.sh --dry-run

# Save checkpoint
> /checkpoint save task-review

# Resume later
> /checkpoint load task-review
```

**Headless Automation:**

```bash
# Automated task discovery
gemini -p "List all pending high-priority tasks using list_tasks.py" --output-format json

# Automated task analysis
gemini -p "Compare task files and generate report using compare_task_files.py" --output-format json

# Automated recovery
gemini -p "Find lost tasks in last 100 commits" --output-format json
```

### Script Security

All Python scripts implement security validation:
- **Path Security**: Prevents directory traversal and URL encoding attacks
- **File Size Limits**: 50MB maximum to prevent memory exhaustion
- **Secure JSON Loading**: Validates content before parsing
- **Backup Mechanisms**: Creates backups before destructive operations

### Gemini CLI Usage Guidelines

**When to Use Scripts:**
- Task Master MCP tools are unavailable
- Need advanced filtering and search capabilities
- Generating task summaries or comparisons
- Recovering lost tasks from git history
- Performing orchestration workflow operations
- Headless automation with JSON output

**Best Practices:**
1. Use `--dry-run` flag for generation and sync scripts to preview changes
2. Use `--verbose` flag for debugging and monitoring
3. Use `--output-format json` for headless automation
4. Use `/checkpoint` for session state management
5. Review script output before applying destructive operations
6. Combine MCP tools with scripts for optimal workflow

**Integration with Google Search:**
```bash
# Research best practices
gemini -p "Search for branch alignment best practices and generate tasks"

# Research security patterns
gemini -p "Search for Python security validation patterns and update scripts"

# Research implementation approaches
gemini -p "Search for Git hook best practices and improve disable-hooks.sh"
```

**Documentation:**
- Complete usage guide: `scripts/README.md`
- Legacy documentation: `scripts/README_TASK_SCRIPTS.md`
- Shared utilities: `task_scripts/taskmaster_common.py`
2. **Reference files with @** - Leverage Gemini's file inclusion
3. **Save checkpoints** - Offer to save state after significant progress
4. **Monitor usage** - Remind users about `/stats` for long sessions
5. **Use Google Search** - Leverage search grounding for research

**Key Principle:** Focus on natural conversation. Task Master MCP tools work seamlessly with Gemini CLI's interface.

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
