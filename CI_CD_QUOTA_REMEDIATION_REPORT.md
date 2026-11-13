# CI/CD Quota Remediation Report

**As of:** 2026-11-12  
**Scope:** MasumRab/EmailIntelligence, gemini-fullstack-langgraph-quickstart, gemini-cli-prompt-library, jules, masumrab.github.io  
**Status:** Partial remediation; reviewable PRs opened. No Actions billing usage data was available through the connected API.

## 1. Workflow inventory (default branches)

Inventory counts below include executable `.yml`/`.yaml` files only; README and `.DISABLED` files are excluded.

| Repository | Default branch | Active workflow definitions | Observations |
|---|---|---:|---|
| EmailIntelligence | main | 5 | ci, dependabot-auto-merge, dependency-check, pr-check, semgrep |
| gemini-fullstack-langgraph-quickstart | main | 12 | Includes 8 active jules-pr-* definitions |
| gemini-cli-prompt-library | main | 12 | Includes 8 active jules-pr-* definitions, Robin, CI, security and SonarCloud |
| masumrab.github.io | master | 8 | blank, chatops, ci, docker-nbdev, docker, gh-page, setup, upgrade |
| jules | inaccessible | UNKNOWN | GitHub API returned 404 for MasumRab/jules |

Branch inventories were enumerated (up to 100 branch entries per repository). Full workflow content was inspected for EmailIntelligence, the two Gemini repositories, and the website on their default branches. A complete branch-by-branch workflow diff was not completed.

## 2. Verified usage evidence and root causes

### EmailIntelligence
- Recent 30-run window on 2026-11-11 contains overlapping CI, Semgrep, dependency-check and dynamic push runs against the same main-branch commits.
- PR events independently start CI, Pull Request Check and Semgrep.
- The CI workflow had separate test and lint-only jobs. Both checked out the repository, set up Python and ran `uv sync --all-extras --dev`; test job already ran Ruff.
- Dependency-check has push + pull_request + weekly schedule triggers. The workflow's Python audit installs the complete development dependency set, then runs pip-audit.
- Existing CI used `|| true` on tests, Bandit and lint/type checks, masking failures.

### gemini-fullstack-langgraph-quickstart
- Eight active Jules PR workflows exist on main.
- Dependabot auto-merge listens to both `pull_request` and `pull_request_target`; sampled recent runs show repeated skipped invocations.
- PR Check and Validate Environment both run for matching PRs. PR Check sample had backend success and frontend failure.
- A recent main push-check completed successfully.
- Vercel root-directory issue not fully verified; no Vercel dashboard access was available.

### gemini-cli-prompt-library
- Eight active Jules PR workflows exist on main.
- Robin previously listened to PR lifecycle events and every `issue_comment: created` event. At least 18 Robin runs appeared in the returned recent-run window; sampled job records were all skipped.
- The PR initially removed the broad issue-comment trigger, but inspection showed it still invoked an external reusable LLM workflow on PR lifecycle events using `LLM_API_KEY` and `LLM_BASE_URL`. Provider pricing and free allowance could not be verified. To enforce the no-cost requirement, this PR now removes the automatic Robin workflow entirely.
- Recent CI and SonarCloud runs failed; Security Scan succeeded.
- CI lint job and test job both perform Python setup; test matrix currently has Python 3.11 and 3.12 (Ubuntu only).
- SonarCloud separately installs dependencies and reruns tests, duplicating test work.

### masumrab.github.io
- Eight active workflow definitions exist on master.
- `blank.yml` is a generic Hello World workflow with push + pull_request triggers and no apparent production purpose.
- `ci.yaml` builds on push and pull_request; deployment step is push-only.
- `docker-nbdev.yaml` has a 12-hour schedule but its job condition restricts execution to `fastai/fastpages`; likely skipped for this fork, but run history returned zero runs.
- `docker.yaml` also restricts its job to `fastai/fastpages`.
- Pages publishing workflow must be preserved. No workflow changes were made to the website.

## 3. Changes and PRs

### EmailIntelligence
PR: https://github.com/MasumRab/EmailIntelligence/pull/1042
- Added top-level concurrency cancellation keyed by workflow and PR/ref.
- Added a 15-minute job timeout.
- Added safe documentation/backlog path exclusions.
- Removed redundant lint-only job; lint and formatting remain in the test job.
- Added explicit dependency cache globs for uv lockfiles and pyproject manifests.
- Removed `|| true` masking from tests, Bandit, Ruff and mypy so required validation can fail visibly.
- Python 3.12, tests, security scan and type check retained.
- The EmailIntelligence PR diff adds no paid API, paid action, paid runner or new hosted AI-review integration. This is a statement about the PR changes only, not a verification of account-wide or third-party billing.

### gemini-cli-prompt-library
PR: https://github.com/MasumRab/gemini-cli-prompt-library/pull/66
- Removed the Robin workflow file because it automatically called a reusable external LLM workflow and the provider's zero-cost status could not be established.
- This deliberately disables automatic Robin reviews until its model endpoint and billing controls can be proven free. It does not affect GitHub-native checks or the existing Sourcery/CodeRabbit OSS integrations.

Both PRs are drafts and require review. Neither was merged.

## 4. Free-tier and no-cost policy

- Use only standard GitHub-hosted runners for public repositories; do not select larger runners or paid runner products.
- Do not add paid Marketplace actions, paid plans, free trials that convert to paid plans, metered AI/API keys, or usage-based fallback providers.
- Keep existing OSS AI reviewers only where the repository is eligible for their published public-repository free offering. Do not add additional AI reviewers or trigger redundant reviews.
- Cubic's advertised free Starter allowance is finite (20 reviews/month); do not enable paid flex/overage capacity. Treat this as a hard cap, not an invitation to upgrade.
- Sourcery and CodeRabbit are retained only under their published public/open-source free eligibility. Do not enable paid private-repository features or trials.
- Open-source CLI tools may be used locally or in bounded existing CI jobs, but adding them to CI still consumes runner execution time. Add no always-running scanner jobs without evidence that they cover a gap.
- No external LLM workflow may run automatically unless its endpoint, quota and billing configuration are explicitly verified as zero-cost.
- Repository-level changes cannot guarantee account-level billing settings. Confirm GitHub budget/stop-usage controls and third-party billing settings in their respective dashboards. This remediation did not inspect or change billing settings.

## 5. Measured versus estimated savings

- **Measured Actions minutes saved:** UNKNOWN. Billing usage endpoint was unavailable through the connected GitHub API; no before/after billing telemetry was returned.
- **Measured per-run job durations:** UNKNOWN. Job records returned conclusions but not timestamps/duration values in the sampled response.
- **Verified avoidable work:** EmailIntelligence duplicated checkout/Python setup/full uv dependency sync in its lint-only job; Robin generated many skipped issue-comment workflow executions; Gemini fullstack Dependabot automation produced duplicate skipped event runs.
- **Projected monthly savings:** NOT ESTIMATED. Run counts alone are insufficient to infer billed minutes, and skipped jobs may consume little or no runner time.
- **OS multipliers:** No matrix OS multipliers identified in sampled workflows; EmailIntelligence and sampled Gemini workflows use Ubuntu. gemini-cli-prompt-library test matrix has two Python versions on Ubuntu.

## 6. Validation

- Workflow files and triggers inspected on default branches.
- Recent Actions run lists inspected for the four accessible repositories.
- Sampled job conclusions inspected for recent Gemini fullstack and Robin runs.
- Static review of the PR diff confirms the documented EmailIntelligence workflow changes; no local checkout/actionlint environment was available through this GitHub MCP session, so `actionlint` and `git diff --check`: NOT RUN.
- Tests, lint, build, dependency resolution and workflow execution on the PR branches: NOT RUN / NOT VERIFIED.
- **Workflow-trigger incident:** A prior report-update commit unintentionally triggered PR synchronization workflows despite the exhausted monthly allowance. On commit `a28f417b1c7e368db6d0881db4961f166968fbe4`, Semgrep Security Scan completed successfully; CI failed at the test step; Pull Request Check's Python and frontend jobs passed, while its Codecov artifact-download job failed; Dependabot Auto-Merge was skipped. The run records were inspected after the event. No workflow was manually dispatched or re-run. This incident means the earlier statement that Actions were not triggered was incorrect; it is superseded by this record. Do not trigger further push, pull-request or manual runs while quota remains exhausted unless separately authorized and the billing outcome is established.
- No claim of passing CI, measured minute savings, or verified billing protection is made. PRs remain drafts pending review and separately authorized validation.

## 7. Outstanding work and blockers

1. **Repository access:** `MasumRab/jules` returned GitHub API 404. Confirm repository visibility/name or grant installation access.
2. **Billing telemetry:** GitHub Actions billing usage endpoint was not accessible through the connected API. Obtain owner billing usage export or account billing permissions to rank actual minute drains.
3. **Jules deactivation:** The eight active Jules workflows in each Gemini repository were identified but not yet disabled. Their intended status and any required manual-only workflows need review before archival.
4. **EmailIntelligence:** Further review required for dependency-check trigger duplication, PR Check overlap, and the agent branch population. Main/scientific/orchestration-tools and agent branches were not exhaustively diffed for active workflow counterparts.
5. **Gemini fullstack:** Confirm project root and build target against repository tree and Vercel project settings. Dashboard access was unavailable; no root-directory change made.
6. **gemini-cli-prompt-library:** Review SonarCloud/test duplication and scheduled Jules auto-merge-label workflow. Security scan retained.
7. **Website:** Review and retire generic blank workflow only after confirming no external required status check depends on it. Preserve Pages production publishing.
8. **Target:** <1,000 minutes/month remains unverified until billing telemetry and at least one post-change usage period are available.

## 8. Safety and deployment status

- No branch protection was bypassed.
- No PR was merged.
- No production deployment or security scan was intentionally removed.
- No Vercel setting was changed.
- Robin automatic LLM calls are removed in PR #66 pending verified zero-cost provider configuration.
