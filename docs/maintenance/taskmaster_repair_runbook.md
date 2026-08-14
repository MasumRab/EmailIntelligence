# Taskmaster Repair Runbook: Task Management System Recovery

This runbook provides a structured approach for repairing, maintaining, and troubleshooting the Task Master AI integration. It covers task database integrity, file synchronization, and MCP connectivity.

---

## 1. Task Database Integrity

Task Master stores the primary state of all tasks in a JSON database.

### Core File: `tasks.json`
The source of truth is: `.taskmaster/tasks/tasks.json`
**Warning:** Never manually edit `tasks.json` while a Task Master process or MCP session is active. Manual edits should be a last resort.

### Repairing `tasks.json` Corruption
If `task-master list` or other commands fail due to JSON parsing errors:
1.  **Validate JSON:** Run `python3 -m json.tool .taskmaster/tasks/tasks.json` to identify syntax errors.
2.  **Restore from Backup:** If the file is unrecoverable, check if your version control has a clean previous state.
3.  **Regenerate from Markdown (Partial Recovery):** If `tasks.json` is lost but `.taskmaster/tasks/*.md` files exist, you may need to re-initialize and re-parse the PRD, as there is currently no direct "reverse sync" from Markdown to JSON.

---

## 2. File Synchronization & Dependencies

Task Master maintains markdown files for each task to provide human-readable context.

### Out-of-Sync Markdown Files
If the `.md` files in `.taskmaster/tasks/` do not match the state in `tasks.json`:
```bash
task-master generate
```
This command regenerates all task markdown files based on the current state of `tasks.json`.

### Dependency Issues
If tasks have circular dependencies or invalid parent-child relationships:
```bash
task-master validate-dependencies
```
If issues are found, use `task-master fix-dependencies` (if available) or manually correct the `dependencies` or `parentId` fields using `task-master update-task`.

---

## 3. MCP & AI Model Troubleshooting

Task Master often runs as an MCP (Model Context Protocol) server.

### MCP Connection Failures
If Claude Code or another client cannot connect to the Task Master MCP:
1.  **Check `.mcp.json`:** Verify the command and environment variables.
    ```json
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": { ... }
    }
    ```
2.  **Test CLI Directly:** Run `task-master help` in the terminal. If the CLI fails, the MCP will also fail.
3.  **Debug Mode:** Use the `--mcp-debug` flag when starting your AI agent session.

### AI Model Failures
If `expand` or `research` commands fail:
1.  **Verify API Keys:** Ensure the relevant keys (e.g., `ANTHROPIC_API_KEY`, `PERPLEXITY_API_KEY`) are set in your `.env` or environment.
2.  **Check Model Config:** Run `task-master models` to see current settings.
3.  **Reset Config:** Use `task-master models --setup` to reconfigure the models interactively.

---

## 4. Maintenance Checklist

### Regular Health Check
- [ ] Run `task-master list` to ensure the database is readable.
- [ ] Run `task-master validate-dependencies` to check for logic issues.
- [ ] Ensure all API keys in `.env` are valid and not expired.

### Post-Repair Validation
- [ ] `task-master generate` completes without errors.
- [ ] Task status changes correctly reflect in both `tasks.json` and the corresponding `.md` file.
- [ ] AI-powered commands (like `task-master show <id>`) return coherent information.
