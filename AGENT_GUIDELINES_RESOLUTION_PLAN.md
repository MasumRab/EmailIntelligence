# Agent Guidelines Consistency Resolution Plan

**Document Status**: ACTIVE  
**Created**: 2025-11-12  
**Target Completion**: 2025-11-30  
**Priority**: HIGH

---

## Root Cause Analysis

### Primary Causes

#### 1. **Branch Divergence Without Synchronization**
- **Problem**: orchestration-tools and scientific branches diverged significantly after a shared ancestor
- **When**: Around commits a617d2b7 (orchestration-tools) vs. 7702247e (scientific)
- **Impact**: Each branch evolved independently, creating separate AGENTS.md versions with different content
- **Evidence**:
  - orchestration-tools focuses on Task Master CLI and orchestration workflows
  - scientific focuses on TypeScript code style and context contamination prevention
  - No synchronization mechanism between branches for shared documentation

#### 2. **No Shared Documentation Standard**
- **Problem**: No single source of truth for agent guidelines across all branches
- **When**: Since initial branch creation
- **Impact**: Each branch creates independent guidance, leading to duplication and inconsistency
- **Evidence**:
  - AGENTS.md content completely different between branches
  - CLAUDE.md identical across branches (by accident, not design)
  - No cross-branch reference mechanism

#### 3. **Context Control System Added Without Full Integration**
- **Problem**: Context profiles created (32942f89) but not fully synchronized with AGENTS.md changes
- **When**: commit 32942f89 "feat: Add context profiles for main and scientific branches"
- **Impact**: Profiles define access control but guidelines don't explain the profiles
- **Evidence**:
  - Profiles don't appear in AGENTS.md documentation
  - Main/scientific profiles block .specify/.taskmaster but AGENTS.md doesn't explain why
  - No documentation linking profiles to actual guidelines

#### 4. **Task Master Implementation Incomplete Across Branches**
- **Problem**: Task Master commands heavily documented in orchestration-tools/main AGENTS.md but absent from scientific AGENTS.md
- **When**: Task Master integrated in orchestration-tools but scientific branch evolved separately
- **Impact**: Scientific branch agents unaware of centralized task management capabilities
- **Evidence**:
  - orchestration-tools AGENTS.md: Full Task Master CLI section (30+ commands)
  - scientific AGENTS.md: Zero mention of Task Master
  - constitution.md references "goals and tasks" but unclear how this maps to either branch

#### 5. **No Enforcement of Documentation Updates**
- **Problem**: Files updated independently without verification of downstream effects
- **When**: Throughout history; each commit updates one file in isolation
- **Impact**: Changes to context control profiles don't trigger AGENTS.md updates, etc.
- **Evidence**:
  - Context profile changes (32942f89) with no corresponding AGENTS.md changes
  - Task Master integration without updating scientific branch docs
  - CLAUDE.md unchanged across major feature additions

#### 6. **Missing Configuration & Convention Documentation**
- **Problem**: No documented standards for how to maintain agent guidelines
- **When**: Never documented; implicit expectations only
- **Impact**: Developers don't know which files to update when changing branch policies
- **Evidence**:
  - `.context-control/` has no README explaining profile system
  - No guide for adding new branches or updating profiles
  - No checklist for documentation updates

### Secondary Causes

#### 7. **Branch-Specific Needs Without Unified Approach**
- Each branch has legitimate different needs (orchestration-tools, scientific, main)
- But no mechanism to satisfy needs while maintaining consistency
- Leads to independent evolution and divergence

#### 8. **Context Contamination Prevention Only in One Place**
- Excellent detailed guidance in scientific AGENTS.md
- But this knowledge doesn't propagate to other branches
- Orchestration agents work without contamination prevention awareness

---

## Impact Assessment

### Severity Matrix

| Issue | Branches Affected | User Impact | Fix Complexity | Dependencies |
|-------|-------------------|------------|-----------------|--------------|
| Task Master scope ambiguity | scientific | HIGH | HIGH | Issue #2, #4 |
| File access control inconsistency | main, scientific | HIGH | MEDIUM | Issue #3 |
| Context contamination guidance missing | orchestration-tools | MEDIUM | LOW | None |
| Code style guidance missing | orchestration-tools | MEDIUM | MEDIUM | Issue #7 |
| Claude vs. non-Claude guidance | all | MEDIUM | MEDIUM | None |
| Profile coverage gaps | feature branches | LOW | LOW | Issue #3 |
| Agent settings redundancy | all | LOW | LOW | None |

---

## Root Cause Dependency Tree

```
┌─────────────────────────────────────────────────────────┐
│ No Shared Documentation Standard (Cause #2)            │
│ └─ Lacks synchronization mechanism                      │
│ └─ No cross-branch reference                            │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    Branch      Context      Task Master
    Divergence  Control      Implementation
    (Cause #1)  Issues       Incomplete
               (Cause #3)    (Cause #4)
         │           │           │
         └───────────┼───────────┘
                     │
    ┌────────────────┴────────────────┐
    ▼                                  ▼
No Enforcement              Configuration
of Updates                  Documentation
(Cause #5)                 Missing (Cause #6)
```

---

## Resolution Strategy

### Phase 1: Establish Foundation (Weeks 1-2)

**Objective**: Create central documentation hub and standards

#### Task 1.1: Create Unified Agent Guidelines Framework
- **Description**: Establish single source of truth structure
- **Deliverable**: `.specify/AGENT_GUIDELINES_FRAMEWORK.md`
- **Content**:
  - Master list of all agent-related documentation files
  - File purposes and interdependencies
  - Update procedures and checklist
  - Branch-specific customization rules
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: None

#### Task 1.2: Document Context Control System
- **Description**: Create comprehensive profile system guide
- **Deliverable**: `.context-control/README.md`
- **Content**:
  - How profiles work
  - Profile matching logic and patterns
  - How to add new branch profiles
  - Security implications
  - Examples for each branch
- **Owner**: TBD
- **Effort**: 3 hours
- **Dependencies**: Task 1.1

#### Task 1.3: Create Code Style Guide
- **Description**: Unified standards for all branches
- **Deliverable**: `CODING_STANDARDS.md`
- **Content**:
  - Python style (orchestration-tools, main, backend services)
  - TypeScript style (scientific, frontend)
  - Shared principles
  - Branch-specific overrides
  - Linting configuration explanations
- **Owner**: TBD
- **Effort**: 4 hours
- **Dependencies**: Task 1.1

#### Task 1.4: Document Agent Context System
- **Description**: Explain context contamination prevention + control profiles together
- **Deliverable**: `CONTEXT_CONTROL_AND_CONTAMINATION_PREVENTION.md`
- **Content**:
  - What context contamination is
  - Prevention techniques (from scientific AGENTS.md)
  - How profiles enforce isolation
  - Testing context contamination prevention
  - Recovery procedures
- **Owner**: TBD
- **Effort**: 3 hours
- **Dependencies**: Task 1.1, 1.2

**Phase 1 Total**: 12 hours | Blocking: Phase 2

---

### Phase 2: Reconcile Branch-Specific Guidance (Weeks 2-3)

**Objective**: Bring all branch AGENTS.md files to consistent state with branch-specific customizations

#### Task 2.1: Create Master AGENTS.md Template
- **Description**: Branch-agnostic template that all branches can use
- **Deliverable**: `.specify/templates/AGENTS.md.template`
- **Content**:
  - Boilerplate sections (mandatory for all branches)
  - Branch-specific sections (optional, marked with {BRANCH_NAME})
  - Integration points with other docs (CLAUDE.md, CODING_STANDARDS.md, etc.)
  - Comment markers for branch customization
- **Owner**: TBD
- **Effort**: 4 hours
- **Dependencies**: Task 1.1, 1.3, 1.4
- **Notes**: Will use this template for Phase 2 tasks 2.2, 2.3, 2.4

#### Task 2.2: Update orchestration-tools AGENTS.md
- **Description**: Add missing sections while preserving existing Task Master content
- **Deliverable**: Updated `AGENTS.md` (orchestration-tools)
- **Changes**:
  - Add section: "Context Contamination Prevention" (from Task 1.4)
  - Add section: "Code Style Guidelines for Python" (from Task 1.3)
  - Keep existing Task Master commands and workflow
  - Add cross-reference to CLAUDE.md for Claude-specific features
  - Add note about non-Jules compatibility
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 2.1
- **Validation**: Review against Phase 1 deliverables

#### Task 2.3: Update scientific AGENTS.md
- **Description**: Add Task Master commands while preserving context/style guidance
- **Deliverable**: Updated `AGENTS.md` (scientific)
- **Changes**:
  - Add section: "Task Master Integration" (reference orchestration-tools version, note any science-specific adaptations)
  - Keep existing context contamination prevention sections
  - Keep existing code style guidance
  - Add section: "Context Control & Branch Access"
  - Link to constitution.md for goal-task alignment
- **Owner**: TBD
- **Effort**: 3 hours
- **Dependencies**: Task 2.1
- **Validation**: Verify Task Master commands match orchestration-tools

#### Task 2.4: Update main AGENTS.md
- **Description**: Consolidate Task Master + code style + context contamination
- **Deliverable**: Updated `AGENTS.md` (main)
- **Changes**:
  - Start with orchestration-tools Task Master section (Task 2.2)
  - Add Python code style section (from CODING_STANDARDS.md)
  - Add context contamination prevention section (from CONTEXT_CONTROL...)
  - Add branch-specific note: "main is foundational but has specialized branches (scientific, orchestration-tools)"
  - Include context control profile explanation
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 2.1, 2.2, 2.3
- **Validation**: Ensure consistency across all three branch versions

#### Task 2.5: Create Agent Selection Guide
- **Description**: Help agents choose correct branch and documentation
- **Deliverable**: `AGENT_BRANCH_SELECTION_GUIDE.md`
- **Content**:
  - Decision tree for selecting correct branch
  - Which AGENTS.md to use (with decision criteria)
  - Context control implications for each branch
  - Common mistakes and how to avoid them
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 2.2, 2.3, 2.4

**Phase 2 Total**: 15 hours | Blocking: Phase 3

---

### Phase 3: Fix Context Control & Access (Weeks 3-4)

**Objective**: Ensure context profiles match documented access controls

#### Task 3.1: Audit and Consolidate Agent Settings
- **Description**: Extract shared settings to defaults, keep only overrides in profiles
- **Deliverable**: 
  - `.context-control/defaults.json` (new)
  - Updated `.context-control/profiles/*.json` (all three)
- **Changes**:
  - Create defaults.json with standard agent_settings
  - Remove duplicate settings from all three profiles
  - Add explanatory comments to profiles explaining why settings differ
  - Explicitly list protected files for each branch (no wildcards guessing)
- **Owner**: TBD
- **Effort**: 3 hours
- **Dependencies**: Task 1.2
- **Validation**: Test that profiles still function correctly with split config

#### Task 3.2: Add Missing Profile Patterns
- **Description**: Create profiles for feature branches to match branch naming convention
- **Deliverable**: Updated `.context-control/profiles/` with new profiles
- **New Profiles**:
  - `orchestration-tools-feature.json` (for orchestration-tools-* branches)
  - `main-feature.json` (for feature/* branches off main)
  - `scientific-feature.json` (for feature/* branches off scientific)
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 1.2
- **Notes**: Feature profiles inherit from parent branch but allow more access (less restricted)

#### Task 3.3: Add Profile Documentation to AGENTS.md
- **Description**: Explain which profile agents will get on each branch
- **Deliverable**: New section in all AGENTS.md files
- **Content**: "Your Context Control Profile" section explaining:
  - Which profile applies to current branch
  - What files this agent can/cannot access
  - Why certain files are restricted
  - How to understand profile warnings if they appear
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 2.2, 2.3, 2.4, 3.1

#### Task 3.4: Create MCP Integration Guide
- **Description**: Separate Claude-specific MCP from agent-agnostic configuration
- **Deliverable**: `MCP_INTEGRATION_GUIDE.md`
- **Content**:
  - For Claude Code users: MCP setup instructions
  - For non-Claude agents: Alternative task integration methods
  - MCP server configuration explanation
  - Tool allowlist and what each tool does
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 1.1
- **Validation**: Ensure non-Claude agents understand their task workflow

**Phase 3 Total**: 9 hours | Blocking: Phase 4

---

### Phase 4: Create Maintenance & Synchronization (Weeks 4-5)

**Objective**: Prevent future inconsistencies through automation and standards

#### Task 4.1: Create Agent Documentation Update Checklist
- **Description**: Step-by-step checklist for updating agent-related docs
- **Deliverable**: `.specify/AGENT_DOCS_UPDATE_CHECKLIST.md`
- **Content**:
  - When to update (triggers: context control change, tool addition, branch creation)
  - Which files to update in what order
  - Validation steps (consistency checks)
  - Per-branch requirements
  - How to validate changes work
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Phase 1-3 complete
- **Usage**: Referenced in PR template

#### Task 4.2: Create GitHub PR Template Update
- **Description**: Add agent documentation checklist to PR template
- **Deliverable**: `.github/pull_request_template.md` (updated)
- **Change**: Add checkbox section for "Agent Documentation Changes":
  - [ ] AGENTS.md updated (if guidance changed)
  - [ ] Context profiles updated (if access control changed)
  - [ ] CLAUDE.md updated (if Claude features changed)
  - [ ] CODING_STANDARDS.md updated (if code style changed)
  - [ ] New branch profile added (if new branch created)
  - Checklist reference link
- **Owner**: TBD
- **Effort**: 1 hour
- **Dependencies**: Task 4.1

#### Task 4.3: Create Branch Synchronization Script
- **Description**: Tool to detect and warn about agent documentation divergence
- **Deliverable**: `scripts/verify-agent-docs-consistency.sh`
- **Functionality**:
  - Compare AGENTS.md versions across branches (warn on major differences)
  - Verify CLAUDE.md exists and is current on all branches
  - Check context control profiles match expected branches
  - Validate CODING_STANDARDS.md referenced correctly
  - Generate consistency report
- **Owner**: TBD
- **Effort**: 3 hours
- **Dependencies**: Phase 1-3 complete
- **Usage**: CI/CD check, manual verification

#### Task 4.4: Update AGENTS.md with Synchronization Note
- **Description**: Add note explaining synchronization mechanism
- **Deliverable**: Header update in all AGENTS.md files
- **Content**: "Keeping Documentation Synchronized" section explaining:
  - How often docs are synchronized
  - What to do if docs are out of sync
  - How to report inconsistencies
  - Reference to update checklist
- **Owner**: TBD
- **Effort**: 1 hour
- **Dependencies**: Task 4.1, 4.3

**Phase 4 Total**: 7 hours | Blocking: Phase 5

---

### Phase 5: Validation & Documentation (Weeks 5-6)

**Objective**: Verify all changes work correctly and document the process

#### Task 5.1: Test Context Control Profiles
- **Description**: Verify each profile grants/blocks access correctly
- **Deliverable**: Test report `docs/CONTEXT_PROFILE_TEST_REPORT.md`
- **Tests**:
  - orchestration-tools profile: Verify scripts/** accessible, tests/** accessible
  - main profile: Verify scripts/** blocked, src/** accessible
  - scientific profile: Verify deployment/** blocked, setup/** blocked, src/** accessible
  - Feature profiles: Verify inheritance works
- **Owner**: TBD
- **Effort**: 3 hours
- **Dependencies**: Task 3.1, 3.2
- **Validation**: Manual test with actual agent access attempts

#### Task 5.2: Verify Task Master Integration
- **Description**: Confirm Task Master commands work on all branches
- **Deliverable**: Test report `docs/TASK_MASTER_INTEGRATION_TEST.md`
- **Tests**:
  - orchestration-tools: All Task Master commands available
  - main: All Task Master commands available (if applicable)
  - scientific: Task Master available and documented
  - Config consistency across branches
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Task 2.3, 4.3
- **Notes**: Only functional if Task Master actually integrated in scientific

#### Task 5.3: Create Agent Guidelines Summary Report
- **Description**: Final consolidated documentation
- **Deliverable**: Updated `BRANCH_AGENT_GUIDELINES_SUMMARY.md` (replace existing)
- **Content**:
  - Final state of all branch guidelines
  - Resolution status for all 8 issues (should be "RESOLVED")
  - Links to all new documentation created
  - Verification test results
  - Maintenance procedures going forward
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: All previous tasks
- **Audience**: Documentation and verification

#### Task 5.4: Create Agent Implementation Guide
- **Description**: Guide for actual agents (Claude, GPT, etc.) on how to use all docs
- **Deliverable**: `AGENT_IMPLEMENTATION_GUIDE.md`
- **Content**:
  - Quick start (1 page)
  - Which docs to read in what order
  - Common workflows by branch
  - Troubleshooting inconsistent guidance
  - How to report documentation issues
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Phase 1-4 complete

#### Task 5.5: Create Review & Sign-Off
- **Description**: Final review of all changes
- **Deliverable**: Review checklist + sign-off document
- **Process**:
  - Code review of all AGENTS.md updates
  - Review of new documentation for clarity
  - Verification tests pass
  - Consistency report shows all issues resolved
  - Final team approval
- **Owner**: TBD
- **Effort**: 2 hours
- **Dependencies**: Tasks 5.1-5.4

**Phase 5 Total**: 11 hours

---

## Implementation Timeline

```
Week 1-2 (Phase 1: Foundation)
├── Task 1.1: Framework                    [████]
├── Task 1.2: Context Control README      [████]
├── Task 1.3: Coding Standards            [████]
└── Task 1.4: Context Contamination Doc   [████]

Week 2-3 (Phase 2: Reconciliation)
├── Task 2.1: AGENTS.md Template          [████]
├── Task 2.2: Update orch-tools AGENTS    [████]
├── Task 2.3: Update scientific AGENTS    [████]
├── Task 2.4: Update main AGENTS          [████]
└── Task 2.5: Branch Selection Guide      [████]

Week 3-4 (Phase 3: Access Control)
├── Task 3.1: Consolidate Settings        [████]
├── Task 3.2: Add Feature Profiles        [████]
├── Task 3.3: Profile Doc in AGENTS       [████]
└── Task 3.4: MCP Integration Guide       [████]

Week 4-5 (Phase 4: Maintenance)
├── Task 4.1: Update Checklist            [████]
├── Task 4.2: PR Template Update          [████]
├── Task 4.3: Verification Script         [████]
└── Task 4.4: Sync Note in AGENTS         [████]

Week 5-6 (Phase 5: Validation)
├── Task 5.1: Test Profiles               [████]
├── Task 5.2: Test Task Master            [████]
├── Task 5.3: Updated Summary Report      [████]
├── Task 5.4: Agent Guide                 [████]
└── Task 5.5: Review & Sign-Off           [████]
```

**Total Effort**: ~61 hours  
**Elapsed Time**: ~6 weeks (with team parallel work)  
**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5

---

## Success Criteria

### Phase 1 Success
- ✅ Documentation framework created and approved
- ✅ Context control system fully documented
- ✅ Code style standards consolidated
- ✅ Context contamination prevention guide created

### Phase 2 Success
- ✅ All AGENTS.md files follow same structure
- ✅ All branch versions include Task Master, context contamination, and code style guidance
- ✅ No redundant/conflicting guidance between branches
- ✅ Branch selection guide helps agents choose correctly

### Phase 3 Success
- ✅ Context profiles use shared defaults + branch-specific overrides
- ✅ All branch patterns covered (main, scientific, orchestration-tools, and feature branches)
- ✅ Each AGENTS.md explains which profile applies
- ✅ MCP integration documented for Claude and non-Claude agents

### Phase 4 Success
- ✅ Checklist prevents future inconsistencies
- ✅ PR template enforces documentation updates
- ✅ Verification script detects divergence
- ✅ Synchronization note explains maintenance process

### Phase 5 Success
- ✅ All context control profiles tested and working
- ✅ Task Master integration verified on all applicable branches
- ✅ All 8 original consistency issues marked as RESOLVED
- ✅ New documentation complete and verified
- ✅ Agent implementation guide helps users navigate all docs

---

## Risk Mitigation

### Risk 1: Incomplete Task Master Integration on Scientific
**Risk**: Task Master may not actually be integrated on scientific branch
**Mitigation**: Task 2.3 includes validation step; if not integrated, document as "planned future work" instead of "available now"
**Fallback**: Create separate "Scientific-Only Workflow" guide

### Risk 2: Branches Diverge Again During Implementation
**Risk**: While implementing Phase 2, new changes push branches further apart
**Mitigation**: Task 4.3 verification script created in Phase 4; communicate Phase plan to team
**Fallback**: Rebase strategy using Phase 1 framework as anchor

### Risk 3: Agent Settings Cannot Be Shared
**Risk**: Task 3.1 discovers settings need different values per branch
**Mitigation**: Keep defaults.json but allow full override in profiles (no error if override used)
**Fallback**: Keep settings duplicated but add comments explaining "intentionally identical to X"

### Risk 4: MCP Not Universal
**Risk**: Task 3.4 discovers MCP doesn't work on non-Claude agents
**Mitigation**: Create alternate "Stateless Task Management" section for non-Claude agents
**Fallback**: Keep Task Master CLI as universal fallback interface

### Risk 5: Documentation Review Takes Longer Than Expected
**Risk**: Phase 5 review and testing takes >2 weeks
**Mitigation**: Run Phase 5.1-5.2 tests in parallel; pre-review during Phase 4
**Fallback**: Accept preliminary testing; full validation can happen post-deployment

---

## Rollback Strategy

If issues arise during implementation:

1. **Before Phase 2**: Rollback to existing documentation; start over with better planning
2. **During Phase 2**: Commit completed AGENTS.md updates but pause at 2.4; review consistency
3. **Before Phase 3**: Keep new documentation but revert profile changes; update individually
4. **Before Phase 4**: Finalize Phase 1-3, mark Phase 4-5 as "planned improvements"
5. **During Phase 5**: Complete Phase 5.3 and 5.5; defer automated scripts (Phase 4.3)

Rollback commits changes made but can resume from last completed phase.

---

## Responsible Parties

| Phase | Primary | Secondary | Reviewer |
|-------|---------|-----------|----------|
| Phase 1 | [ASSIGN] | [ASSIGN] | [ASSIGN] |
| Phase 2 | [ASSIGN] | [ASSIGN] | [ASSIGN] |
| Phase 3 | [ASSIGN] | [ASSIGN] | [ASSIGN] |
| Phase 4 | [ASSIGN] | [ASSIGN] | [ASSIGN] |
| Phase 5 | [ASSIGN] | [ASSIGN] | [ASSIGN] |

---

## Appendix: Related Documents

- **Initial Analysis**: `BRANCH_AGENT_GUIDELINES_SUMMARY.md` (identifies 8 issues)
- **Framework Template**: `.specify/AGENT_GUIDELINES_FRAMEWORK.md` (to be created in Phase 1)
- **Current State**: Existing AGENTS.md, CLAUDE.md, context control profiles (archived in git history)
- **Verification Tests**: To be created in Phase 5

---

## Document Control

| Version | Date | Author | Status |
|---------|------|--------|--------|
| 1.0 | 2025-11-12 | Amp AI | DRAFT - Ready for Team Review |

**Approval Pending**: Architecture Lead, Branch Maintainers, Agent Integration Owner

