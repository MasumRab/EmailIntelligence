# Phase 10 Appendix: Branch-Dependent Stack Evaluation

**Purpose:** Fine-grained rule-by-rule gap analysis of agentrulegen.com template recommendations against `.ruler/AGENTS.md`, using the **permissive style-based** inclusion model.

**Hand-crafted for:** `orchestration-tools` branch (style: `orchestration-tools`)
**Detection script:** `bash scripts/detect-branch-stack.sh`
**Auto-generated skeleton:** `bash scripts/detect-branch-stack.sh --generate-eval`

---

## How to Use This Document

1. Run `bash scripts/detect-branch-stack.sh` — it classifies the branch into a style family and recommends templates
2. If this is the `orchestration-tools` branch, use the completed tables below
3. For any other branch, run `bash scripts/detect-branch-stack.sh --generate-eval` to auto-generate a skeleton, then fill in the rule verdicts
4. **Permissive principle:** Include rules unless they create a HARD CONFLICT — if any branch in the style family uses the tool, the rules should mention it

---

## Branch Style Classification

This project has 4 major branch styles. Each branch is classified into a style, and the tech stack is cumulative across all branches in that style:

| Style | Root Branch | Description | Branch Count |
|-------|-------------|-------------|--------------|
| `scientific` | `scientific` | Full backend: AI engine, database, caching, auth, email, ML inference, Gradio UI | ~387 |
| `orchestration-tools` | `orchestration-tools` | CLI tooling, agent infrastructure, shell orchestration, multi-branch management | ~54 |
| `main` | `main` | Stable production — union of scientific + orchestration merges | ~5 |
| `taskmaster` | `taskmaster` | Task management infrastructure, agent memory, triage workflows | ~11 |

Feature branches inherit their target's style. The style profile accumulates — if a feature branch adds Redis support, Redis stays in the profile even after the branch merges.

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

## Template 1: `python-fastapi` — INCLUDE (permissive)

FastAPI is in `requirements.txt`. Routes live on `scientific` but this style family has them. Under permissive rules, FastAPI patterns are included unless they hard-conflict with CLI-only code.

| # | Template Rule | In AGENTS.md? | Verdict | Rationale |
|---|---------------|---------------|---------|-----------|
| 1 | Use Python 3.12+ type hints on all signatures | ✅ Yes | ALREADY COVERED | "type hints required" |
| 2 | Run `mypy --strict` or `pyright` in CI | ✅ Yes | ALREADY COVERED | "mypy ." in Lint |
| 3 | Use f-strings for interpolation | ❌ No | REDUNDANT | Agent infers from Python version |
| 4 | Use `pathlib.Path` for file operations | ❌ No | **INCLUDE** | Prevents hardcoded paths, reinforces Critical Rule |
| 5 | Format with `ruff format` / Lint with `ruff check` | ❌ No | HARD CONFLICT | Project uses Black + flake8 (in .flake8, setup.cfg) — mentioning ruff would mislead |
| 6 | Keep route handlers under 15 lines | ❌ No | **INCLUDE** | Routes exist on sibling branches in this style |
| 7 | Group routes with `APIRouter` | ❌ No | **INCLUDE** | Routes exist on sibling branches |
| 8 | Declare `response_model=` on route decorators | ❌ No | **INCLUDE** | Standard FastAPI pattern for sibling branches |
| 9 | Use `Annotated` for DI | ❌ No | **INCLUDE** | DI rule exists but FastAPI-specific syntax is additive |
| 10 | Use `async def` for I/O functions | ❌ No | **INCLUDE** | Async code exists across style family |
| 11 | Never call blocking code in async context | ❌ No | **INCLUDE** | Relevant when async routes are encountered |
| 12 | Use `AsyncSession` with `expire_on_commit=False` | ❌ No | **INCLUDE** | SQLAlchemy present on scientific branches in same style |
| 13 | Alembic migrations | ❌ No | **INCLUDE** | Database work happens on sibling branches |
| 14 | Custom exception classes for HTTP errors | ❌ No | **INCLUDE** | Standard pattern for the style family |
| 15 | Hash passwords with `passlib[bcrypt]` | ❌ No | **INCLUDE** | Auth exists on scientific branches |
| 16 | Configure CORS — never `["*"]` with credentials | ❌ No | **INCLUDE** | Security rule; relevant when web server runs |
| 17 | Use `pytest-asyncio` | ❌ No | REDUNDANT | Already in pytest.ini markers; agent infers |
| 18 | Use `httpx.AsyncClient` for route tests | ❌ No | **INCLUDE** | Test pattern for sibling branches |

**Summary:** 2 already covered, 13 included (permissive), 2 redundant, 1 hard conflict.

---

## Template 2: `git-workflow` — FULL MATCH

78 shell scripts, multi-branch project with branch.sh, safety.sh, distribute.sh. Git workflow rules are directly relevant.

| # | Template Rule | In AGENTS.md? | Verdict | Rationale |
|---|---------------|---------------|---------|-----------|
| 1 | Branch naming: `feature/AGE-123-desc` | ❌ No | **INCLUDE** | Multi-branch project; agent needs naming convention |
| 2 | Delete branches after merging | ❌ No | **INCLUDE** | Relevant — some branches are long-lived but cleanup still matters |
| 3 | Conventional Commits: `<type>(<scope>): <subject>` | ❌ No | **INCLUDE** | Not in any config file; agent cannot infer commit format |
| 4 | Commit types: feat, fix, docs, style, refactor... | ❌ No | ALREADY COVERED (by #3) | Part of Conventional Commits |
| 5 | Subject line: imperative, <72 chars, no period | ❌ No | ALREADY COVERED (by #3) | Part of Conventional Commits |
| 6 | Never commit generated files, secrets, node_modules | ✅ Partial | ALREADY COVERED | "NEVER commit secrets or API keys" + .gitignore |
| 7 | Rebase feature branches before PR | ❌ No | **INCLUDE** | Multi-branch project; clarifies merge strategy |
| 8 | Use `pre-commit` hooks for linting | ❌ No | **INCLUDE** | Agent RuleZ exists but pre-commit hooks are additive |
| 9 | Keep hooks fast (under 5s) | ❌ No | REDUNDANT | Agent infers from hooks.yaml |
| 10 | Tag releases with `v1.2.3` | ❌ No | **INCLUDE** | Permissive — release process may evolve |
| 11 | Use `.gitattributes` for line endings | ❌ No | REDUNDANT | Already have .gitattributes |
| 12 | Keep PRs under 400 lines of diff | ❌ No | **INCLUDE** | Useful guidance for this complex multi-branch project |

**Summary:** 1 already covered, 8 included, 2 redundant.

---

## Template 3: `python-ml` — INCLUDE (permissive)

torch, transformers, accelerate, scikit-learn, nltk are in `requirements.txt`. ML code lives primarily on `scientific`, but the deps are shared and ML functionality is core to the project. Under permissive rules, ML patterns are included to prepare agents for when ML code is encountered across the style family.

| # | Template Rule | In AGENTS.md? | Verdict | Rationale |
|---|---------------|---------------|---------|-----------|
| 1 | Type hints on all signatures; document tensor shapes | ✅ Partial | ALREADY COVERED | "type hints required" |
| 2 | Format with `ruff format`; lint with `ruff check` | ❌ No | HARD CONFLICT | Project uses Black + flake8 |
| 3 | No magic numbers; define hyperparams in config dataclass | ❌ No | **INCLUDE** | ML code on sibling branches uses hyperparams |
| 4 | Use `dataclasses` or Pydantic v2 for config objects | ❌ No | **INCLUDE** | Pydantic in deps; config pattern applies broadly |
| 5 | Validate data at every pipeline entry point | ❌ No | **INCLUDE** | Data pipelines exist on scientific branches |
| 6 | Use `pandera` or `great_expectations` for data contracts | ❌ No | **INCLUDE** | Good practice; not yet in deps but permissive inclusion |
| 7 | Write idempotent pipelines | ❌ No | **INCLUDE** | Data pipelines on sibling branches |
| 8 | Store intermediate results as Parquet | ❌ No | **INCLUDE** | Performance pattern for data processing |
| 9 | Use `sklearn.pipeline.Pipeline` | ❌ No | **INCLUDE** | scikit-learn in deps |
| 10 | Keep model architectures separate from training loops | ❌ No | **INCLUDE** | Core ML architecture pattern |
| 11 | Implement early stopping on validation loss | ❌ No | **INCLUDE** | Training code on scientific branches |
| 12 | Use cross-validation for model selection | ❌ No | **INCLUDE** | scikit-learn in deps |
| 13 | Save checkpoints (model state, optimizer, epoch, metric) | ❌ No | **INCLUDE** | torch in deps; training on sibling branches |
| 14 | Use `torch.inference_mode()` for evaluation | ❌ No | **INCLUDE** | torch in deps |
| 15 | Track every experiment with MLflow/W&B | ❌ No | **INCLUDE** | Experiment tracking is best practice for the project |
| 16 | Set seeds for reproducibility | ❌ No | **INCLUDE** | ML reproducibility |
| 17 | Pin dependency versions; use `uv lock` | ❌ No | REDUNDANT | Already have requirements.txt with pinned versions |
| 18 | Smoke-test training: 2 batches on synthetic data | ❌ No | **INCLUDE** | ML testing pattern |
| 19 | Use `torch.compile()` for speedup | ❌ No | **INCLUDE** | torch in deps; performance optimization |
| 20 | Use mixed precision with `autocast` + `GradScaler` | ❌ No | **INCLUDE** | GPU training optimization |

**Summary:** 1 already covered, 16 included (permissive), 1 redundant, 1 hard conflict. On `scientific` branch these become FULL MATCH with active code.

---

## Template 4: `ai-agent-workflow` — INCLUDE (permissive)

This branch IS an agent orchestration system (100+ scripts, CLI with agent/task/infra subcommands, multi-agent handoff framework). The template targets agent self-governance patterns. Under permissive rules, these are included since the project manages multi-agent workflows — but adapted for Task Master (not generic `tasks/todo.md`).

| # | Template Rule | In AGENTS.md? | Verdict | Rationale |
|---|---------------|---------------|---------|-----------|
| 1 | Plan mode for non-trivial tasks (3+ steps) | ❌ No | **INCLUDE** | Agent orchestration is this branch's purpose |
| 2 | Use subagents to keep main context clean | ❌ No | **INCLUDE** | Multi-agent patterns are core to this project |
| 3 | Self-improvement loop (update lessons.md) | ❌ No | **INCLUDE** (adapt) | Adapt to Task Master: use `task-master update-task --prompt=` instead of lessons.md |
| 4 | Never mark task complete without proving it works | ❌ No | **INCLUDE** | Reinforces Task Master workflow already in AGENTS.md |
| 5 | Demand elegance for non-trivial changes | ❌ No | **INCLUDE** | Gentle reminder; permissive inclusion |
| 6 | Autonomous bug fixing | ❌ No | **INCLUDE** | Agent autonomy is relevant to this orchestration project |
| 7 | Write plan to `tasks/todo.md` | ❌ No | **INCLUDE** (adapt) | Adapt to Task Master: use `.taskmaster/` not `tasks/todo.md` |
| 8 | Simplicity First, No Laziness, Minimal Impact | ❌ No | **INCLUDE** | General engineering principle; not harmful |

**Summary:** 8 included (permissive, some adapted). Adapt template's task tracking to Task Master conventions.

---

## Template 5: `react-typescript` — SKIP (hard conflict with UI strategy)

The `client/` directory has React 18, Radix UI (27 components), TanStack Query, Tailwind in `package.json`, but the project's UI strategy is **Gradio** (`gradio` in `requirements.txt`) for quick prototyping. Only 3 TS files exist. Adding React rules would mislead agents into building complex React components when the project prefers Gradio for UI.

**Why SKIP instead of INCLUDE:** This is one of the few **hard conflicts** — including React patterns would actively contradict the project's stated UI direction. The React scaffolding exists but is not the intended path. If the UI strategy changes back to React, re-evaluate.

| # | Template Rule | Verdict | Rationale |
|---|---------------|---------|-----------|
| 1–16 | All React/TypeScript rules | HARD CONFLICT | UI strategy is Gradio; React rules would mislead agents |

**Summary:** 0 included. Hard conflict with Gradio UI strategy.

---

## Template 6: `code-review` — INCLUDE (always relevant)

Code review patterns apply to all branches. Under permissive rules, include all that don't hard-conflict.

| # | Template Rule | In AGENTS.md? | Verdict | Rationale |
|---|---------------|---------------|---------|-----------|
| 1 | Keep PRs small and focused (<400 lines) | ❌ No | **INCLUDE** | Good practice for 593-branch project |
| 2 | No hardcoded secrets in code or tests | ✅ Yes | ALREADY COVERED | Critical Rules |
| 3 | All user input validated and sanitized | ❌ No | **INCLUDE** | CLI accepts user input; applies across style family |
| 4 | SQL uses parameterized queries | ❌ No | **INCLUDE** | SQL exists on scientific branches |
| 5 | Check for N+1 query patterns | ❌ No | **INCLUDE** | Database queries on scientific branches |
| 6 | Functions small, single responsibility | ❌ No | **INCLUDE** | General quality; permissive inclusion |
| 7 | No dead code or debugging statements | ❌ No | **INCLUDE** | Housekeeping pattern |
| 8 | New dependencies justified | ❌ No | **INCLUDE** | Important with shared requirements.txt across branches |

**Summary:** 1 already covered, 7 included (permissive).

---

## Consolidated Gap Analysis

### Evaluation Summary

| Template | Included | Already Covered | Redundant | Hard Conflict |
|----------|----------|-----------------|-----------|---------------|
| python-fastapi | 13 | 2 | 2 | 1 (ruff) |
| git-workflow | 8 | 1 | 2 | 0 |
| python-ml | 16 | 1 | 1 | 1 (ruff) |
| ai-agent-workflow | 8 | 0 | 0 | 0 |
| react-typescript | 0 | 0 | 0 | 16 (Gradio conflict) |
| code-review | 7 | 1 | 0 | 0 |
| **Total** | **52** | **5** | **5** | **18** |

### Inclusion Decision

52 rules are marked INCLUDE. However, `.ruler/AGENTS.md` must stay under 80 lines (currently 57). These 52 rules should NOT all be added verbatim — they should be **distilled** into concise guidance categories:

### Proposed Additions to `.ruler/AGENTS.md`

| # | Category | Distilled Rule | Source Templates | Lines |
|---|----------|----------------|------------------|-------|
| 1 | Paths | `Use pathlib.Path for all file path operations` | python-fastapi | +1 |
| 2 | Commits | `Commits: conventional format — type(scope): subject` | git-workflow | +1 |
| 3 | FastAPI | `FastAPI routes: async def, response_model=, Annotated DI, APIRouter grouping` | python-fastapi | +1 |
| 4 | Async | `Async: never block async context; use run_in_executor for sync I/O` | python-fastapi | +1 |
| 5 | Database | `SQLAlchemy: AsyncSession, expire_on_commit=False, Alembic migrations` | python-fastapi | +1 |
| 6 | ML | `ML: separate model architecture from training, use inference_mode(), set seeds, track experiments` | python-ml | +1 |
| 7 | Data | `Data: validate at pipeline entry, idempotent transforms, Parquet for intermediates` | python-ml | +1 |
| 8 | Security | `Security: parameterized SQL, validate all user input, explicit CORS origins, no secrets in tests` | python-fastapi, code-review | +1 |
| 9 | UI | `UI: Gradio for prototyping (primary); React/Vite client is secondary scaffolding` | project decision | +1 |
| 10 | PRs | `PRs: under 400 lines, justify new deps, no dead code` | git-workflow, code-review | +1 |

**Total: +10 lines → 67 lines (under 80-line threshold)**

### Rules confirmed HARD CONFLICT (do NOT add)

| Rule | Conflict |
|------|----------|
| Use `ruff format` / `ruff check` | Project uses Black + flake8 (.flake8, setup.cfg) |
| React/TypeScript patterns | UI strategy is Gradio; React client is scaffolding |

### Rules confirmed REDUNDANT (already in config files)

| Rule | Config File |
|------|-------------|
| Line length 100/120 | `.flake8` (120), `setup.cfg` (120) |
| isort profile = black | `setup.cfg` |
| Test paths = tests/ | `pytest.ini`, `setup.cfg` |
| Use Black formatting | Agent infers from isort `profile = black` |
| Pin dependency versions | `requirements.txt` already pinned |
| pytest-asyncio | `pytest.ini` markers |
| .gitattributes line endings | `.gitattributes` already exists |
| hooks speed | Agent infers from `.claude/hooks.yaml` |

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

### Step 1: Detect the branch's style and stack

```bash
bash scripts/detect-branch-stack.sh
```

This outputs:
- Branch style classification (scientific, orchestration-tools, main, taskmaster)
- Cumulative style profile (all deps across the style family)
- Current branch actual state
- Template recommendations (permissive)
- Redundancy signals (config files)

### Step 2: Generate evaluation skeleton (optional)

```bash
bash scripts/detect-branch-stack.sh --generate-eval
```

Creates `docs/handoff/phase-10-stack-evaluation-<branch>.md` with pre-filled branch context and empty evaluation tables for each recommended template.

### Step 3: Determine template applicability (permissive)

| Branch Style | Templates to Evaluate | Hard Conflicts to Skip |
|-------------|----------------------|----------------------|
| `scientific` | python-fastapi (FULL), python-ml (FULL), ai-agent-workflow, git-workflow, code-review | ruff (uses Black+flake8) |
| `orchestration-tools` | python-fastapi (INCLUDE), python-ml (INCLUDE), ai-agent-workflow (FULL), git-workflow (FULL), code-review | ruff, react-typescript (Gradio) |
| `main` | All templates — union of scientific + orchestration | ruff |
| `taskmaster` | ai-agent-workflow, code-review | Most framework-specific templates |
| Has `client/` with active React development | Add react-typescript | — |
| Has `client/` but UI is Gradio-based | — | react-typescript (hard conflict) |

### Step 4: Evaluate each template (permissive)

For each template:
1. Fetch rules from `agentrulegen.com/templates/<name>`
2. For each rule, apply the **permissive** classification:
   - **INCLUDE** (default) — Rule is relevant to the style family
   - **ALREADY COVERED** — Rule exists in `.ruler/AGENTS.md`
   - **REDUNDANT** — Rule is expressed in a config file
   - **HARD CONFLICT** — Rule contradicts a project convention (only reason to exclude)
3. Distill INCLUDE rules into one-liner summaries to stay under 80 lines
4. Record in the STATE file Phase 10 Decision Log

### Step 5: Apply

- Add distilled rules to `.ruler/AGENTS.md`
- Run `ruler apply` to redistribute
- Run `bash scripts/verify-agent-content.sh` to confirm no drift

### Key Principles

> **Permissive by default.** If a tool exists in requirements.txt, if a branch in the
> style family uses it, or if a feature branch targeting this style adds it — include it.
> Only exclude on HARD CONFLICT (ruff vs Black, React vs Gradio).

> **Cumulative across style.** Style profiles grow as feature branches add capabilities.
> Only trim on major reworks of branch responsibilities.

> **Distill, don't dump.** 52 template rules become 10 one-liner summaries.
> The 80-line limit forces compression. Each line should be high-signal — something
> the agent cannot infer from config files or universal conventions.

---

## Line Count Impact Assessment

Current `.ruler/AGENTS.md`: **57 lines**
Gate check threshold: **80 lines**

| Change | Lines Added | Running Total |
|--------|-------------|---------------|
| Add pathlib.Path to Code Conventions | +1 | 58 |
| Add conventional commits to Code Conventions | +1 | 59 |
| Add FastAPI patterns line | +1 | 60 |
| Add async patterns line | +1 | 61 |
| Add SQLAlchemy/database line | +1 | 62 |
| Add ML patterns line | +1 | 63 |
| Add data pipeline line | +1 | 64 |
| Add security line | +1 | 65 |
| Add UI strategy line | +1 | 66 |
| Add PR guidance line | +1 | 67 |

**Result:** 67 lines — under 80-line threshold with 13 lines of headroom.

> **Note:** These 10 distilled lines compress 52 template rules into actionable one-liners.
> Each line is a high-signal summary the agent cannot infer from config files.
> If line budget is tight, prioritize: pathlib.Path (#1), conventional commits (#2),
> UI strategy (#9), and ML patterns (#6) — those have the highest "agent cannot infer" signal.
