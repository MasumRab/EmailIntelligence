# Branch Sync Architecture

**Last updated:** 2026-06-08
**Maintained on:** `orchestration-tools` branch
**Referenced from:** `AGENTS.md`

## Intended Architecture

| Branch | Purpose | Should Contain | Should NOT Contain |
|---|---|---|---|
| `main` | Application code | `src/core/`, `modules/`, `setup/`, `client/`, `backend/`, `tests/`, `.github/workflows/` | Orchestration scripts, agent configs, NLP models |
| `scientific` | Application + research | Everything in `main` + `models/`, NLP-specific modules, research features | Orchestration scripts, agent configs |
| `orchestration-tools` | Shared tooling | `scripts/`, `setup/`, `docs/`, lint configs, git hooks, agent configs, `src/analysis/`, `src/resolution/` | Application modules, data files, NLP models |

### Sync Flow

```
orchestration-tools (shared tooling)
    ↓ git hooks / manual sync
main (app code) ←→ scientific (app + research)
```

- `orchestration-tools` syncs setup tooling, hooks, and configs INTO other branches
- `main` and `scientific` share app code; scientific adds NLP/research on top
- `orchestration-tools` does NOT merge with app branches — it distributes tooling

## Current Drift Status

### Last Cross-Branch Merges

| Merge | Date | Gap |
|---|---|---|
| main → scientific | Nov 1, 2025 | **7 months** |
| main → orchestration-tools | Nov 8, 2025 | **7 months** |
| scientific → orchestration-tools | Oct 27, 2025 | **7+ months** |

No cross-branch merges in the last 30 days.

### Divergence Metrics (as of 2026-06-08)

| Metric | main ↔ scientific | main ↔ orchestration-tools |
|---|---|---|
| Commits ahead of main | 1,392 | 805 |
| Commits behind main | 17 | 39 |
| `src/` files differing | 156 | 207 |
| `modules/` files differing | 31 | 44 |
| `.github/` files differing | 10 | 41 |

### Known Drift Issues

| Issue | Branches | Severity | Notes |
|---|---|---|---|
| `src/cli/commands/` deleted | scientific | CRITICAL | 8 CLI command files missing |
| `src/context_control/` deleted | scientific | CRITICAL | 12+ context control files missing |
| `modules/new_ui/` deleted | both | HIGH | 6 new UI files missing |
| `modules/auth/`, `dashboard/`, `email/` etc. deleted | orchestration-tools | HIGH | 35 module files missing (expected per scope) |
| `src/backend/data/` deleted | orchestration-tools | MEDIUM | Data files missing |
| CI workflows diverged | both | MEDIUM | `checkout@v6` vs `@v4`, missing gemini workflows |
| `src/` content present | orchestration-tools | ⚠️ SCOPE VIOLATION | `orchestration_branch_scope.md` says no `src/` but 11 directories exist. Needs review — may be necessary for current work. |

### Justifiable Differences

| Difference | Branch | Justification |
|---|---|---|
| `models/` (topic model, tokenizer, vocab) | scientific | NLP research models — scientific-only |
| `src/analysis/` (conflict analyzer, constitutional checker) | orchestration-tools | Shared analysis tooling — correct home |
| `src/resolution/` (auto_resolver) | orchestration-tools | Shared resolution tooling — correct home |
| `.agents/`, `.claude/`, `.cline/`, `.codex/`, `.cursor/` | orchestration-tools | Agent configs — correct home |
| `modules/*.sh` (branch.sh, config.sh, safety.sh) | orchestration-tools | Orchestration shell scripts — correct home |

## Sync Rules

### Must Stay Aligned Across main ↔ scientific

- `src/core/` — shared engine code
- `src/backend/python_backend/` — shared API backend
- `modules/auth/`, `modules/email/`, `modules/dashboard/` — shared app modules
- `setup/` — shared launch and config
- `.github/workflows/` — CI/CD pipelines
- `.gitignore`, `.gitattributes` — repo config

### Must Stay Aligned Across orchestration-tools → main/scientific

- `setup/launch.py`, `setup/launch.sh` — shared launcher
- `setup/pyproject.toml`, `setup/requirements*.txt` — shared deps
- `scripts/` — orchestration scripts
- `.flake8`, `.pylintrc`, `.pre-commit-config.yaml` — lint configs
- `.github/workflows/` — CI pipelines

### Allowed to Drift

- `models/` — scientific-only NLP models
- `src/analysis/`, `src/resolution/` — orchestration-tools-only tooling
- Agent config directories (`.agents/`, `.claude/`, etc.) — orchestration-tools-only
- Branch-specific docs and reports

## Update Process

When making changes that affect branch alignment:
1. Update the drift status table above
2. Update the last merge dates if a merge occurs
3. Add new justifiable differences if intentional drift is introduced
4. Run `git diff --stat origin/main origin/scientific -- src/ modules/ setup/ .github/` to refresh metrics
