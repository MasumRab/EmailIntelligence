# Testing Guide

This guide covers how to run and author tests for EmailIntelligence, the CI gates that enforce quality, and the conventions for skipping CI on documentation-only changes.

> ⚠️ **Branch awareness required.** `main` and `scientific` are **intentionally divergent** product branches. Never merge one into the other. When porting a fix or capability between them, use a curated per-file cherry-pick (see `.taskmaster/BRANCH_MANAGEMENT_MODEL.md`, §4 T1/T2). The testing commands below apply identically on both branches.

## Table of Contents

- [Test Layout](#test-layout)
- [Running Tests Locally](#running-tests-locally)
- [Coverage Gates](#coverage-gates)
- [Frontend Tests](#frontend-tests)
- [Linting & Formatting](#linting--formatting)
- [Security Scans](#security-scans)
- [CI/CD Behavior](#cicd-behavior)
- [CI Control Flags](#ci-control-flags)

---

## Test Layout

```
tests/
├── core/              # Core functionality tests (unit)
├── modules/           # Module-specific tests (unit)
├── integration/       # Component interaction tests
└── conftest.py        # Shared pytest configuration / fixtures
src/                   # Tests alongside source are also collected
modules/               # Tests alongside modules are also collected
```

- **Unit tests** — test individual functions/classes in `tests/core/` and `tests/modules/`.
- **Integration tests** — test component interactions in `tests/integration/`.
- **Target coverage:** 80%+ for new code; CI enforces ≥70% on `src/` + `modules/`.

## Running Tests Locally

**Recommended** (project default, uses `uv`):

```bash
# Full suite with coverage (what CI runs)
uv run pytest tests/ src/ modules/ -v --tb=short \
  --cov=src --cov=modules --cov-report=xml --cov-report=term-missing --cov-fail-under=70

# Single file
uv run pytest tests/core/test_security.py

# Single test node
uv run pytest tests/core/test_security.py::TestSecurity::test_jwt_expiry

# Watch mode (requires pytest-watch)
uv run pytest --watch

# Coverage HTML report
uv run pytest --cov=src --cov=modules --cov-report=html
python -m http.server 8080 --directory htmlcov
```

**Alternative runners** (equivalent):

```bash
pytest                       # bare, if uv/.venv is active
python -m pytest tests/
```

## Coverage Gates

| Scope                        | Threshold | Enforced via                     |
| ---------------------------- | --------- | -------------------------------- |
| `src/` + `modules/` combined | ≥ 70%     | `ci.yml` (`--cov-fail-under=70`) |
| New/modified code            | ≥ 80%     | Pull-request review (guideline)  |

Coverage reports are uploaded as artifacts in CI (`coverage.xml` + HTML).

## Frontend Tests

```bash
# From client/
npm ci
npm run lint        # ESLint
npx tsc --noEmit    # TypeScript type check
npm run test --if-present || echo "No tests configured"   # Jest/Vitest
```

> `npm ci` is used in CI for reproducibility; never commit `package-lock.json` drift.

## Linting & Formatting

| Language          | Tool                | Command                                                        |
| ----------------- | ------------------- | -------------------------------------------------------------- |
| Python (lint)     | ruff                | `uv run ruff check src/ modules/`                              |
| Python (format)   | ruff format / black | `uv run ruff format --check src/ modules/` / `black . --check` |
| Python (imports)  | isort               | `isort . --check`                                              |
| Python (lint alt) | flake8              | `flake8 src/`                                                  |
| Python (types)    | mypy                | `mypy src/`                                                    |
| YAML/JSON/MD      | prettier            | `npx prettier --check .github/workflows/ `*.md`                |

Python standard: Black, 100-char line length; imports ordered stdlib → third-party → local; type hints required on all function signatures; Google-style docstrings.

## Security Scans

```bash
uv run bandit -r src/ modules/          # SAST
```

Bandit runs in `ci.yml` on every PR to `main`/`scientific`. Treat `B`-severity/high-confidence findings as blocking.

## CI/CD Behavior

CI triggers on `pull_request` and `push` (filtered) for `main` and `scientific`.

| Workflow                    | Triggers                         | What it does                                             |
| --------------------------- | -------------------------------- | -------------------------------------------------------- |
| `ci.yml`                    | PR + push to `main`/`scientific` | pytest (cov ≥70%), bandit, ruff lint + format --check    |
| `pr-check.yml`              | PR to `main`/`scientific`        | Frontend: `npm ci`, lint, `tsc --noEmit`, frontend tests |
| `push-check.yml`            | Direct push to `main`            | Fast Python lint (`ruff check src/ modules/`)            |
| `dependabot-auto-merge.yml` | PR by `dependabot[bot]`          | Waits for all checks → approves → auto-merge             |

> `orchestration-tools` is **not** a CI target — it is the shared tooling substrate distributed via sync scripts (T3), not via PR→CI.

## CI Control Flags

Skip or scope CI per-commit or per-PR:

| Mechanism                        | Effect                     |
| -------------------------------- | -------------------------- |
| Commit message `[skip ci]`       | Skip all CI                |
| Commit message `[ci:lint-only]`  | Run lint only, skip tests  |
| Commit message `[ci:tests-only]` | Run tests only, skip lint  |
| PR label `ci:skip-tests`         | Skip the test suite        |
| PR label `ci:skip-lint`          | Skip linting               |
| PR label `automerge`             | Auto-merge after CI passes |

**Path-based triggers** — CI is automatically skipped for documentation-only changes:

- `**/*.md`
- `docs/**`
- `**/*.mdx`

> Code changes always run the full suite. Note: line-ending churn is a common source of spurious diffs when propagating docs (`.gitattributes` sets `eol=lf`); review diffs before committing.
