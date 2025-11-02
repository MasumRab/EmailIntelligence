# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the EmailIntelligence project.

## Workflows

### 1. CI Workflow (`ci.yml`)
- **Trigger**: Push to `main` or `scientific` branches, and pull requests targeting these branches
- **Purpose**: Runs comprehensive tests, linting, and type checking for all code changes
- **Features**:
  - Python 3.11 testing
  - pytest with coverage reporting
  - Code formatting checks (black, isort)
  - Linting (flake8)
  - Type checking (mypy)

### 2. Dependabot Auto-Merge (`dependabot-auto-merge.yml`)
- **Trigger**: Pull requests opened, synchronized, or reopened
- **Purpose**: Automatically merges Dependabot pull requests when CI passes
- **Safety Features**:
  - Only runs for PRs created by `dependabot[bot]`
  - Uses GitHub's native PR status checks (no bash JSON parsing)
  - Waits for CI workflow completion before proceeding
  - Verifies PR is mergeable and not in draft state using GitHub context
  - Comprehensive error handling for GitHub CLI operations
  - Adds approval comment before enabling auto-merge
  - Uses GitHub's auto-merge feature for safety

## Security Considerations

The Dependabot auto-merge workflow includes several safety measures:
1. **Identity Verification**: Only runs for PRs from `dependabot[bot]`
2. **CI Dependency**: Waits for and requires CI workflow success
3. **Native GitHub Checks**: Uses GitHub's built-in PR status instead of fragile parsing
4. **Merge Readiness**: Verifies PR is in a mergeable state using GitHub context
5. **Error Handling**: Comprehensive error handling with graceful degradation
6. **Approval Process**: Automatically approves and adds explanatory comment

## Setup Requirements

For the workflows to function properly, ensure:
1. The repository has the necessary permissions for GitHub Actions
2. The `GITHUB_TOKEN` has sufficient permissions for auto-merge operations
3. Branch protection rules (if any) are compatible with auto-merge
4. All dependencies are properly defined in `pyproject.toml`

## Customization

To modify the auto-merge behavior:
- Edit the conditions in the workflow `if` statement (line 15)
- Adjust the CI check name in the `wait-for-check` action (line 23)
- Modify the merge strategy (currently uses `--merge`, could use `--squash` or `--rebase`)
- Change timeout values for CI wait (currently 600 seconds)

## Architecture Improvements

The workflows have been optimized for:
- **Reliability**: Native GitHub API usage instead of bash JSON parsing
- **Simplicity**: Single-purpose jobs without unnecessary complexity
- **Error Handling**: Comprehensive error checking with graceful degradation
- **Performance**: Eliminates duplicate test runs by trusting CI results