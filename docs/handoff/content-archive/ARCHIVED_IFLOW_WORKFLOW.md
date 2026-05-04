# iFlow CLI Workflow Patterns

**Archived from:** IFLOW.md git history (EmailIntelligenceGem worktree)  
**Date:** 2026-04-09  
**Status:** Reference only — iFlow CLI not actively used on current branch

---

## iFlow CLI Core Mandates

### Conventions

1. **Rigorously adhere to existing project conventions**
   - Analyze surrounding code, tests, and configuration first
   - Mimic code style, framework choices, naming conventions

2. **Library/Framework Verification**
   - NEVER assume a library/framework is available without verifying
   - Check imports, configuration files, or neighboring files

---

## Session Tracking

### Directory Structure

```
backlog/sessions/
├── README.md
├── IFLOW-20251031-001.md
├── IFLOW-20251101-001.md
├── IFLOW-20251102-001.md
├── IFLOW-20251104-001.md
└── IFLOW-20251112-ACHIEVEMENTS.md
```

### Naming Convention

```
IFLOW-YYYYMMDD-XXX.md
```

Where:
- `YYYYMMDD` — Session date
- `XXX` — Sequential number (001, 002, etc.)

### Session File Template

```markdown
# Session: [Brief Description]

**Date:** YYYY-MM-DD
**Type:** [Development | Bugfix | Research | Planning]

## Objectives
- [ ] Objective 1
- [ ] Objective 2

## Progress
- Item 1: [Status]
- Item 2: [Status]

## Decisions Made
1. Decision 1 — Reason: ...

## Next Steps
- [ ] Next step for next session
```

---

## iFlow CLI Software Engineering Workflow

### 5-Phase Process

```
1. UNDERSTAND
   └── Read code, tests, configuration
   └── Identify surrounding context

2. PLAN
   └── Design solution approach
   └── Document in session file

3. IMPLEMENT
   └── Write code following conventions
   └── Use existing patterns

4. VERIFY (Tests)
   └── Write/update tests
   └── Run test suite

5. VERIFY (Standards)
   └── Check linting (flake8, mypy)
   └── Check formatting (black)
   └── Update documentation
```

---

## Tools Available

| Tool | Purpose |
|------|---------|
| `read_file` | Read file contents |
| `write_file` | Create new files |
| `replace` | Edit existing files |
| `search_file_content` | Search within files |
| `glob` | Find files by pattern |
| `run_shell_command` | Execute shell commands |
| `todo_write/todo_read` | Task tracking |

---

## Node-Based Workflow Engine

### Architecture

EmailIntelligence includes a node-based workflow system inspired by ComfyUI/Stable Diffusion:

```
┌─────────────────────────────────────────────────────┐
│                 Workflow Engine                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│   ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐  │
│   │ Input │───▶│ Node1 │───▶│ Node2 │───▶│ Output│  │
│   │ (Email)│    │(Parse)│    │(NLP)  │    │(Result)│ │
│   └───────┘    └───────┘    └───────┘    └───────┘  │
│                                                      │
│   Extension System: Plug-and-play modules            │
│   Filtering: Conditional node execution              │
│   Module System: Reusable workflow components         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Input nodes | `backend/node_engine/inputs/` | Email source connectors |
| Processing nodes | `backend/node_engine/processors/` | NLP analysis steps |
| Output nodes | `backend/node_engine/outputs/` | Result handlers |
| Extensions | `modules/` | Plugin functionality |

---

## Related Documentation

- `docs/handoff/content-archive/ARCHIVED_AI_MODELS_SETUP.md` — AI models organization
- `backlog/sessions/IFLOW-*.md` — Historical session files
- `docs/source-of-truth/project/PROJECT_SUMMARY.md` — Project overview
