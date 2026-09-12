# Gemini CLI-Specific Instructions

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the shared Task Master workflow and project baseline. This file keeps Gemini-specific runtime and workflow guidance at the project root as a reviewed Tier 2 context file.

## Runtime on This Branch

- Project config lives in `.gemini/settings.json`.
- The current Gemini runtime loads `AGENTS.md` as the shared baseline via `"contextFileName": "AGENTS.md"`.
- Keep `GEMINI.md` at the project root so Gemini-specific behavior is preserved instead of being collapsed into shared AGENTS content.

## MCP Configuration

Current project configuration:

```json
{
  "contextFileName": "AGENTS.md",
  "mcpServers": {
    "task-master-ai": {
      "command": "npm",
      "args": ["exec", "task-master-ai"]
    }
  }
}
```

API keys are still configured via `task-master models --setup` or environment variables, not by hard-coding secrets into repo files.

## Gemini CLI-Specific Features

### Session Management

Built-in session commands:

- `/chat` — start a new conversation while keeping context
- `/checkpoint save <name>` — save session state
- `/checkpoint load <name>` — resume saved state
- `/memory show` — inspect loaded context

For this repo, checkpoints work best when paired with `docs/handoff/STATE.md` so long-running handoffs can be resumed cleanly.

### Headless Mode for Automation

Non-interactive mode is useful for quick lookups and scripted checks:

```bash
gemini -p "What's the next task?"
gemini -p "List pending handoff phases" --output-format json
gemini -p "Summarize this diff" --output-format stream-json
```

### Research and Grounding

Gemini can use Google Search grounding for:

- official documentation lookups
- implementation pattern research
- security or dependency checks
- validating tool behavior before changing configs

### File-Oriented Workflow

- Use `@path/to/file` references when asking Gemini to focus on specific files.
- Keep the shared baseline in `AGENTS.md`, then use this file for Gemini-only workflow differences.
- The Jules backlog template content lives in `.gemini/JULES_TEMPLATE.md`; keep it separate from the live root guidance.

## Important Differences from Other Agents

### No Custom Project Slash Commands

Gemini has built-in slash commands, but this repo does not rely on custom project slash-command files the way some other agents do.

### MCP Permissions Live in Settings

Security and server wiring are managed through `.gemini/settings.json`, not through `.mcp.json`.

### Shared Baseline + Tier 2 Split

On this branch, Gemini uses the shared baseline from `AGENTS.md`, but `GEMINI.md` still matters because it captures Gemini-specific workflow guidance that should remain easy to discover at the root.

## Recommended Usage

As a Gemini assistant in this repo:

1. Use `AGENTS.md` for shared project rules and commands.
2. Use `GEMINI.md` for Gemini-only behavior, especially checkpoints, grounding, and file-oriented prompting.
3. Use `docs/handoff/STATE.md` as the authoritative resume log for this cleanup work.
4. Prefer official docs or live code evidence when tool behavior is uncertain.

**Key Principle:** Keep shared rules centralized, but keep Gemini-specific workflow behavior explicit at the root.
