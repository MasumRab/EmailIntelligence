# GitHub Workflows Implementation Roadmap

## Overview

This document outlines a prioritized strategy for implementing GitHub Actions workflows in the EmailIntelligence project. The recommendations are based on best practices for Python/FastAPI applications and are aligned with the project's free tier GitHub usage limits (2,000 min/month).

---

## Executive Summary

| Priority | Workflow | Effort | Impact | Timeline |
|----------|----------|--------|--------|----------|
| P0 | Unit & Integration Tests (CI) | 1-2h | Critical | Week 1 |
| P0 | Linting & Code Quality | 30m | Critical | Week 1 |
| P1 | Security Scanning | 1h | High | Week 2 |
| P1 | Merge Validation Framework | 4-6h | Critical | Task 7 (In Planning) |
| P2 | Build & Push Docker Image | 2h | Medium | Week 3 |
| P2 | E2E/Integration Tests | 2-3h | Medium | Week 4+ |
| P3 | Dependency Updates (Dependabot) | 30m | Low | Later |
| P3 | Release & Changelog | 2-3h | Low | Later |
| P3 | Performance Regression Detection | 3-4h | Low | Later |
| P3 | Documentation Generation | 1-2h | Low | Later |

---

## Current Status

### Existing Workflows
- ✅ **extract-orchestration-changes.yml** - Extracts orchestration files to dedicated branch

### Recent Updates (November 9, 2025)
- ✅ Enhanced post-checkout and post-merge hooks to detect hooks-disabled state
- ✅ Added `.git/hooks.disabled` detection to prevent syncing on branches with disabled hooks
- ✅ Updated SYNC-FRAMEWORK.md with independent setup development workflow
- ✅ Documented orchestration file extraction and management

---

## P0 - CRITICAL (Do First)

### 1. Unit & Integration Tests (CI) - test.yml

**Purpose**: Catch regressions and prevent broken code from merging

**Configuration**:
```yaml
triggers:
  - pull_request
  - push: [main, scientific, 'feature/*']

runs:
  - pytest with coverage
  - Report coverage to PR
  - Block merge if tests fail (required check)
```

**What to include**:
- Install dependencies from `requirements.txt` + `requirements-dev.txt`
- Run pytest from `tests/` and `src/backend/tests/`
- Generate coverage reports
- Post coverage badge/summary to PR

**Free tier impact**: Medium (depends on test suite size, typically 5-15 min per run)

**Implementation checklist**:
- [ ] Create `.github/workflows/test.yml`
- [ ] Verify pytest configuration in `pytest.ini`
- [ ] Test on feature branch PR
- [ ] Enable as required check in branch protection rules

---

### 2. Linting & Code Quality - lint.yml

**Purpose**: Enforce consistent code style and catch common errors early

**Configuration**:
```yaml
triggers:
  - pull_request

runs:
  - flake8 (check style)
  - pylint (check code quality)
  - black --check (format validation)
  - isort --check (import sorting)
```

**What to include**:
- Use existing `.flake8` and `.pylintrc` configurations
- Report violations in PR comments
- Fail if issues found

**Free tier impact**: Low (typically 1-3 min per run, fast checks)

**Implementation checklist**:
- [ ] Create `.github/workflows/lint.yml`
- [ ] Verify `.flake8`, `.pylintrc` are current
- [ ] Test on feature branch
- [ ] Enable as required check in branch protection rules

---

## P1 - HIGH (Do Next)

### 3. Security Scanning - security.yml

**Purpose**: Catch vulnerabilities in code and dependencies before they reach production

**Configuration**:
```yaml
triggers:
  - pull_request
  - push: [main, scientific]
  - schedule: daily

runs:
  - pip-audit (dependency vulnerabilities)
  - bandit (SAST for Python code)
  - Report critical/high severity findings
```

**What to include**:
- Scan `requirements.txt` and `requirements-dev.txt`
- Scan `src/backend/**/*.py` with bandit
- Block merge on critical/high vulnerabilities
- Allow low/info findings (informational only)

**Free tier impact**: Low (typically 2-5 min per run)

**Implementation checklist**:
- [ ] Create `.github/workflows/security.yml`
- [ ] Configure bandit for Python
- [ ] Test with intentional vulnerability (then remove)
- [ ] Enable as required check for high/critical only

---

### 4. Merge Validation Framework - merge-validation.yml

**Purpose**: Ensure scientific→main merges meet all architectural, performance, and security standards

**This is Task 7 in the backlog** - Comprehensive validation gate

**Configuration**:
```yaml
triggers:
  - pull_request: [target: main, source: scientific]

runs:
  - Architectural consistency checks (src/backend module boundaries)
  - Full regression test suite execution
  - E2E smoke tests against live FastAPI instance
  - Performance benchmark testing (detect regressions)
  - Security vulnerability scanning
  - Generate unified validation report
```

**Status**: Documented in Task 7, implementation in progress

**Related files**:
- Task definition: `.taskmaster/tasks/tasks.json` (Task 7)
- Validation criteria: `docs/ci-cd/VALIDATION_CRITERIA.md` (to be created in Task 7)

**Implementation checklist**:
- [ ] Complete Task 7 implementation
- [ ] Create `.github/workflows/merge-validation.yml`
- [ ] Define validation criteria in `docs/ci-cd/VALIDATION_CRITERIA.md`
- [ ] Enable as required check for main branch

---

## P2 - MEDIUM (Do Within Sprint)

### 5. Build & Push Docker Image - build-docker.yml

**Purpose**: Validate app builds correctly and enable easy deployment/testing

**Configuration**:
```yaml
triggers:
  - push: [main, scientific]
  - tags: [v*]

runs:
  - Build Docker image from Dockerfile
  - Push to ghcr.io (GitHub Container Registry)
  - Tag with commit SHA + 'latest'
```

**What to include**:
- Dockerfile must exist in root or `src/backend/`
- Use GitHub's built-in container authentication
- Tag images sensibly (sha, branch, version)

**Free tier impact**: Medium (image storage, typically 5-10 min per build)

**Implementation checklist**:
- [ ] Verify Dockerfile exists and builds locally
- [ ] Create `.github/workflows/build-docker.yml`
- [ ] Test on main branch push
- [ ] Verify images appear in Package registry

---

### 6. E2E/Integration Tests - e2e.yml

**Purpose**: Validate full user workflows and API integrations work end-to-end

**Configuration**:
```yaml
triggers:
  - pull_request: [main, scientific]
  - schedule: nightly

runs:
  - Build Docker image of PR code
  - Start FastAPI service from container
  - Run pytest against live API
  - Validate critical user flows
```

**What to include**:
- API authentication flows
- Email processing pipeline
- Smart filtering/retrieval
- Core business logic flows

**Free tier impact**: High (slower tests, 10-30 min per run; run nightly only for cost control)

**Implementation checklist**:
- [ ] Identify critical user flows
- [ ] Create E2E test suite in `tests/e2e/`
- [ ] Create `.github/workflows/e2e.yml`
- [ ] Set to run nightly + on PR to main (not every feature PR)

---

## P3 - LOW (Defer)

### 7. Dependency Updates (Dependabot) - dependabot.yml

**Purpose**: Keep dependencies fresh and patched

**Configuration**:
```yaml
triggers:
  - daily/weekly schedule (GitHub Dependabot)

runs:
  - Checks for outdated dependencies
  - Creates PRs for updates
  - CI runs on those PRs automatically
```

**What to include**:
- Configure `.github/dependabot.yml` with schedule
- Group updates by type (major, minor, patch)
- Allow auto-merge for patch updates

**Free tier impact**: Low (creates PRs, CI runs on them)

**Implementation checklist**:
- [ ] Create `.github/dependabot.yml`
- [ ] Configure update schedule (weekly)
- [ ] Test by manually creating dependency PR

---

### 8. Release & Changelog - release.yml

**Purpose**: Automate release creation and changelog generation

**Configuration**:
```yaml
triggers:
  - push: tags (v*)

runs:
  - Create GitHub Release
  - Generate changelog
  - Build artifacts (if any)
```

**Timeline**: Defer until you have release process defined

---

### 9. Performance Regression Detection - performance.yml

**Purpose**: Track API performance over time, alert on degradation

**Configuration**:
```yaml
triggers:
  - schedule: weekly or nightly

runs:
  - Load tests against main branch
  - Compare with baseline
  - Report regressions
```

**Free tier impact**: Very high (intensive tests)

**Timeline**: Defer until you have performance baselines

---

### 10. Documentation Generation - docs.yml

**Purpose**: Auto-publish API docs and project documentation

**Configuration**:
```yaml
triggers:
  - push: main

runs:
  - Build docs (Sphinx/mkdocs)
  - Deploy to GitHub Pages
```

**Timeline**: Defer until documentation structure is finalized

---

## Implementation Timeline

### **Week 1** (P0 - Start this week)
- [ ] Create test.yml (Unit & Integration Tests)
- [ ] Create lint.yml (Linting & Code Quality)
- [ ] Enable both as required checks
- [ ] Test on feature branch PRs

### **Week 2** (P1 - Start next week)
- [ ] Create security.yml (Security Scanning)
- [ ] Enable as required check for high/critical
- [ ] Review and finalize Task 7 merge validation

### **Week 3** (P2 - Early sprint)
- [ ] Create build-docker.yml (Docker Build)
- [ ] Verify Dockerfile works
- [ ] Test on main branch

### **Week 4+** (P2 continuation & P3)
- [ ] Create e2e.yml (E2E Tests) - set to nightly initially
- [ ] Plan P3 workflows for future implementation

---

## Free Tier Usage Projection

### Scenario A: P0 Only (Recommended Start)
- Test CI: ~300 min/month (5 PRs/week × 4 weeks × 15 min avg)
- Lint: ~50 min/month (5 PRs/week × 4 weeks × 2.5 min avg)
- **Total: ~350 min/month** ✅ Well within limits (2,000 available)

### Scenario B: P0 + P1 Security
- Add security.yml: ~80 min/month (on PRs + daily)
- **Total: ~430 min/month** ✅ Safe

### Scenario C: P0 + P1 + P2 Docker
- Add build-docker.yml: ~100 min/month (main/scientific pushes)
- **Total: ~530 min/month** ✅ Comfortable

### Scenario D: Full Stack with E2E (Nightly)
- Add e2e.yml nightly: ~300 min/month (daily, ~10 min runs)
- **Total: ~830 min/month** ✅ Still safe

**Conclusion**: You can implement everything through P2, even full E2E, while staying comfortably within free tier limits.

---

## Integration with Current Infrastructure

### Existing Hooks Impact
The following Git hooks will continue to operate alongside CI/CD:
- ✅ **post-checkout** - Syncs orchestration files (respects hooks-disabled state)
- ✅ **post-merge** - Syncs orchestration files (respects hooks-disabled state)
- ✅ **pre-commit** - Warns about orchestration-managed files
- ⚠️ **post-push** - Can be simplified/removed (GitHub Actions replaces it)

### Orchestration Workflow Integration
- **extract-orchestration-changes.yml** already exists
- Continues to run independently of new CI/CD workflows
- No conflicts expected

---

## Success Criteria

### P0 Complete ✓
- [ ] Test workflow runs on all feature PRs
- [ ] Lint workflow runs on all feature PRs
- [ ] Both workflows are required checks on main/scientific
- [ ] All PRs show green checkmarks

### P1 Complete ✓
- [ ] Security scan identifies known vulnerabilities
- [ ] Task 7 merge validation framework deployed
- [ ] High/critical vulns block merge

### P2 Complete ✓
- [ ] Docker images build and push successfully
- [ ] Images available in GitHub Package Registry
- [ ] E2E tests validate core workflows (nightly)

---

## Related Documentation

- **SYNC-FRAMEWORK.md** - Orchestration file syncing and hooks behavior
- **orchestration_summary.md** - Orchestration branch scope and responsibilities
- **Task 7** - Merge Validation Framework details
- **AGENTS.md** - Task Master workflow and commands

---

## Questions & Decisions Needed

Before implementation, confirm:

1. **Testing**: What is the current test coverage? Which tests are critical path?
2. **Docker**: Should Docker build run on every push or only tagged releases?
3. **E2E**: Which user workflows are critical enough to test in CI?
4. **Performance**: Do you have performance baselines to compare against?
5. **Security**: What vulnerability severity levels should block merge?

---

## Next Steps

1. **Review this document** with team
2. **Create test.yml** (P0 - 1-2 hours)
3. **Create lint.yml** (P0 - 30 mins)
4. **Enable branch protection** rules requiring these checks
5. **Monitor usage** in GitHub Actions tab
6. **Proceed to P1** once P0 is stable (1-2 weeks)

---

**Last Updated**: November 9, 2025  
**Status**: Ready for implementation  
**Owner**: CI/CD Team
