# Task Numbering Mapping: Old IDs → New Clean IDs

## Task 75 (Branch Clustering System) Integration into Task 002

**Status:** Task 75 now renumbered as **Task 002** (Clustering System) via WS2 refactoring (Jan 4, 2026)

**Important:** Task 002 is a **separate, independent initiative** (Initiative 3) that runs **parallel** with the main framework tasks (Initiative 1-2). It is NOT the same as Task 002 (Merge Validation Framework from Initiative 1).

| Old ID | New Format | Title | Stage | Effort | Status |
|--------|------------|-------|-------|--------|--------|
| Task 75 | 002-Clustering | Branch Clustering System | All | 212-288h | Parallel (separate numbering) |
| 75.1 | 002.1 | CommitHistoryAnalyzer | One | 24-32h | ✅ |
| 75.2 | 002.2 | CodebaseStructureAnalyzer | One | 28-36h | ✅ |
| 75.3 | 002.3 | DiffDistanceCalculator | One | 32-40h | ✅ |
| 75.4 | 002.4 | BranchClusterer | One(I) | 28-36h | ✅ |
| 75.5 | 002.5 | IntegrationTargetAssigner | Two | 24-32h | ✅ |
| 75.6 | 002.6 | PipelineIntegration | Two | 20-28h | ✅ (includes Task 007 merge) |
| 75.7 | 002.7 | VisualizationReporting | Three | 20-28h | ✅ |
| 75.8 | 002.8 | TestingSuite | Three | 24-32h | ✅ |
| 75.9 | 002.9 | FrameworkIntegration | All | 16-24h | ✅ |

**Historical Note:** Task 75 was previously part of scattered codebase analysis. Now unified as dedicated Initiative 3 system.

**Refactoring Context (Jan 4, 2026 - WS2):**
- Task 021→002 renumbering applied across all documentation
- Task 007 (I2.T4 - Feature Branch Identification) merges into Task 002.6 (PipelineIntegration) as execution mode

---

## Cancelled/Duplicate Tasks

The following tasks have been cancelled, merged, or marked as duplicates:

| Task | Status | Reason | Resolution |
|------|--------|--------|------------|
| **007** | MERGED | Feature Branch Identification merged into 002.6 | Functionality preserved in task-002-6.md |
| **019** | DUPLICATE | Same as Task 003 | Use task-003.md for implementation |
| **021** | NEVER EXISTED | Intermediate numbering artifact | No content was created |
| **023** | DUPLICATE | Same as Task 014 (Orchestration Tools Alignment) | Use task-014.md for implementation |
| **025** | MERGED | Content merged into 016 | Use task-016.md (Scan Merge Conflicts) |
| **026** | MERGED | Content merged into 017 | Use task-017.md (launch.py Dependencies) |

---

## Complete Mapping (Initiative 1-5)

| Old Number | New Number | Notes |
| :--- | :--- | :--- |
| Task 7 | 001 | Framework Strategy Definition |
| Task 9 | 002 | Merge Validation Framework |
| 9.1 | 002.1 | Validation subtask 1 |
| 9.2 | 002.2 | Validation subtask 2 |
| 9.3 | 002.3 | Validation subtask 3 |
| 9.4 | 002.4 | Validation subtask 4 |
| 9.5 | 002.5 | Validation subtask 5 |
| 9.6 | 002.6 | Validation subtask 6 |
| 9.7 | 002.7 | Validation subtask 7 |
| 9.8 | 002.8 | Validation subtask 8 |
| 9.9 | 002.9 | Validation subtask 9 |
| Task 19 | ~~003~~ | DUPLICATE - Use Task 003 |
| Task 54 | I2.T1 (004) | |
| (from 74.1) | I2.T1.1 | |
| (from 74.2) | I2.T1.2 | |
| (from 74.3 & 74.8) | I2.T1.3 | |
| (from 74.9) | I2.T1.4 | |
| (from 54.1) | I2.T1.5 | |
| (from 54.2) | I2.T1.6 | |
| (from 54.3) | I2.T1.7 | |
| Task 55 | I2.T2 (005) | |
| (from 55.1 & 76.4) | I2.T2.1 | |
| (from 55.2 & 76.5) | I2.T2.2 | |
| (from 55.3 & 76.6) | I2.T2.3 | |
| (from 55.1) | I2.T2.4 | |
| Task 56 | I2.T3 (006) | |
| 56.1 | I2.T3.1 | |
| 56.2 | I2.T3.2 | |
| 56.3 | I2.T3.3 | |
| Task 57 | ~~007~~ | MERGED into 002.6 |
| 57.3 | I2.T4.5 | |
| Task 59 | I2.T5 (010) | |
| (from 59.19) | I2.T5.1 | |
| (from 59.20) | I2.T5.2 | |
| (from 59.21) | I2.T5.3 | |
| (from 59.22) | I2.T5.4 | |
| (from 59.23) | I2.T5.5 | |
| (from 59.24) | I2.T5.6 | |
| Task 60 | I2.T6 (011) | |
| (from 60.16) | I2.T6.1 | |
| (from 60.17) | I2.T6.2 | |
| (from 60.18) | I2.T6.3 | |
| (from 60.19) | I2.T6.4 | |
| (from 60.20) | I2.T6.5 | |
| Task 61 | I2.T7 (012) | |
| (from 61.1) | I2.T7.1 | |
| (from 61.5) | I2.T7.2 | |
| (from 61.4) | I2.T7.3 | |
| (from 61.7) | I2.T7.4 | |
| (from 61.8) | I2.T7.5 | |
| Task 62 | I2.T8 (013) | |
| (from 62.2) | I2.T8.1 | |
| (from 62.3) | I2.T8.2 | |
| (from 62.8) | I2.T8.3 | |
| (from 62.10) | I2.T8.4 | |
| (from 62.11) | I2.T8.5 | |
| (from 62.13) | I2.T8.6 | |
| (from 62.14) | I2.T8.7 | |
| Task 83 | I2.T9 (014) | |
| 83.1 | I2.T9.1 | |
| 83.2 | I2.T9.2 | |
| 83.3 | I2.T9.3 | |
| 83.4 | I2.T9.4 | |
| 83.5 | I2.T9.5 | |
| Task 63 | I2.T10 (015) | |
| (from 82.1) | I2.T10.1 | |
| (from 82.2) | I2.T10.2 | |
| (from 63.7) | I2.T10.3 | |
| (from 63.13) | I2.T10.4 | |
| (from 63.15) | I2.T10.5 | |
| Task 23 | 022 | Scientific Branch Recovery (Execution) |
| Task 101 | ~~023~~ | DUPLICATE - Use Task 014 |
| Task 27 | 024 | Regression Prevention (Maintenance) |
| Task 31 | ~~025~~ | MERGED into 016 |
| Task 40 | ~~026~~ | MERGED into 017 |
| Task 100 | (Archive) | Legacy, not used |

---

## Final Task Sequence (001-020)

After consolidation, the final task sequence is:

| New # | Title | Source |
| :--- | :--- | :--- |
| 001 | Framework Strategy Definition | task-001.md |
| 002 | Branch Clustering System | task-002.md (+ subtask files) |
| 003 | Pre-merge Validation Scripts | task-003.md |
| 004 | Core Branch Alignment Framework | task-004.md |
| 005 | Automated Error Detection | task-005.md |
| 006 | Branch Backup and Restore | task-006.md |
| 007 | Feature Branch Identification | task-008.md → renamed |
| 008 | Merge Validation Framework | task-009.md → renamed |
| 009 | Primary-to-Feature Alignment | task-010.md → renamed |
| 010 | Complex Branch Strategies | task-011.md → renamed |
| 011 | Validation Integration | task-012.md → renamed |
| 012 | Sequential Orchestration | task-013.md → renamed |
| 013 | Orchestration-Tools Alignment | task-014.md → renamed |
| 014 | Documentation | task-015.md → renamed |
| 015 | Scan Merge Conflicts | task-016.md (expanded from 025) |
| 016 | launch.py Dependencies | task-017.md (expanded from 026) |
| 017 | Import Validation | task-018.md → renamed |
| 018 | Branch Protection | task-020.md → renamed |
| 019 | Scientific Branch Recovery | task-022.md → renamed |
| 020 | Restore Context Control | task-024.md → renamed |

**Total: 20 tasks (001-020), 0 gaps**

---

**Updated:** 2026-01-06 (Phase 1 complete - content expansion and cancellation notes added)
