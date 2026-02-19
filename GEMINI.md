# GEMINI.md - Project Context & Instructions

This file provides the necessary context and guidelines for working within the **Branch Alignment Tooling** workspace.

## Project Overview

**Branch Alignment Tooling** is a project focused on Git branch clustering, merge automation, and validation. It aims to streamline complex repository management by analyzing branch metrics and facilitating safe, automated merges.

- **Primary Language:** Python
- **Key Frameworks:** FastAPI, GitPython, Pydantic
- **Development Philosophy:** Task-Driven Development (TDD) using highly structured Markdown specifications.

### Critical Project Identity
**Note:** Do not confuse this project with "EmailIntelligence." While some historical documentation (like `ORACLE_RECOMMENDATION_TODO.md`) may suggest a pivot to EmailIntelligence, that proposal was **REJECTED**. The canonical identity remains **Branch Alignment Tooling**.

## Workspace Structure

- `tasks/`: **Canonical source** of task specifications. Each task follows a 14-section standard.
- `scripts/`: Extensive suite of utility scripts for task management, validation, and orchestration.
- `src/`: Core implementation of the branch alignment tools.
- `docs/`: Supporting documentation.
- `backups/` & `archive/`: Historical records; **not** canonical sources.

## Task Management Standards

All tasks must adhere to the **14-section standard** defined in `TASK_STRUCTURE_STANDARD.md`. This ensures consistency and prevents information loss during handoffs.

### Required Task Sections
1. Task Header (Status, Priority, Effort, etc.)
2. Overview/Purpose
3. Success Criteria (Detailed)
4. Prerequisites & Dependencies
5. Sub-subtasks Breakdown
6. Specification Details
7. Implementation Guide
8. Configuration Parameters
9. Performance Targets
10. Testing Strategy
11. Common Gotchas & Solutions
12. Integration Checkpoint
13. Done Definition
14. Next Steps

## Key Development Workflows

### Local vs Global Tooling
- **Local Tool (`taskmaster_cli.py`):** This is the **Fidelity Bridge**. It parses the Markdown files in `tasks/` and generates the `tasks.json` file. Use this to sync human-readable specs with structured data.
- **Global Extension (`tm` / `task-master`):** These are high-level orchestrators. They consume the `tasks.json` produced by the local tool to provide AI-assisted workflows (e.g., `tm next-task`).

### Task Discovery & Execution
Use the following scripts to navigate the task list:
- `python scripts/list_tasks.py`: List all active tasks.
- `python scripts/next_task.py`: Identify the next task to work on based on dependencies and priority.
- `python scripts/show_task.py <ID>`: Display detailed information for a specific task.
- `python scripts/task_summary.py`: Get a high-level overview of the workspace status.

### Markdown-First Workflow
1. **Edit:** Always modify the `.md` files in `tasks/` as the primary source of truth. Adhere to the 14-section standard.
2. **Sync:** Run `python taskmaster_cli.py parse-prd --input tasks/` to update the central `tasks.json`.
3. **Execute:** Use global `tm` commands or local `scripts/` to manage your progress.

### Building and Running
The project uses a FastAPI backend for core logic and CLI-like services.
- **Install Dependencies:** `pip install -r requirements.txt`
- **Run the Service:** `python src/main.py` (Starts FastAPI on port 8000 by default).
- **Run Tests:** `pytest tests/` (Use `--cov` for coverage reporting).
- **Linting:** `.flake8` and `.pylintrc` are provided. Run `flake8 .` or `pylint src/`.

## Coding Conventions
- **Style:** Google-style docstrings are preferred.
- **Validation:** Use Pydantic models for data validation and schema enforcement.
- **Git Operations:** Use `GitPython` or the project's internal `subprocess` wrappers in `src/git/` for reliable repository interaction.
- **Safety:** Always include timeouts in `subprocess` calls and handle edge cases like orphaned branches or non-existent repositories.

## Performance Targets
- **Single Branch Analysis:** Must complete in < 2 seconds.
- **Memory Usage:** < 50 MB per analysis call.
- **Scalability:** Must handle repositories with 10,000+ commits efficiently.

---
**Last Updated:** February 19, 2026
**Reference:** `PROJECT_IDENTITY.md`, `TASK_STRUCTURE_STANDARD.md`
