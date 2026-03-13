# tasks/ AGENTS.md

**Task management workspace** — contains all project tasks as markdown files

## OVERVIEW
Task Master AI's task repository. 100+ markdown files defining project work items. Tasks follow 14-section standard defined in `../TASK_STRUCTURE_STANDARD.md`.

## FILES
| Pattern | Count | Purpose |
|---------|-------|---------|
| `task_###.md` | ~28 | Main tasks |
| `task_###.#.md` | ~70 | Subtasks |
| `.ck/` | - | Code index (ignore) |

## DOCUMENTATION TO CONSULT

| For | Consult |
|-----|---------|
| Task structure | `../TASK_STRUCTURE_STANDARD.md` |
| CLI commands | Root `AGENTS.md` |
| PRD methodology | PRD METHODOLOGY section |
| Testing/fidelity | TESTING, ROUND-TRIP sections |
| Enhancement scripts | PRD ENHANCEMENT section |
| Task scripts | `scripts/README.md` |

### Documentation Categories

| Category | Location | Purpose |
|----------|----------|--------|
| **Workflow** | `docs/COMPLETE_TASK_WORKFLOW.md` | End-to-end task management |
| **Round-trip** | `docs/ROUND_TRIP_*.md` | Fidelity testing guides |
| **Enhancement** | `docs/*_IMPROVEMENTS_*.md` | Task spec improvements |
| **Orchestration** | `docs/branch_alignment/` | Branch coordination |
| **Archive** | `docs/archive/` | Deprecated - 19 files, old branch refs (ws1-, ws2-), use only if historical context needed |

### Quick Access
```
Quick question → This file (tasks/AGENTS.md)
CLI usage → Root AGENTS.md
Deep dive → docs/ROUND_TRIP_SCRIPTS_SUMMARY.md
```

| For | Consult |
|-----|---------|
| Task structure | `../TASK_STRUCTURE_STANDARD.md` |
| CLI commands | Root `AGENTS.md` |
| Task format | Any `task_001.md` reference |

## TASK WORKFLOW

| Action | Command |
|--------|---------|
| List tasks | `task-master list` |
| Next task | `task-master next` |
| Show details | `task-master show <id>` |
| Update status | `task-master set-status --id=<id> --status=done` |
| Expand task | `task-master expand --id=<id> --research` |
## PRD METHODOLOGY

### Creating Tasks from PRD
1. Write PRD → Create `docs/prd.txt` or `.md` with feature requirements
2. Generate tasks → `task-master parse-prd docs/prd.txt --research`
3. Review output → Always check generated tasks before accepting
4. Append mode → `task-master parse-prd --append` adds to existing tasks

### PRD Format
- Plain text (`.txt`) or Markdown (`.md`)
- Include: Overview, Success Criteria, Dependencies, Subtasks
## PRD ENHANCEMENT & REVERSE ENGINEERING

### PRD Enhancement
Improves task files for better PRD generation accuracy.

| Script | Purpose |
|--------|--------|
| `enhance_task_specifications_for_prd_accuracy.py` | Enhances tasks for PRD output |
| `validate_task_specifications.py` | Validates against enhanced template |

```bash
python scripts/enhance_task_specifications_for_prd_accuracy.py
```

### Reverse Engineering PRD
Generate PRD from task files (Tasks → PRD).

| Script | Quality | Use Case |
|--------|---------|----------|
| `perfect_fidelity_reverse_engineer_prd.py` | Highest | Production PRD |
| `ultra_enhanced_reverse_engineer_prd.py` | High | Advanced features |

```bash
python scripts/perfect_fidelity_reverse_engineer_prd.py -i tasks/ -o prd.md
```

### Round-Trip
```
Tasks → [Reverse Engineer] → PRD → [parse-prd] → Tasks
```
Use `test_round_trip_enhanced.py` to validate fidelity.

## TESTING METHODOLOGY

### Round-Trip Fidelity Testing
Validates: Tasks → PRD → Tasks preserves information fidelity.

| Script | Purpose |
|--------|--------|
| `scripts/test_round_trip.py` | Basic round-trip test |
| `scripts/test_round_trip_enhanced.py` | Enhanced with empty tasks.json |
| `scripts/perfect_fidelity_validator.py` | Strict fidelity validation |

### Running Tests
```bash
python scripts/test_round_trip_enhanced.py
```

## EMPTY TASKS.JSON

### Intentional Design
`tasks.json` is intentionally kept empty (`[]`).

**Why:**
- Canonical source: `tasks/*.md` files are the source of truth
- Round-trip testing only: Empty tasks.json used only for fidelity validation
- JSON is derived: tasks.json regenerated from markdown via `parse-prd`

### Workflow
1. Edit markdown in `tasks/*.md`
2. Run `python taskmaster_cli.py parse-prd --input tasks/` to sync
3. CLI tools consume the generated tasks.json

### NEVER
- DO NOT manually edit tasks.json
- DO NOT use tasks.json as source of truth
- DO NOT commit non-empty tasks.json unless for testing


## CHANGING TASKS

1. **Add new task** → `task-master add-task --prompt="..."`
2. **Modify task** → Edit markdown directly, then `task-master generate`
3. **Change structure** → Modify `../TASK_STRUCTURE_STANDARD.md`
4. **Dependency mgmt** → `task-master add-dependency --id=<id> --depends-on=<id>`

## ANTI-PATTERNS
- DO NOT edit `tasks.json` manually — use CLI
- DO NOT skip `--research` for complex expansions
- DO NOT parse PRD without reviewing output first

## NOTES
- Tasks in `.ck/` are code index artifacts — ignore
- Main tasks: `task_NNN.md` (no decimal)
- Subtasks: `task_NNN.M.md` (decimal = subtask)
