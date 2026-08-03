# Testing Guide (scientific)

How to run and author tests on the `scientific` branch, plus the CI gates that
enforce quality. The `scientific` branch is the **experimental** product; tests
live alongside the code in `tests/`, `src/`, `modules/`, and `node_engine/`.

> ⚠️ **Branch awareness.** `main` (stable) and `scientific` (experimental) are
> **intentionally divergent** and are **never merged** into each other. When a
> test or fix needs to cross branches, copy the file (T1/T2) — never merge the
> branches. Branch rules live in
> [`.taskmaster/BRANCH_MANAGEMENT_MODEL.md`](.taskmaster/BRANCH_MANAGEMENT_MODEL.md).

## Table of Contents

- [Test Layout](#test-layout)
- [Running Tests Locally](#running-tests-locally)
- [Watch Mode](#watch-mode)
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
├── core/              # Core functionality (unit)
├── modules/           # Module-specific tests (unit)
├── integration/       # Component interaction tests
└── conftest.py        # Shared fixtures
src/                   # Tests alongside source are also collected
modules/               # Tests alongside modules are also collected
node_engine/           # Node-based workflow engine tests
python_nlp/            # NLP module tests
```

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
```

The scientific launcher exposes a Gradio UI (`launch.py --gradio`) used for
interactive model testing and data visualization — prefer it for ad-hoc checks
during experimentation, but keep CI parity by running the pytest commands above.

## Watch Mode

```bash
# Re-run on file changes (requires pytest-watch)
uv run pytest --watch
```

## Coverage Gates

| Scope | Threshold | Enforced via |
|-------|-----------|--------------|
| `src/` + `modules/` combined | ≥ 70% | `ci.yml` (`--cov-fail-under=70`) |
| New/modified code | ≥ 80% | Pull-request review (guideline) |

Reports are uploaded as CI artifacts (`coverage.xml` + HTML).

## Frontend Tests

```bash
# From client/
npm ci
npm run lint
npx tsc --noEmit
npm run test --if-present   # Jest/Vitest, if configured
```

## Linting & Formatting

| Language | Tool | Command |
|----------|------|---------|
| Python (lint) | ruff / flake8 | `uv run ruff check src/ modules/` / `flake8 .` |
| Python (format) | black / ruff format | `black .` / `uv run ruff format --check src/ modules/` |
| Python (imports) | isort | `isort . --check` |
| Python (types) | mypy | `mypy .` |
| YAML/JSON/MD | prettier | `npx prettier --check .github/workflows/ *.md` |

Python standard: Black, 100-char line length; imports ordered stdlib → third-party → local; type hints required on all signatures; Google-style docstrings.

## Security Scans

```bash
uv run bandit -r src/ modules/
```

## CI/CD Behavior

CI triggers on `pull_request` and `push` for `main` and `scientific`.

| Workflow | Triggers | What it does |
|----------|----------|--------------|
| `ci.yml` | PR + push to `main`/`scientific` | pytest (cov ≥70%), bandit, ruff lint + format --check |
| `pr-check.yml` | PR to `main`/`scientific` | Frontend: `npm ci`, lint, `tsc --noEmit`, frontend tests |
| `push-check.yml` | Direct push to `main` | Fast Python lint (`ruff check src/ modules/`) |

> `orchestration-tools` is **not** a CI target — it is the shared tooling
> substrate distributed via sync scripts (T3), not via PR→CI.

## CI Control Flags

Skip or scope CI per-commit or per-PR:

| Mechanism | Effect |
|-----------|--------|
| Commit message `[skip ci]` | Skip all CI |
| Commit message `[ci:lint-only]` | Run lint only, skip tests |
| Commit message `[ci:tests-only]` | Run tests only, skip lint |
| PR label `ci:skip-tests` | Skip the test suite |
| PR label `ci:skip-lint` | Skip linting |
| PR label `automerge` | Auto-merge after CI passes |

Path-based triggers auto-skip CI for `**/*.md`, `docs/**`, and `**/*.mdx`
(documentation-only changes). Code changes always run the full suite.
