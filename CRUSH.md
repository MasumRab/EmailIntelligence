# Crush IDE-Specific Instructions

<<<<<<< HEAD
## Build/Lint/Test Commands
### Python Backend
- **Test all**: `pytest`
- **Test single file**: `pytest tests/test_file.py`
- **Test single function**: `pytest tests/test_file.py::TestClass::test_function`
- **Format**: `black .`
- **Lint**: `flake8 . && pylint python_backend src modules`
- **Type check**: `mypy .`
- **Dependency Update**: `python launch.py --update-deps`

### TypeScript/React Frontend
- **Build**: `npm run build` (from client/)
- **Lint**: `npm run lint` (from client/)
- **Dev server**: `npm run dev` (from client/)
=======
> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only Crush IDE-specific features and integrations.

## MCP Configuration for Crush IDE
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613

Configure Task Master MCP server in your Crush workspace configuration:

<<<<<<< HEAD
### TypeScript/React
- **Strict mode**: Enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- **JSX**: react-jsx transform
- **Imports**: `@/` (client src), `@shared/` (shared types)
- **Components**: `PascalCase` naming, default export functions
- **Styling**: Tailwind CSS
- **API**: Use client from `lib/api.ts`

## ⚠️ Critical Rules to Follow
- Rigorously adhere to existing project conventions when reading or modifying code.
- Analyze surrounding code, tests, and configuration first before making changes.
- Mimic code style, framework choices, naming conventions, typing, and architectural patterns.
- NEVER assume a library/framework is available without verifying its established usage.
- Check imports, configuration files, or neighboring files to confirm usage before employing any library.
- Follow existing code style and structure strictly.
- Use existing libraries and utilities already established in the project.
- Follow existing architectural patterns.
- Understand local context (imports, functions/classes) to ensure changes integrate naturally.
- Make changes that are idiomatic to the existing codebase.
- Check existing dependencies before adding new libraries.
- Follow security best practices.

- No circular dependencies
- No hard-coded paths/secrets
- Strict typing (full annotations)
- Consistent naming conventions
- Security: Never expose or log sensitive data
- Global State: Use dependency injection over global state
=======
```json
{
  "extensions": {
    "task-master-ai": {
      "enabled": true,
      "mcpServer": {
        "command": "npx",
        "args": ["-y", "task-master-ai"]
      }
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## Crush IDE-Specific Features

### Workspace Integration

- Built-in terminal with task management
- File explorer with MCP tool integration
- Split editor windows for parallel task work
- Integrated debugging and linting

Both `AGENTS.md` and `CRUSH.md` are auto-loaded in Crush workspace context.

### File Management in Crush

```bash
# Direct file operations from integrated terminal
task-master show 1.2    # View task details
task-master update-subtask --id=1.2 --prompt="progress notes"

# File context available via workspace explorer
# Edit files directly in Crush editor (superior UX to terminal)
```

### Inline AI Assistance

- Hover over code for explanations
- Right-click → "Analyze with Task Master"
- Inline suggestions for code improvements

## Important Differences from Other Agents

### Integrated Development Environment
Crush provides a unified IDE experience - no need for separate terminal windows.

### Visual File Tree
Navigate repository structure with visual file explorer (more efficient than `ls`/`find`).

### Real-time Collaboration
Crush supports shared workspaces - multiple developers on same project.

### No Separate Configuration Files
Settings managed within Crush IDE GUI, not via `.crush/` directories.

## Recommended Model Configuration

For Crush IDE users:

```bash
# Configure via Crush IDE settings panel
task-master models --set-main <your-preferred-model>
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback <backup-model>
```

## Your Role with Crush IDE

As a Crush IDE assistant with Task Master:

1. **Leverage IDE features** - Use visual file explorer, split editors, integrated terminal
2. **Use MCP tools naturally** - Available through IDE context menu and inline suggestions
3. **Manage tasks in editor** - View task details directly in Crush
4. **Workspace coordination** - Facilitate multi-developer workflows
5. **Real-time feedback** - Provide immediate code analysis and suggestions

**Key Principle:** Crush IDE provides a complete development environment. Task Master integrates seamlessly for task-driven development workflows.

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
