# Plan to Address Path and File Existence Issues in Tests

## Executive Summary

The EmailIntelligence test suite has multiple path and file existence issues that prevent test execution. This plan provides a systematic approach to resolve environment variable requirements, missing dependencies, and configuration issues.

## Current Issues Identified

### 1. Environment Variable Dependencies
**Issue**: Tests fail due to missing required environment variables

**Affected Tests**:
- `tests/test_auth.py` - Requires `SECRET_KEY`
- `tests/test_password_hashing.py` - Requires `SECRET_KEY`

**Root Cause**: `src/core/settings.py` enforces `SECRET_KEY` requirement in `__init__`

### 2. Missing Python Dependencies
**Issue**: Tests import modules that aren't installed

**Affected Tests**:
- `tests/test_mfa.py` - Requires `pyotp` package
- `tests/modules/default_ai_engine/test_modular_ai_engine.py` - Requires `transformers` package

**Root Cause**: Optional dependencies not installed in test environment

### 3. Import Path Issues
**Issue**: Test modules cannot import required components

**Affected Tests**:
- `tests/test_launcher.py` - Cannot import from `launch.py`
- Various tests with module import failures

**Root Cause**: Import path resolution and circular import issues

### 4. Configuration and File Path Issues
**Issue**: Tests expect certain directories and files to exist

**Root Cause**: Missing data directories, configuration files, or improper path handling

## Detailed Resolution Plan

### Phase 1: Environment Variable Setup (Priority: HIGH)

#### 1.1 Create Test Environment Configuration
**Objective**: Provide test-specific environment variables

**Actions**:
- Create `tests/.env.test` file with test-specific values
- Update `tests/conftest.py` to load test environment variables
- Set `SECRET_KEY` to a known test value
- Add other required environment variables for tests

**Implementation**:
```bash
# tests/.env.test
SECRET_KEY=test-secret-key-for-emailintelligence-testing-only
DATA_DIR=./test_data
DEBUG=true
```

**Success Criteria**:
- `SECRET_KEY` environment variable is available during tests
- Settings module initializes without errors
- Auth-related tests can import required modules

#### 1.2 Update Test Fixtures
**Objective**: Ensure test fixtures set required environment variables

**Actions**:
- Modify `tests/conftest.py` to set environment variables automatically
- Add environment variable setup to session fixtures
- Ensure variables are set before any test module imports

**Success Criteria**:
- Test session starts with all required environment variables
- No "SECRET_KEY environment variable must be set" errors

### Phase 2: Dependency Management (Priority: HIGH)

#### 2.1 Install Missing Test Dependencies
**Objective**: Ensure all required packages are available for tests

**Actions**:
- Add missing dependencies to `pyproject.toml` dev dependencies:
  - `pyotp` for MFA functionality
  - `transformers` for AI engine tests (optional/skip if not available)
- Update dependency installation in CI/test environment
- Consider making some dependencies optional with skip markers

**Implementation**:
```toml
# pyproject.toml [project.optional-dependencies]
test = [
    "pyotp>=2.0.0",
    "transformers>=4.40.0",
    "pytest-env>=1.1.0",
    # ... other test dependencies
]
```

**Success Criteria**:
- `pyotp` and `transformers` packages are available
- Tests can import required modules without ModuleNotFoundError

#### 2.2 Implement Dependency-Aware Test Skipping
**Objective**: Gracefully handle optional dependencies

**Actions**:
- Add pytest skip markers for optional dependencies
- Implement try/except blocks in test modules
- Use `pytest.importorskip()` for optional imports

**Example**:
```python
# In test files
transformers = pytest.importorskip("transformers")
pyotp = pytest.importorskip("pyotp")
```

**Success Criteria**:
- Tests skip gracefully when dependencies are missing
- No import errors for optional functionality

### Phase 3: Import Path Resolution (Priority: HIGH)

#### 3.1 Fix Launcher Import Issues
**Objective**: Resolve circular and path import issues

**Actions**:
- Fix `tests/test_launcher.py` import from `launch` module
- Update import statements to use correct module paths
- Resolve any circular import issues

**Analysis**: The test is trying to import `PYTHON_MAX_VERSION` from `launch.py`, but this constant doesn't exist in the current launch.py structure.

**Success Criteria**:
- `tests/test_launcher.py` can import required modules
- No import errors related to launcher functionality

#### 3.2 Standardize Test Import Patterns
**Objective**: Ensure consistent import behavior across tests

**Actions**:
- Update `tests/conftest.py` PYTHONPATH setup
- Ensure all test files can import project modules
- Standardize import patterns across test files

**Success Criteria**:
- All test modules can import project components
- Consistent import behavior across the test suite

### Phase 4: File and Directory Setup (Priority: MEDIUM)

#### 4.1 Create Test Data Directories
**Objective**: Ensure required directories exist for tests

**Actions**:
- Create `tests/test_data/` directory structure
- Set up mock data files for tests that require them
- Configure test-specific data paths

**Success Criteria**:
- Required data directories exist during test execution
- Tests can read/write test data without path errors

#### 4.2 Implement Test Isolation
**Objective**: Prevent tests from interfering with each other

**Actions**:
- Use temporary directories for file-based tests
- Implement proper cleanup between tests
- Ensure test data doesn't persist between runs

**Success Criteria**:
- Tests run in isolation without side effects
- No conflicts between parallel test execution

### Phase 5: CI/CD Integration (Priority: MEDIUM)

#### 5.1 Update CI Pipeline
**Objective**: Ensure tests run in CI environment

**Actions**:
- Update GitHub Actions or CI configuration
- Install test dependencies in CI
- Set required environment variables in CI
- Add test result reporting

**Success Criteria**:
- CI pipeline can execute full test suite
- Test failures are properly reported
- Environment setup works in CI

## Implementation Timeline

| Phase | Duration | Key Deliverables | Dependencies |
|-------|----------|------------------|--------------|
| 1 | 1-2 days | Environment variables configured | None |
| 2 | 1-2 days | Dependencies installed, optional handling | Phase 1 |
| 3 | 1-2 days | Import issues resolved | Phase 1-2 |
| 4 | 1 day | Test data setup, isolation | Phase 1-3 |
| 5 | 1 day | CI integration | Phase 1-4 |

## Risk Mitigation

### Technical Risks
- **Dependency Conflicts**: Test optional dependencies separately
- **Environment Variable Leaks**: Use test-specific values clearly marked as non-production
- **Import Path Complexity**: Implement gradual migration to fix imports

### Process Risks
- **Test Coverage Reduction**: Ensure optional tests don't reduce overall coverage metrics
- **CI Failures**: Test CI changes in isolation before merging
- **Team Coordination**: Communicate changes to environment setup requirements

## Success Criteria

### Functional Success
- All tests can be collected without import errors
- Test suite runs without environment variable errors
- Optional dependencies are handled gracefully
- CI pipeline executes tests successfully

### Quality Success
- Test execution is reliable and reproducible
- Environment setup is well-documented
- New tests follow established patterns
- Test failures provide clear diagnostic information

## Immediate Action Items

1. **Create test environment file**: `tests/.env.test`
2. **Update pyproject.toml**: Add missing test dependencies
3. **Fix conftest.py**: Load test environment variables
4. **Update failing tests**: Add environment variable setup

## Next Steps

1. Begin implementation with Phase 1 (environment variables)
2. Test each phase incrementally
3. Update documentation with new environment requirements
4. Train team on test environment setup

---

*This plan addresses the root causes of test failures while establishing a robust testing environment for the EmailIntelligence project.*
