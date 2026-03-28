# Qwen CLI-Specific Instructions

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only Qwen CLI-specific features and integrations.

## MCP Configuration for Qwen CLI

Configure Task Master MCP server in `.qwen/settings.json` or `~/.qwen/config.json`:

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

## Qwen CLI-Specific Features

### Session Management

Built-in session commands:

- `/chat` - Start new conversation while keeping context
- `/context` - View current loaded context
- `/model` - Switch between Qwen models
- `/history` - View conversation history

Both `AGENTS.md` and `QWEN.md` are auto-loaded on every Qwen CLI session.

### Headless Mode for Automation

Non-interactive mode for scripts:

```bash
# Simple text response
qwen "What's the next task?"

# Stream output for long operations
qwen --stream "Expand all tasks"

# Set specific model
qwen --model qwen-plus "Analyze this code"
```

### Token Usage Monitoring

```bash
# In Qwen CLI session
/usage

# Shows: token usage, cost estimation, request count
```

### Qwen-Specific Capabilities

- Multi-turn conversations with context retention
- Code generation and analysis
- Math and reasoning tasks
- Chinese language support

## Important Differences from Other Agents

### No Tool Allowlist
Qwen manages permissions at the MCP level, not via agent configuration.

### Session Persistence
Each session maintains context automatically. Use `/context` to verify loaded files.

### Configuration Files
- Global: `~/.qwen/config.json` or `~/.qwen/settings.json`
- Project: `.qwen/settings.json`
- **Not**: `.mcp.json` (that's for Claude Code)

## Recommended Model Configuration

For Qwen CLI users:

```bash
# Set Qwen as primary model
task-master models --set-main qwen-plus
task-master models --set-fallback qwen-turbo

# Optional: Use Perplexity for research
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
```

## Your Role with Qwen CLI

As a Qwen CLI assistant with Task Master:

1. **Use MCP tools naturally** - They integrate transparently in conversation
2. **Reference context** - Use `/context` to verify what's loaded
3. **Monitor usage** - Remind users about `/usage` for long sessions
4. **Leverage reasoning** - Use Qwen's strength in multi-step reasoning
5. **Multi-language support** - Can explain concepts in multiple languages

**Key Principle:** Focus on natural conversation. Task Master MCP tools work seamlessly with Qwen CLI's interface.

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
