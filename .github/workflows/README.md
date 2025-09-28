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
- **Purpose**: Automatically merges Dependabot pull requests when tests pass
- **Safety Features**:
  - Only runs for PRs created by `dependabot[bot]`
  - Runs full test suite before merging
  - Checks code formatting and linting
  - Verifies PR is mergeable and not in draft state
  - Adds approval comment before merging
  - Uses GitHub's auto-merge feature for safety

## Security Considerations

The Dependabot auto-merge workflow includes several safety measures:
1. **Identity Verification**: Only runs for PRs from `dependabot[bot]`
2. **Test Requirements**: All tests must pass before merge
3. **Code Quality**: Linting and formatting checks must pass
4. **Merge Readiness**: Verifies PR is in a mergeable state
5. **Approval Process**: Automatically approves and adds explanatory comment

## Setup Requirements

For the workflows to function properly, ensure:
1. The repository has the necessary permissions for GitHub Actions
2. The `GITHUB_TOKEN` has sufficient permissions for auto-merge operations
3. Branch protection rules (if any) are compatible with auto-merge
4. All dependencies are properly defined in `pyproject.toml`

## Customization

To modify the auto-merge behavior:
- Edit the conditions in the `if` statements
- Adjust the test commands in the `test` job
- Modify the merge strategy (currently uses `--merge`, could use `--squash` or `--rebase`)