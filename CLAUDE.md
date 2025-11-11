# Claude AI Assistant - Context & Guidelines

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only Claude-specific features and integrations.

## MCP Configuration for Claude Code/Claude AI

Configure Task Master MCP server in `.mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here",
        "PERPLEXITY_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## Claude-Specific Features

### Context Management

- Use `/clear` between different tasks to maintain focus
- AGENTS.md and CLAUDE.md are auto-loaded for context
- Use `task-master show <id>` to pull specific task context when needed

### Tool Allowlist

Add to `.claude/settings.json`:

```json
{
  "allowedTools": [
    "Edit",
    "Bash(task-master *)",
    "Bash(git commit:*)",
    "Bash(git add:*)",
    "Bash(npm run *)",
    "mcp__task_master_ai__*"
  ]
}
```

### Custom Slash Commands

Create `.claude/commands/taskmaster-next.md`:

```markdown
Find the next available Task Master task and show its details.

Steps:
1. Run `task-master next` to get the next task
2. If a task is available, run `task-master show <id>` for full details
3. Provide a summary of what needs to be implemented
```

### Parallel Development with Git Worktrees

```bash
# Create worktrees for parallel task development
git worktree add ../project-auth feature/auth-system
git worktree add ../project-api feature/api-refactor

# Run Claude in each worktree
cd ../project-auth && claude    # Terminal 1: Auth work
cd ../project-api && claude     # Terminal 2: API work
```

## Important Differences from Other Agents

### Direct File Access
Claude Code can directly edit files with native Edit tool (superior to sed/manual editing).

### Git Integration
Native git commands - no special syntax needed.

### Session Persistence
Use `/clear` for context isolation between tasks. Multiple Claude Code windows can work on different worktrees simultaneously.

## Recommended Model Configuration

For Claude users:

```bash
# Set Claude as primary model
task-master models --set-main claude-3-5-sonnet-20241022
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback claude-3-5-haiku-20241022
```

## Your Role with Claude Code

As a Claude assistant with Task Master:

1. **Use MCP tools naturally** - They integrate transparently via `.mcp.json`
2. **Direct file editing** - Use Edit tool for clean, efficient changes
3. **Context isolation** - Use `/clear` between tasks to stay focused
4. **Custom commands** - Leverage `.claude/commands/` for repeated workflows
5. **Parallel worktrees** - Manage multiple features in separate terminals

**Key Principle:** Use native Claude capabilities (Edit, file reading) combined with Task Master MCP for comprehensive task management.

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
