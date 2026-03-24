# GitHub Actions Workflow Usage Guide

## Overview

This repository uses several automated workflows powered by Google's Gemini CLI. With the GitHub free tier having a 2000 requests/month limit for certain features, it's important to monitor and manage workflow triggers.

## Current Usage

- **Daily rate**: ~43 Gemini workflow runs/day
- **Monthly estimate**: ~1,296 runs/month (~65% of 2000 limit)

## Workflows

### 1. 🔀 Gemini Dispatch (gemini-dispatch.yml)
**Primary consumer** - 48% of all workflow runs

**Triggers:**
- `pull_request_review` - fires on EVERY PR review submission
- `pull_request_review_comment` - fires on EVERY PR comment
- `issue_comment` - fires on EVERY issue comment
- `pull_request` - fires on PR opened
- `issues` - fires on issue opened/reopened

**Recommendation**: Reduce triggers by removing `pull_request_review` (fires on every review). Keep `pull_request` (opened only) and `issues` (opened/reopened). Consider filtering `issue_comment` to only trigger on specific keywords like `@gemini-cli`.

### 2. 📋 Gemini Scheduled Triage (gemini-scheduled-triage.yml)
**Current**: ~5 runs (5% of total)

**Triggers:**
- Hourly cron schedule (`0 * * * *`)
- Manual trigger (`workflow_dispatch`)
- Changes to the workflow file itself

**Recommendation**: Keep - already minimal usage (~5/hour out of 24 possible).

### 3. Other Essential Workflows
- CI (pytest, linting, type checking)
- Dependabot (dependency updates)
- Lint/Test (pull request checks)

**Recommendation**: Keep - essential for project maintenance.

## Usage Limit Strategy

### To Stay Under 2000/month:

1. **Reduce Gemini Dispatch triggers** - remove `pull_request_review` trigger
2. **Monitor monthly usage** - track via GitHub Actions dashboard
3. **Disable scheduled triage** if approaching limit - change cron to every 6 hours or daily

### Risk Levels:
- **Green (<50%)**: Current usage is safe
- **Yellow (50-75%)**: Consider reducing triggers
- **Red (>75%)**: Immediately disable some workflows

## Quick Actions

To reduce triggers in `gemini-dispatch.yml`:

```yaml
on:
  pull_request:
    types: [opened]  # REMOVED: review, closed, etc.
  issues:
    types: [opened, reopened]
  # Keep issue_comment but will trigger on all comments
```

For more granular control, use path filters or required labels.

---

Last updated: 2026-03-24