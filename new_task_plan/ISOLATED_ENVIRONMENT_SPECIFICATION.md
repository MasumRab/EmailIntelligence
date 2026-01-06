# Isolated Task Environment Specification

**Purpose:** Design and implement a clean, isolated task environment in `.taskmaster/tasks/` that supports parallel agent execution through self-contained task specifications, standardized script references, and shared findings memory.

**Scope:** 
- Structure of the `.taskmaster/tasks/` directory.
- Migration of existing tasks to standardized `.md` formats.
- Integration of script execution references within tasks.
- Shared memory management via `.agent_memory/` for findings and state.

**Goal:** Enable any agent to pick up a `task-XXX.md` file and execute it independently with all necessary context, script pointers, and access to previous findings.

**Version:** 2.2  
**Created:** January 6, 2026  

---

## Architecture Overview: The Clean Tasks Directory

The core of the system is a flattened, high-signal `tasks/` directory where each file represents an executable unit of work.

### 1. Directory Structure

```
.taskmaster/
├── tasks/                        (CLEAN TASKS AREA)
│   ├── tasks.json                (Master task database/index)
│   ├── task-001.md               (Foundation Framework)
│   ├── task-002.md               (Validation Framework)
│   ├── task-021.md               (Clustering System)
│   └── ...                       (All main tasks as .md)
│
├── .agent_memory/                (SHARED FINDINGS & STATE)
│   ├── session_log.json          (Persistent activity log)
│   ├── findings/                 (Domain-specific discoveries)
│   └── memory_api.py             (Interface for agents)
│
└── scripts/                      (STANDARDIZED TOOLS)
    ├── list_tasks.py
    ├── show_task.py
    └── ...
```

---

## Component Design

### 1. Standardized Task Specification (task-XXX.md)

Each task file must follow a strict template that includes script references and memory integration points:

```markdown
# Task ID: task-XXX

## 1. Context & Objectives
- **Initiative:** [Initiative Name]
- **Status:** [Status]
- **Goal:** [Clear statement of intent]

## 2. Dependencies & Prerequisites
- Pre-requisite Tasks: [task-YYY]
- Required State: [Findings required from .agent_memory]

## 3. Script References (Execution)
Standardized commands for this task:
- `python scripts/show_task.py XXX`
- `python scripts/expand_subtasks.py --task XXX`

## 4. Implementation Guide
[Detailed steps for an agent to follow]

## 5. Memory & Findings sharing
- **Input Memory:** Refer to `findings/phase_XXX_summary.json`
- **Output Memory:** Log discoveries to `.agent_memory/findings/` using `memory_api.py`

## 6. Verification & Done Definition
- [ ] Logic check
- [ ] Test execution
- [ ] Documentation updated
```

### 2. Script References & Tooling

Tasks are "live" documents. They contain direct references to scripts that the agent should run to manage the task life cycle.
- **Discovery:** `list_tasks.py`
- **Retrieval:** `show_task.py`
- **Expansion:** `expand_subtasks.py`
- **Sync:** `regenerate_tasks_from_plan.py`

### 3. Memory Management for Findings Sharing

To ensure agents don't work in isolation without knowing what others found:
- **Findings Storage:** Located in `.agent_memory/findings/`.
- **Finding Index:** A central map linking task IDs to specific finding files.
- **Sharing Protocol:** Agents MUST check relevant finding files before starting a task and MUST update finding files upon completion.

---

## Implementation Roadmap (First Goal)

### Phase 1: Task Standardization (Immediate)
1. Consolidate all scattered task descriptions in `new_task_plan/` and `tasks/`.
2. Generate clean `task-XXX.md` files for all primary tasks.
3. Ensure each file has the **Script References** section populated.

### Phase 2: Memory Integration
1. Link `task-XXX.md` "Required State" section to existing finding files in `.agent_memory/`.
2. Establish a pattern for agents to log task-specific findings during execution.

### Phase 3: Directory Cleanup
1. Move historical and planning artifacts to `archive/`.
2. Ensure the `tasks/` directory contains only active `.md` files and the `tasks.json` master file.

---

## Success Metrics

1. **Self-Sufficiency:** An agent can complete a task using only the `task-XXX.md` file and the referenced scripts/memory.
2. **Finding Persistence:** Discoveries made in Task A are correctly utilized in dependent Task B via the findings shared memory.
3. **Execution Clarity:** Standardized script references reduce command guessing by >90%.