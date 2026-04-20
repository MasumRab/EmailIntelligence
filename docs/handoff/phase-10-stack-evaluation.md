# Phase 10 Appendix: Branch-Dependent Stack Evaluation

**Purpose:** Fine-grained rule-by-rule gap analysis of agentrulegen.com template recommendations against `.ruler/AGENTS.md`, specific to the tech stack present on the current branch.

**Generated for:** `orchestration-tools` branch
**Detection script:** `bash scripts/detect-branch-stack.sh`

---

## How to Use This Document

1. Run `bash scripts/detect-branch-stack.sh` to get the template recommendations for your branch
2. For each ✅ template, use the evaluation tables below
3. For each rule, check the **Verdict** column — only add rules marked **WORTH ADDING**
4. If on a different branch, regenerate by running the detection script and comparing against that branch's `.ruler/AGENTS.md`

---

## Current `.ruler/AGENTS.md` Coverage Summary (57 lines)

| Section | Lines | Content |
|---------|-------|---------|
| Project Overview | 2 | Python/FastAPI + React/TypeScript, Python 3.11+ |
| Branch Context | 1 | orchestration-tools focus, scientific branch reference |
| Code Conventions | 4 | Python/TS/Shell/Test conventions |
| Build Commands | 4 | launch.py, npm, pytest, flake8/mypy/pylint |
| Key Directories | 17 | All src/ subdirs, cli/, setup/, client/, modules/, scripts/, etc. |
| Task Management | 8 | Task Master workflow |
| Critical Rules | 6 | Security, eval/exec, DI, type hints, verify script |

---

## Template 1: `python-fastapi` — PARTIAL MATCH

FastAPI is in `requirements.txt` but **no SQLAlchemy usage** and **no async route handlers** exist in `src/` on this branch. The backend code lives on `scientific`. Only rules applicable to CLI/interfaces code apply.

| # | Template Rule | In AGENTS.md? | Applicable? | Verdict | Rationale |
|---|---------------|---------------|-------------|---------|-----------|
| 1 | Use Python 3.12+ type hints on all signatures | ✅ Yes (line 10) | Yes | ALREADY COVERED | "type hints required" |
| 2 | Run `mypy --strict` or `pyright` in CI | ✅ Yes (line 19) | Yes | ALREADY COVERED | "mypy ." in Lint |
| 3 | Use f-strings for interpolation | ❌ No | Yes | NOT WORTH ADDING | Agent infers from Python version |
| 4 | Use `pathlib.Path` for file operations | ❌ No | Yes | WORTH ADDING | Prevents hardcoded paths, reinforces Critical Rule |
| 5 | Format with `ruff format` / Lint with `ruff check` | ❌ No | No | NOT APPLICABLE | Project uses Black + flake8 (in .flake8, setup.cfg) |
| 6 | Keep route handlers under 15 lines | ❌ No | No | NOT APPLICABLE | No route handlers on this branch |
| 7 | Group routes with `APIRouter` | ❌ No | No | NOT APPLICABLE | No routes on this branch |
| 8 | Declare `response_model=` on route decorators | ❌ No | No | NOT APPLICABLE | No routes on this branch |
| 9 | Use `Annotated` for dependency injection | ❌ No | Partial | NOT WORTH ADDING | DI rule exists; FastAPI-specific syntax not needed here |
| 10 | Use `async def` for I/O functions | ❌ No | Yes | NOT WORTH ADDING | Only 1 async file; agent infers from code |
| 11 | Never call blocking code in async context | ❌ No | Minimal | NOT WORTH ADDING | Minimal async code on this branch |
| 12 | Use `AsyncSession` with `expire_on_commit=False` | ❌ No | No | NOT APPLICABLE | No SQLAlchemy on this branch |
| 13 | Alembic migrations | ❌ No | No | NOT APPLICABLE | No database on this branch |
| 14 | Custom exception classes for HTTP errors | ❌ No | No | NOT APPLICABLE | No HTTP error handling on this branch |
| 15 | Hash passwords with `passlib[bcrypt]` | ❌ No | No | NOT APPLICABLE | No auth on this branch |
| 16 | Configure CORS — never `["*"]` with credentials | ❌ No | No | NOT APPLICABLE | No web server on this branch |
| 17 | Use `pytest-asyncio` with `asyncio_mode = "auto"` | ❌ No | Yes | NOT WORTH ADDING | Already in pytest.ini via markers; agent infers |
| 18 | Use `httpx.AsyncClient` for async route tests | ❌ No | No | NOT APPLICABLE | No route tests on this branch |

**Summary:** 2 covered, 1 worth adding (`pathlib.Path`), 15 not applicable or not worth adding.

---

## Template 2: `git-workflow` — FULL MATCH

78 shell scripts, multi-branch project with branch.sh, safety.sh, distribute.sh. Git workflow rules are directly relevant.

| # | Template Rule | In AGENTS.md? | Applicable? | Verdict | Rationale |
|---|---------------|---------------|-------------|---------|-----------|
| 1 | Branch naming: `feature/AGE-123-desc` | ❌ No | Yes | WORTH ADDING | Multi-branch project; agent needs to know naming convention |
| 2 | Delete branches after merging | ❌ No | Yes | NOT WORTH ADDING | Agent infers; also complex — some branches are long-lived |
| 3 | Conventional Commits: `<type>(<scope>): <subject>` | ❌ No | Yes | WORTH ADDING | Not in any config file; agent cannot infer commit format |
| 4 | Commit types: feat, fix, docs, style, refactor... | ❌ No | Yes | ALREADY COVERED (by #3) | Part of Conventional Commits |
| 5 | Subject line: imperative, <72 chars, no period | ❌ No | Yes | ALREADY COVERED (by #3) | Part of Conventional Commits |
| 6 | Never commit generated files, secrets, node_modules | ✅ Partial | Yes | ALREADY COVERED | "NEVER commit secrets or API keys" + .gitignore |
| 7 | Rebase feature branches before PR | ❌ No | Yes | NOT WORTH ADDING | Git strategy decision — not essential for agent rules |
| 8 | Use `pre-commit` hooks for linting | ❌ No | Yes | NOT WORTH ADDING | Agent RuleZ (.claude/hooks.yaml) already handles this |
| 9 | Keep hooks fast (under 5s) | ❌ No | Yes | NOT WORTH ADDING | Agent infers from hooks.yaml |
| 10 | Tag releases with `v1.2.3` | ❌ No | No | NOT APPLICABLE | No release process on orchestration-tools |
| 11 | Use `.gitattributes` for line endings | ❌ No | Yes | NOT WORTH ADDING | Already have .gitattributes |
| 12 | Keep PRs under 400 lines of diff | ❌ No | Yes | NOT WORTH ADDING | Agent behavior, not codebase rule |

**Summary:** 2 worth adding (branch naming convention, conventional commits).

---

## Template 4: `python-ml` — PARTIAL MATCH

torch, transformers, accelerate, scikit-learn, nltk, textblob are in `requirements.txt`. However, on `orchestration-tools` the ML code lives on `scientific` — this branch has the deps but no active training loops, model files, or data pipelines in `src/`.

| # | Template Rule | In AGENTS.md? | Applicable? | Verdict | Rationale |
|---|---------------|---------------|-------------|---------|-----------|
| 1 | Type hints on all signatures; document tensor shapes | ✅ Partial | Yes | ALREADY COVERED | "type hints required" covers signatures; no tensors on this branch |
| 2 | Format with `ruff format`; lint with `ruff check` | ❌ No | No | NOT APPLICABLE | Project uses Black + flake8 (in .flake8, setup.cfg) |
| 3 | No magic numbers; define hyperparams in config dataclass | ❌ No | No | NOT APPLICABLE | No model training on this branch |
| 4 | Use `dataclasses` or Pydantic v2 for config objects | ❌ No | Yes | NOT WORTH ADDING | Agent infers from pydantic in requirements.txt |
| 5 | Validate data at every pipeline entry point | ❌ No | No | NOT APPLICABLE | No data pipelines on this branch |
| 6 | Use `pandera` or `great_expectations` for data contracts | ❌ No | No | NOT APPLICABLE | Not in deps; no data processing |
| 7 | Write idempotent pipelines | ❌ No | No | NOT APPLICABLE | No data pipelines |
| 8 | Store intermediate results as Parquet | ❌ No | No | NOT APPLICABLE | No data processing |
| 9 | Use `sklearn.pipeline.Pipeline` | ❌ No | No | NOT APPLICABLE | No model code on this branch |
| 10 | Keep model architectures separate from training loops | ❌ No | No | NOT APPLICABLE | No model code |
| 11 | Implement early stopping on validation loss | ❌ No | No | NOT APPLICABLE | No training loops |
| 12 | Use cross-validation for model selection | ❌ No | No | NOT APPLICABLE | No model selection |
| 13 | Save checkpoints (model state, optimizer, epoch, metric) | ❌ No | No | NOT APPLICABLE | No training |
| 14 | Use `torch.inference_mode()` for evaluation | ❌ No | No | NOT APPLICABLE | No inference code |
| 15 | Track every experiment with MLflow/W&B | ❌ No | No | NOT APPLICABLE | No experiments |
| 16 | Set seeds for reproducibility | ❌ No | No | NOT APPLICABLE | No training |
| 17 | Pin dependency versions; use `uv lock` | ❌ No | Yes | NOT WORTH ADDING | Already have requirements.txt with pinned versions |
| 18 | Smoke-test training: 2 batches on synthetic data | ❌ No | No | NOT APPLICABLE | No training |
| 19 | Use `torch.compile()` for speedup | ❌ No | No | NOT APPLICABLE | No model code |
| 20 | Use mixed precision with `autocast` + `GradScaler` | ❌ No | No | NOT APPLICABLE | No training |

**Summary:** 1 already covered, 0 worth adding. ML deps are present but all ML code lives on `scientific`. When evaluating `scientific`, re-run — most of these become FULL MATCH.

---

## Template 5: `ai-agent-workflow` — PARTIAL MATCH (updated)

This branch IS an agent orchestration system (100+ scripts, CLI with agent/task/infra subcommands, multi-agent handoff framework). The template targets agent self-governance behavior. Most rules are about how the agent acts, not codebase structure — but the orchestration-specific patterns are relevant.

| # | Template Rule | In AGENTS.md? | Applicable? | Verdict | Rationale |
|---|---------------|---------------|-------------|---------|-----------|
| 1 | Plan mode for non-trivial tasks (3+ steps) | ❌ No | Yes | NOT WORTH ADDING | Agent behavior, not codebase rule. Agents already do this. |
| 2 | Use subagents to keep main context clean | ❌ No | Yes | NOT WORTH ADDING | Agent behavior — specific to the agent runtime, not the project |
| 3 | Self-improvement loop (update lessons.md) | ❌ No | No | NOT APPLICABLE | This project uses Task Master, not lessons.md |
| 4 | Never mark task complete without proving it works | ❌ No | Yes | NOT WORTH ADDING | Redundant with Task Master workflow already in AGENTS.md |
| 5 | Demand elegance for non-trivial changes | ❌ No | No | NOT WORTH ADDING | Vague — "is there a more elegant way?" wastes tokens |
| 6 | Autonomous bug fixing | ❌ No | Yes | NOT WORTH ADDING | Agent behavior — agents already do this |
| 7 | Write plan to `tasks/todo.md` | ❌ No | No | NOT APPLICABLE | This project uses Task Master (.taskmaster/), not tasks/ |
| 8 | Simplicity First, No Laziness, Minimal Impact | ❌ No | No | NOT WORTH ADDING | Vague principles — "clean code" category, wastes context |

**Summary:** 0 worth adding. Task Master workflow already covers the relevant patterns. Agent-behavioral rules belong in the agent's own system prompt, not the project's AGENTS.md.

---

## Template 6: `react-typescript` — SKIP (Gradio is the primary UI)

The `client/` directory has React 18, Radix UI (27 components), TanStack Query, Tailwind, etc. in `package.json`, but the project's UI strategy is **Gradio** (`gradio==6.7.0` in `requirements.txt`) for quick prototyping. The React client is scaffolding/secondary — only 3 TS files exist. No React-specific rules should be added to `.ruler/AGENTS.md`.

| # | Template Rule | In AGENTS.md? | Applicable? | Verdict | Rationale |
|---|---------------|---------------|-------------|---------|-----------|
| 1–16 | All React/TypeScript rules | — | No | NOT APPLICABLE | UI is Gradio-based; React client is secondary scaffolding |

**Summary:** 0 worth adding. Gradio is the primary UI; React rules would mislead agents.

---

## Template 5: `code-review` — ALWAYS RELEVANT

These rules describe review behavior. Most are agent-behavioral rather than codebase-structural.

| # | Template Rule | In AGENTS.md? | Applicable? | Verdict | Rationale |
|---|---------------|---------------|-------------|---------|-----------|
| 1 | Keep PRs small and focused (<400 lines) | ❌ No | Yes | NOT WORTH ADDING | Agent behavior |
| 2 | No hardcoded secrets in code or tests | ✅ Yes | Yes | ALREADY COVERED | Critical Rules |
| 3 | All user input validated and sanitized | ❌ No | Minimal | NOT WORTH ADDING | CLI-focused branch, minimal user input |
| 4 | SQL uses parameterized queries | ❌ No | No | NOT APPLICABLE | No SQL on this branch |
| 5 | Check for N+1 query patterns | ❌ No | No | NOT APPLICABLE | No database queries |
| 6 | Functions small, single responsibility | ❌ No | Yes | NOT WORTH ADDING | Vague — agent knows this |
| 7 | No dead code or debugging statements | ❌ No | Yes | NOT WORTH ADDING | Agent behavior |
| 8 | New dependencies justified | ❌ No | Yes | NOT WORTH ADDING | Agent behavior |

**Summary:** 1 already covered, 0 worth adding.

---

## Consolidated Gap Analysis

### Rules WORTH ADDING to `.ruler/AGENTS.md`

| # | Rule | Source Template | Proposed Text | Section |
|---|------|----------------|---------------|---------|
| 1 | Use pathlib.Path | python-fastapi | `Use pathlib.Path for all file path operations` | Code Conventions |
| 2 | Conventional Commits | git-workflow | `Commits: conventional format — feat(scope): subject` | Code Conventions or new Git section |

### Rules confirmed REDUNDANT (already in config files)

| Rule | Config File |
|------|-------------|
| Line length 100/120 | `.flake8` (120), `setup.cfg` (120) |
| isort profile = black | `setup.cfg` |
| Test paths = tests/ | `pytest.ini`, `setup.cfg` |
| Use Black formatting | Agent infers from isort `profile = black` |
| 2-space indent (TS) | Agent infers from TypeScript conventions |
| Use React | Agent infers from `client/package.json` |

### Rules confirmed ESSENTIAL (keep in `.ruler/AGENTS.md`)

| Rule | Why Essential |
|------|--------------|
| Branch Context (orchestration-tools vs scientific) | Cannot be inferred from any config file |
| Key Directories with descriptions | Saves massive exploration time |
| Task Master workflow | Cannot be inferred — project-specific process |
| NEVER use eval/exec | Security — not in any linter config |
| DI over global state | Architectural decision — not enforceable by linter |
| Run verify-agent-content.sh after updates | Project-specific process |

---

## Branch-Dependent Evaluation Process

When running Phase 10 on a **different branch**, follow this process:

### Step 1: Detect the branch's stack

```bash
bash scripts/detect-branch-stack.sh
```

This outputs:
- Which dependency files exist
- Which dependencies are present
- Which source code patterns exist (async routes, SQLAlchemy, CLI)
- Which agentrulegen.com templates to evaluate
- Which config files make certain rules redundant

### Step 2: Determine template applicability

| Branch Pattern | Templates to Evaluate | Templates to Skip |
|----------------|----------------------|-------------------|
| Has `src/` with FastAPI routes + SQLAlchemy | python-fastapi (FULL) | — |
| Has `src/` with FastAPI but no SQLAlchemy | python-fastapi (PARTIAL) | SQLAlchemy/Alembic rules |
| Has `client/` with active React development | react-typescript | — |
| Has `client/` but UI is Gradio-based | — | react-typescript (React is scaffolding) |
| Has `modules/*.sh` + `scripts/*.sh` (>10) | git-workflow | — |
| Has AI/ML deps (torch, transformers) | Check if code exists, not just deps | Template if code exists |
| No frontend | — | react-typescript |
| No Python | — | python-fastapi |

### Step 3: Evaluate each recommended template

For each template:
1. Fetch rules from `agentrulegen.com/templates/<name>`
2. For each rule, check:
   - **Is it in `.ruler/AGENTS.md`?** → Mark ALREADY COVERED
   - **Is there a config file that expresses it?** → Mark REDUNDANT
   - **Does the code pattern exist on this branch?** → If no, mark NOT APPLICABLE
   - **Would the agent naturally infer it?** → If yes, mark NOT WORTH ADDING
   - **None of the above?** → Mark WORTH ADDING
3. Record the evaluation in the STATE file's Phase 10 Decision Log

### Step 4: Apply only WORTH ADDING rules

- Add to `.ruler/AGENTS.md` under the appropriate section
- Run `ruler apply` to redistribute
- Run `bash scripts/verify-agent-content.sh` to confirm no drift

### Key Principle

> **The same `.ruler/AGENTS.md` content is branch-specific.** A rule that is ESSENTIAL on `scientific` (e.g., SQLAlchemy async patterns) may be NOT APPLICABLE on `orchestration-tools`. Always run `detect-branch-stack.sh` before evaluating templates.

---

## Line Count Impact Assessment

Current `.ruler/AGENTS.md`: **57 lines**
Gate check threshold: **80 lines**

| Change | Lines Added | Running Total |
|--------|-------------|---------------|
| Add pathlib.Path to Code Conventions | +1 | 58 |
| Add conventional commits to Code Conventions | +1 | 59 |

**Result:** 59 lines — well under 80-line threshold.
