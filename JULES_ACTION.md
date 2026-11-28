# Jules Action Recommendations – EmailIntelligence

> **Note:** This document describes an **alternative** approach using the third-party
> `thalesraymond/jules-pr-reviewer@v1` action. The repo already has a custom self-hosted
> 8-workflow stack deployed in `.github/workflows/jules-pr-*.yml`. See
> `docs/jules_actions.md` for the deployed stack traceability. This page is a reference
> for the simpler third-party option, not a replacement mandate.

## Project Overview

EmailIntelligence is an AI-powered email analysis platform with a Python/FastAPI
backend, React/TypeScript frontend, and ML/NLP stack. Key characteristics:

- FastAPI backend with modular architecture (`src/core/`, `modules/`, `backend/`)
- React 18 + TypeScript + Vite frontend (`client/`)
- ML/NLP stack: transformers, scikit-learn, NLTK
- JSON file storage with gzip compression, in-memory caching
- Multi-branch development: `main`, `scientific`, `orchestration-tools`
- Dependency management via `uv`; linting via `ruff`, `flake8`, `black`

Most contributions are small-to-medium PRs that modify API routes, AI engine logic,
frontend components, or workflow modules. The **Advanced Jules PR Reviewer** is a
simpler alternative to the custom self-hosted workflow stack: it can pinpoint
problematic patterns, flag missing docstrings, and auto-resolve its comments once
you push a fix.

### Recommended Workflow (Advanced PR Reviewer)

Create `.github/workflows/jules-advanced-pr-review.yml` (only if replacing the
existing custom self-hosted stack). Before enabling, disable or remove **all**
overlapping `jules-pr-*.yml` workflows in `.github/workflows/` to avoid duplicate
reviews, comments, and Jules sessions:

```yaml
name: Jules Advanced PR Review – EmailIntelligence
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

concurrency:
  group: jules-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # post review comments
      contents: read # read repo & rule file
      statuses: write # set jules/review commit status
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # full history needed for diff analysis

      - name: Run Jules Advanced PR Review
        uses: thalesraymond/jules-pr-reviewer@<full-commit-sha> # pin to audited release SHA; see https://github.com/thalesraymond/jules-pr-reviewer/releases
        with:
          jules_api_key: ${{ secrets.JULES_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Optional rule file – to be created at .github/jules-review-rules.md
          rules_file: .github/jules-review-rules.md
          # Project-specific extra instructions (keep < 200 words)
          extra_instructions: |
            EmailIntelligence is an AI-powered email analysis platform (Python/FastAPI + React/TypeScript).
            Focus on:
              • Security – never log raw email content or PII at INFO level or higher.
              • Docstring completeness – every public function must have a docstring.
              • Consistency with existing module layout (src/core/, modules/, backend/).
              • Unit-test coverage – any new public function should be accompanied by at least one test.
              • Follow the project's linting config (ruff, flake8, black — see pyproject.toml).
          timeout_minutes: 40
```

#### Optional Rule File (`.github/jules-review-rules.md`)

To be created. A useful starter set:

```markdown
# Jules Review Rules – EmailIntelligence

## Blocking

- Functions that log raw email content (subject/body) or PII at INFO level or higher.
- SQL injection via unsanitized user input in database queries.

## Warn

- Use of bare `except:` – catch specific exception types.
- Public functions missing a docstring.
- Missing type hints on function parameters or return values.

## Info

- Lines longer than 100 characters – consider splitting for readability.
- Replacing `print()` debugging statements with the project logger (`logger.debug(...)`).
```

### When to Use Other Jules Actions

| Action                          | When it makes sense                                                                                                                            | How to adapt (brief)                                                                                                                                                                                                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Jules Invoke** (generic task) | Scheduled maintenance (dependency updates, linting, docs sweeps) that is not tied to a specific PR.                                            | Use the generic Invoke template with a prompt such as "Run `uv pip list` and `pip-audit` (or `safety check`) to identify packages with known vulnerabilities; open a PR to update any package with CVSS >= 7.0; ensure ruff/flake8/black pass; verify README reflects current structure; run the test suite and propose fixes for any failures." |
| **Jules PR Comment**            | You run a Jules task from a schedule or workflow_dispatch and want the session details (prompt, logs, artifacts) posted on the relevant PR(s). | After the Invoke step captures the returned session ID, call the `jules-pr-comment` workflow (or copy its step) with that session ID and the PR number you want to comment on.                                                                                                   |
| **Send Feedback to Jules**      | You want human reviewers (maintainers) to be able to feed their review comments back into Jules so it can learn from corrections.              | Add the `send-feedback-to-jules` workflow (see below) and list the maintainer usernames in `feedback_users`.                                                                                                                                                                     |

---

## Reasoning & Context

- The **Advanced PR Reviewer** sends only the _changed_ diff to Jules on each `synchronize` event, which is essential for a Python-heavy repo where a full-repo scan would waste tokens on unchanged files.
- Line-level comments map directly to the exact function definition or pattern that Jules flags, making it trivial for contributors to locate and fix the issue.
- Auto-resolve reduces comment noise: once you push a fix, Jules automatically marks its own comment thread as resolved, keeping the PR tidy.
- The `extra_instructions` block injects project-specific conventions (security, PII handling, docstring completeness, module layout, unit-test coverage, linting/formatting) without requiring Jules to relearn them from scratch, improving accuracy and lowering token cost.
- The rule file lets you encode "house rules" (blocking/warn/info) that Jules will treat with the appropriate severity, aligning its verdict with your project's policy.
