# TODO Restoration and Branch Alignment Plan

## Overview
This document outlines the implementation plan to restore lost TODO comments and align the feature-notmuch-tagging-1, scientific, and align-feature-notmuch-tagging-1-v2 branches with consistent documentation and development roadmap items.

## Current State Analysis

### Branch Status
- **Scientific Branch**: Contains the most comprehensive TODO comments and documentation
- **Feature-notmuch-tagging-1 Branch**: Missing several TODO comments from security_manager.py compared to scientific branch
- **Align-feature-notmuch-tagging-1-v2 Branch**: Missing additional TODO comments from workflow_engine.py compared to feature-notmuch-tagging-1 branch

### Lost TODO Comments Identified

#### security_manager.py (feature-notmuch-tagging-1 missing compared to scientific)
- Line 53: `# TODO(P1, 3h): Implement comprehensive security policies with RBAC support`
- Line 61: `# TODO(P1, 4h): Add rate limiting for different user roles and node types`
- Line 225: `# TODO(P1, 4h): Enhance sanitization to support additional content types (Markdown, etc.)`
- Line 233: `# TODO(P2, 2h): Add configurable sanitization policies based on security levels`
- Line 288: `# TODO(P1, 8h): Implement comprehensive execution sandboxing with resource isolation`
- Line 289: `# TODO(P2, 4h): Add support for custom execution environments based on node security levels`

#### workflow_engine.py (align-feature-notmuch-tagging-1-v2 missing compared to feature-notmuch-tagging-1)
- Various TODOs related to type validation, optional input ports, input transformation, type compatibility rules, generic types, and type coercion

## Implementation Strategy

### Phase 1: Restore security_manager.py TODO Comments (Immediate Priority)

#### Step 1.1: Backup Current Files
```bash
cp backend/node_engine/security_manager.py backend/node_engine/security_manager.py.backup
```

#### Step 1.2: Restore TODO Comments to feature-notmuch-tagging-1 Branch
1. Add the following TODO comment after line 50 (within the `has_permission` method):
   ```python
   # TODO(P1, 3h): Implement comprehensive security policies with RBAC support
   # Pseudo code for RBAC security policies:
   # - Create Role-Based Access Control system
   # - Define roles: admin, user, guest with different permissions
   # - Implement permission checking for node execution
   # - Add user context to security validation
   # - Support role hierarchies and permission inheritance
   ```

2. Add the following TODO comment after line 58 (within the `has_permission` method):
   ```python
   # TODO(P1, 4h): Add rate limiting for different user roles and node types
   # Pseudo code for rate limiting:
   # - Implement token bucket or sliding window algorithms
   # - Different limits for different user roles (admin: 1000/min, user: 100/min)
   # - Per-node-type rate limiting (expensive nodes: lower limits)
   # - Add rate limit headers to responses
   # - Implement rate limit bypass for trusted operations
   ```

3. Add the following TODO comment after line 222 (within the `InputSanitizer.sanitize_string` method):
   ```python
   # TODO(P1, 4h): Enhance sanitization to support additional content types (Markdown, etc.)
   # Pseudo code for additional content type sanitization:
   # - Add Markdown sanitization with allowed elements (headers, links, lists)
   # - Implement CSV sanitization to prevent formula injection
   # - Add XML sanitization with schema validation
   # - Support YAML sanitization with type safety checks
   # - Implement binary data sanitization for file uploads
   ```

4. Add the following TODO comment after line 230 (within the `InputSanitizer` class):
   ```python
   # TODO(P2, 2h): Add configurable sanitization policies based on security levels
   # Pseudo code for configurable sanitization policies:
   # - Create SanitizationPolicy class with different security levels
   # - Level 1 (Strict): Minimal allowed content, maximum security
   # - Level 2 (Standard): Balanced security and functionality
   # - Level 3 (Permissive): Maximum functionality, reduced security
   # - Allow per-user or per-operation policy selection
   ```

5. Add the following TODO comments after line 285 (within the `ExecutionSandbox` class):
   ```python
   # TODO(P1, 8h): Implement comprehensive execution sandboxing with resource isolation
   # TODO(P2, 4h): Add support for custom execution environments based on node security levels
   ```

#### Step 1.3: Test Changes
```bash
# Run tests to ensure no functionality was broken
python -m pytest backend/node_engine/test_security.py -v
python -m pytest backend/node_engine/test_sanitization.py -v
```

### Phase 2: Align workflow_engine.py TODO Comments

#### Step 2.1: Identify Complete Set of TODO Comments
- Compare workflow_engine.py across all three branches
- Identify the most comprehensive set of TODO comments from scientific branch
- Ensure all branches have consistent TODO coverage

#### Step 2.2: Restore Missing TODO Comments
- Apply the complete set of workflow_engine.py TODO comments to align-feature-notmuch-tagging-1-v2 branch
- Verify consistency across branches

### Phase 3: Documentation Alignment

#### Step 3.1: Documentation Audit
- Compare documentation sets across all branches
- Identify unique documentation files in each branch
- Identify documentation gaps

#### Step 3.2: Merge Documentation Sets
- Create comprehensive documentation set incorporating:
  - Scientific branch baseline documentation
  - Feature-notmuch-tagging-1 specialized documentation (67 unique files)
  - Align-feature-notmuch-tagging-1-v2 comprehensive task documentation (200+ unique files)

#### Step 3.3: Update Documentation References
- Ensure all TODO comments reference relevant documentation files
- Update cross-references between code and documentation

### Phase 4: Branch Alignment Verification

#### Step 4.1: Create Alignment Verification Script
```bash
#!/bin/bash
# verify_alignment.sh
echo "Checking TODO comment consistency across branches..."

# Compare security_manager.py
echo "Comparing security_manager.py TODOs:"
git show scientific:backend/node_engine/security_manager.py | grep -n "TODO" || echo "No TODOs in scientific"
git show feature-notmuch-tagging-1:backend/node_engine/security_manager.py | grep -n "TODO" || echo "No TODOs in feature-notmuch-tagging-1"
git show align-feature-notmuch-tagging-1-v2:backend/node_engine/security_manager.py | grep -n "TODO" || echo "No TODOs in align-feature-notmuch-tagging-1-v2"

echo "Verification complete."
```

#### Step 4.2: Code Quality Verification
- Run linters to ensure no syntax errors in added comments
- Run static analysis tools to check for consistency
- Run unit tests to ensure functionality remains intact

### Phase 5: Commit and Merge Process

#### Step 5.1: Commit Changes to feature-notmuch-tagging-1
```bash
git add backend/node_engine/security_manager.py
git commit -m "feat: restore lost TODO comments in security_manager.py

- Restore RBAC security policies implementation TODO
- Restore rate limiting implementation TODO
- Restore content type sanitization TODO
- Restore configurable sanitization policies TODO
- Restore execution sandboxing TODO
- Restore custom execution environments TODO"
```

#### Step 5.2: Update align-feature-notmuch-tagging-1-v2
- Merge feature-notmuch-tagging-1 changes into align-feature-notmuch-tagging-1-v2
- Add workflow_engine.py TODO comments as identified
- Run verification steps

#### Step 5.3: Final Verification
- Ensure all branches have consistent TODO comment coverage
- Verify documentation alignment
- Run full test suite

## Risk Mitigation

### Code Changes
- Always backup files before making changes
- Run tests after each phase to catch regressions
- Use git diff to verify exact changes before committing

### Branch Management
- Create feature branches for each phase if needed
- Ensure clean merge states before proceeding
- Use pull requests for final integration

## Success Criteria

### Technical Criteria
- All three branches have consistent TODO comment coverage
- No functionality is broken by the changes
- All tests pass successfully
- Code quality metrics remain stable

### Process Criteria
- Development roadmap items are preserved across branches
- Documentation is consolidated and up-to-date
- Team members can clearly identify implementation priorities

## Next Steps

1. Execute Phase 1: Restore security_manager.py TODO comments
2. Validate changes and run tests
3. Execute Phase 2: Align workflow_engine.py TODO comments
4. Execute Phase 3: Documentation alignment
5. Execute Phase 4: Verification
6. Execute Phase 5: Final commits and merge validation