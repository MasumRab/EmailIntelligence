# Task 008.2: Configure GitHub Actions Workflow and Triggers

**Status:** specified
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None

---

## Overview/Purpose

Set up GitHub Actions workflow to trigger validation on PRs.

## Success Criteria

- [ ] Workflow file created
- [ ] Triggers on PR to main
- [ ] Python environment configured
- [ ] Placeholder for validation steps

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 008.2
- **Title**: Configure GitHub Actions Workflow and Triggers
- **Status**: specified
- **Priority**: high
- **Effort**: 2-3 hours
- **Complexity**: 4/10

### Requirements
1. The validation workflow file is `.github/workflows/merge-validation.yml`, and it runs on
   `pull_request` (opened, synchronize, reopened) and on `workflow_dispatch`, so it can be triggered
   by hand for a branch with no PR.
2. The workflow states its trigger branches explicitly. A `pull_request` trigger with no branch
   filter fires for PRs into every base, including the `scientific` and `orchestration-tools` bases
   this repository actually uses.
3. `permissions:` is declared at the top with the minimum needed (`contents: read`); a validation
   workflow that inherits the default token scope can write to the repository.
4. Concurrency is declared with a group keyed on the PR number and `cancel-in-progress: true`, so a
   force-push cancels the stale run instead of racing it.
5. The workflow's job names are stable, because branch protection (task 008.9) requires status check
   names to exist before they can be required.

## Implementation Guide

Add `.github/workflows/merge-validation.yml`. Model the setup steps on `ci.yml` lines 30-40
(checkout with `submodules: recursive`, `actions/setup-python@v7` at `3.12`,
`astral-sh/setup-uv@v5`, `uv sync --all-extras --dev`).

```bash
uv run python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/merge-validation.yml'))"
gh workflow list --repo MasumRab/EmailIntelligence
```

The first command catches the class of failure that leaves a workflow registered with zero jobs: a
YAML error makes GitHub report "workflow file issue" and run nothing.



## Test Strategy

- Create file with encoding issues (should detect)
- Extract imports from valid Python (should extract)
- Test with backend imports (should flag)

---

## Implementation Notes

### Garbled Text Detection

```python
def detect_encoding_issues(filepath):
    """Check for encoding problems."""
    issues = []
    try:
        with open(filepath, encoding='utf-8', errors='replace') as f:
            content = f.read()
            if '' in content:
                issues.append(f"Replacement characters found in {filepath}")
            if '\x00' in content:
                issues.append(f"Null bytes found in {filepath}")
    except UnicodeDecodeError as e:
        issues.append(f"Decode error in {filepath}: {e}")
    return issues
```

### Import Extraction

```python
def extract_python_imports(filepath):
    """Extract import statements from Python file."""
    imports = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('import '):
                modules = line.replace('import ', '').split(',')
                for m in modules:
                    m = m.strip().split(' as ')[0]
                    imports.append(m)
            elif line.startswith('from '):
                match = re.match(r'from\s+(\S+)', line)
                if match:
                    imports.append(match.group(1))
    return imports
```

---

## Purpose

Set up GitHub Actions workflow to trigger validation on PRs.

---

## Details

Create `.github/workflows/merge-validation.yml` with proper triggers.

### Workflow Configuration

```yaml
name: Merge Validation

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run validation
        run: python scripts/run_validation.py
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 008.3**: Implement Architectural Enforcement
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 008: Create Comprehensive Merge Validation Framework

---

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes


## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied
