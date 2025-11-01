# Phase Plan to Attack Major Merge Issues Between fixes-branch and scientific

## Overview
The `fixes-branch` and `scientific` branches have diverged significantly (202 commits in scientific vs ~114 in main/fixes-branch), leading to pervasive merge conflicts. Cherry-picking low-impact commits has proven ineffective due to conflicts in shared files. This plan outlines a phased approach to resolve major merge issues, prioritizing safety, incremental progress, and minimal disruption.

## Phase 1: Comprehensive Assessment (1-2 days)
### Objectives
- Quantify divergence and identify root causes.
- Catalog key features, bug fixes, and architectural changes in `scientific` not present in `fixes-branch`.
- Assess dependencies and inter-commit relationships.

### Actions
1. **Divergence Analysis**:
   - Run `git log --oneline fixes-branch..scientific | wc -l` to count commits.
   - Use `git log --graph --oneline --all` to visualize branch history.
   - Identify merge bases and divergence points.

2. **Feature Inventory**:
   - Review commit messages for major features (e.g., Qwen integration, workflow systems, UI enhancements).
   - Categorize commits: Documentation, Bug Fixes, New Features, Refactors, Dependencies.

3. **Conflict Prediction**:
   - Identify high-conflict files (e.g., `launch.py`, `gradio_app.py`, `database.py`).
   - Estimate effort for each category using historical conflict resolution time.

### Deliverables
- Divergence report with commit breakdown.
- Risk assessment matrix (Low/Medium/High risk for merge).
- Updated branch alignment report with assessment findings.

## Phase 2: Prioritization and Risk Mitigation (1 day)
### Objectives
- Prioritize commits/features for integration.
- Develop mitigation strategies for high-risk items.
- Establish success criteria and rollback plans.

### Actions
1. **Prioritization Matrix**:
   - **High Priority**: Critical bug fixes, security patches, dependency updates.
   - **Medium Priority**: New features with low coupling (e.g., isolated modules).
   - **Low Priority**: Documentation, style fixes, experimental features.
   - **Defer/Exclude**: Highly coupled features that require full architectural changes.

2. **Dependency Mapping**:
   - Map commit dependencies to avoid breaking changes.
   - Identify safe "islands" of commits that can be merged independently.

3. **Mitigation Strategies**:
   - For high-risk: Create feature branches for isolated testing.
   - Backup strategies: Stash, branch snapshots, revert plans.
   - Tools: Use `git merge --no-commit` for manual control.

### Deliverables
- Prioritized commit/feature list with rationale.
- Mitigation playbook for high-risk merges.
- Phase 1-2 summary report.

## Phase 3: Incremental Safe Merges (3-5 days)
### Objectives
- Integrate low-risk, high-value commits/features.
- Build confidence with successful merges.
- Establish patterns for conflict resolution.

### Actions
1. **Start with Documentation and Config**:
   - Merge README updates, config changes, and documentation.
   - Example: Merge commits updating `AGENTS.md`, `llm_guidelines.json`.

2. **Dependency and Tool Updates**:
   - Merge pyproject.toml changes, new dependencies, linting updates.
   - Test with `pip install` and basic imports.

3. **Isolated Features**:
   - Merge self-contained modules (e.g., new analysis components if no core conflicts).
   - Use `git cherry-pick` or `git merge` for small sets.

4. **Validation After Each Merge**:
   - Run lint, type check, and basic tests.
   - Commit and push to fixes-branch for CI validation.

### Deliverables
- Merged low-risk commits/features.
- Test results and validation logs.
- Updated progress in branch alignment report.

## Phase 4: Major Conflict Resolution (5-10 days)
### Objectives
- Tackle high-priority, high-conflict features.
- Resolve core architectural differences.
- Ensure system integrity.

### Actions
1. **Core File Conflicts**:
   - Focus on `launch.py`, `gradio_app.py`, `database.py`, `main.py`.
   - Use `git merge --no-commit` for manual resolution.
   - Prefer fixes-branch versions where possible, integrate scientific improvements.

2. **Feature-by-Feature Integration**:
   - Qwen integration: Merge config and API changes.
   - Workflow systems: Integrate routing and engine updates.
   - UI enhancements: Merge Gradio components carefully.

3. **Conflict Resolution Protocol**:
   - For each conflict: Review both versions, choose best approach.
   - Test immediately after resolution.
   - Document decisions for future reference.

4. **Incremental Commits**:
   - Commit resolved conflicts in logical chunks.
   - Avoid monolithic merges.

### Deliverables
- Resolved major conflicts.
- Functional core system with integrated features.
- Conflict resolution log.

## Phase 5: Testing and Validation (2-3 days)
### Objectives
- Ensure merged code is stable and functional.
- Validate against original requirements.

### Actions
1. **Comprehensive Testing**:
   - Run full test suite: `pytest`, lint, type check.
   - Manual testing of key features (e.g., launch, UI, API endpoints).

2. **Integration Testing**:
   - Test end-to-end workflows.
   - Validate dependencies and imports.

3. **Performance and Regression Checks**:
   - Compare performance metrics.
   - Ensure no regressions in existing functionality.

### Deliverables
- Test reports and coverage.
- Validation sign-off.
- Bug fix list if issues found.

## Phase 6: Final Integration and Cleanup (1-2 days)
### Objectives
- Complete the merge.
- Clean up and document.

### Actions
1. **Final Merge/Rebase**:
   - If not fully merged, perform final `git merge scientific` or rebase.
   - Resolve any remaining conflicts.

2. **Cleanup**:
   - Remove temporary branches, stashes.
   - Update documentation with merge details.

3. **Archival and Documentation**:
   - Archive scientific branch if no longer needed.
   - Update README and branch alignment report with final status.

### Deliverables
- Unified branch with all features.
- Final documentation and lessons learned.

## Alternative Strategies
- **Selective Integration**: Only merge critical features, keep scientific as feature branch.
- **Full Reset**: Rebase scientific onto main, accepting losses.
- **Parallel Development**: Maintain separate branches for different purposes.

## Risks and Contingencies
- **High Risk**: Data loss, broken functionality – frequent backups, revert plans.
- **Timeline Slip**: Adjust phases based on progress.
- **Resource Needs**: May require pair programming for complex conflicts.

## Success Criteria
- All high-priority features integrated.
- No critical bugs or regressions.
- Clean, mergeable codebase.
- Updated documentation.

This plan provides a structured approach to tackle the merge issues incrementally, minimizing risk and ensuring quality.