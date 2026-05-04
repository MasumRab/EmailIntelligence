# Agent Rules Implementation — State Index

**Purpose:** Master index of branch-specific state files.
**How it works:** Each branch has its own `STATE_<branch>.md` file.

---

## Branch State Files

| Branch | State File | Status | Last Updated |
|--------|-----------|--------|--------------|
| `orchestration-tools` | [STATE_orchestration-tools.md](STATE_orchestration-tools.md) | Active — Phases 1-4 complete | 2026-04-14 |
| `main` | STATE_main.md | Not yet created | — |
| `scientific` | STATE_scientific.md | Not yet created | — |
| `taskmaster` | STATE_taskmaster.md | Not yet created | — |

---

## Creating a New Branch State File

```bash
cp docs/handoff/STATE_TEMPLATE.md docs/handoff/STATE_$(git branch --show-current).md
# Edit the header: replace <BRANCH_NAME> with your branch
```

Then update this index with the new entry.

---

## Quick Orientation

- **Starting fresh?** → See [README.md](README.md)
- **Session prompts?** → See [AMP_RUSH_SESSION_CREATION.md](AMP_RUSH_SESSION_CREATION.md)
- **Gate checks?** → See [MULTI_HANDOFF_EXECUTION_PROCESS.md](MULTI_HANDOFF_EXECUTION_PROCESS.md)
