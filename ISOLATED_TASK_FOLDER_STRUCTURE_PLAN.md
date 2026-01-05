# Isolated Task Folder Structure Plan

**Purpose:** Define directory organization that enables independent teams to work on separate subtasks without coordination overhead  
**Scope:** new_task_plan/ directory complete structure  
**Goal:** One agent can pick up task-002-3.md and work completely independently  
**Status:** Ready for Implementation

---

## Core Principle: Isolation

**Isolated Task Completion means:**
- ✅ Agent A works on task-002-3.md (CommitHistoryAnalyzer, Stage One)
- ✅ Agent B works on task-021-5.md (IntegrationTargetAssigner, Stage Two) 
- ✅ Agent C works on task-001-2.md (Alignment Strategy)
- ✅ All 3 work simultaneously WITHOUT waiting for others
- ✅ Each agent has everything needed in their subtask file
- ✅ Minimal cross-reference checking required
- ✅ Work can be integrated at end without rework

**Isolation is enabled by:**
1. Self-contained subtask files (task-XXX-Y.md)
2. Clear folder structure (easy to navigate)
3. Comprehensive guidance co-located (not scattered)
4. Execution context documented (what can run in parallel)
5. Progress tracking templates (independent logging)

---

## Target Directory Structure

### Level 1: Root Directory (new_task_plan/)

```
new_task_plan/
├── README.md                           # ✅ ENTRY POINT for anyone new
├── QUICK_START.md                      # 🆕 QUICK START by role/task type
├── NAVIGATION_GUIDE.md                 # 🆕 WHERE IS EVERYTHING?
│
├── task_files/                         # Main work area
│   ├── README.md                       # Task files overview
│   ├── task-001.md through task-026.md # Main task overviews (26 files)
│   ├── task-001-1.md through task-001-4.md  # Task 001 subtasks (4)
│   ├── task-002-1.md through task-002-9.md  # Task 002 subtasks (9)
│   ├── task-021-1.md through task-021-9.md  # Task 021 subtasks (9)
│   ├── task-003-1.md through task-020-5.md  # Other subtasks (~60+)
│   └── task-022-1.md through task-026-4.md  # Execution/maintenance (~15)
│
├── guidance/                           # 🆕 Architectural guidance & findings
│   ├── README.md                       # Guidance overview
│   ├── GUIDANCE_INDEX.md               # 🆕 Searchable reference
│   ├── architecture_alignment/
│   │   ├── HYBRID_APPROACH.md
│   │   ├── ARCHITECTURAL_PATTERNS.md
│   │   └── SERVICE_COMPATIBILITY.md
│   ├── merge_strategy/
│   │   ├── FINAL_MERGE_STRATEGY.md
│   │   ├── HANDLING_INCOMPLETE_MIGRATIONS.md
│   │   └── CONFLICT_RESOLUTION.md
│   ├── implementation_lessons/
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── BEST_PRACTICES.md
│   │   ├── COMMON_PITFALLS.md
│   │   └── LESSONS_LEARNED.md
│   └── phase_findings/
│       ├── phase_001_framework_strategy/
│       ├── phase_002_validation_framework/
│       ├── phase_003_pre_merge_validation/
│       ├── phase_004_branch_alignment/
│       ├── phase_005_error_detection/
│       ├── phase_006_backup_restore/
│       ├── phase_007_branch_identification/
│       └── phase_008_documentation_automation/
│
├── execution/                          # 🆕 Execution planning & coordination
│   ├── README.md                       # Execution overview
│   ├── EXECUTION_STRATEGIES.md         # 🆕 Sequential vs Parallel vs Hybrid
│   ├── CRITICAL_PATH.md                # 🆕 16-18 week baseline timeline
│   ├── PARALLEL_EXECUTION.md           # 🆕 8-10 week with 5 teams
│   ├── TEAM_ALLOCATION.md              # 🆕 Who does which task
│   ├── MILESTONE_DATES.md              # 🆕 Weekly sync points
│   ├── RISK_ANALYSIS.md                # 🆕 Blockers and dependencies
│   └── DEPENDENCY_MATRIX.md            # 🆕 All 26 tasks cross-referenced
│
├── progress/                           # 🆕 Team progress tracking (optional)
│   ├── README.md                       # Progress tracking overview
│   ├── TEAM_A_TASK_001_PROGRESS.md     # Template: one per active team
│   ├── TEAM_B_TASK_021_PROGRESS.md     # Created as teams start
│   └── COMPLETION_STATUS.md            # Master status by task
│
├── reference/                          # Reference materials
│   ├── README.md                       # Reference overview
│   ├── task_mapping.md                 # 🔄 Old ID → New ID conversion
│   ├── CLEAN_TASK_INDEX.md             # 🔄 Task status and priority
│   ├── complete_new_task_outline_ENHANCED.md  # 🔄 Full specs (archive)
│   ├── INTEGRATION_EXECUTION_CHECKLIST.md     # 🔄 Week-by-week (archive)
│   ├── HANDOFF_INDEX.md                # 🔄 Task 021 strategy (archive)
│   └── TASK_STRUCTURE_STANDARD.md      # 📋 14-section template
│
└── archive/                            # 🆕 Historical & deprecated
    ├── README.md                       # Archive explanation
    ├── v1_planning/                    # First version documents
    ├── v2_iteration/                   # Second version documents
    └── deprecated/                     # Old files (reference only)
```

---

## Directory Purposes and Usage

### 🎯 task_files/ (Main Work Area)

**Purpose:** All executable task specifications  
**Access Pattern:** Agents pick a file, read it completely, implement it  
**Who Uses It:** Development teams (primary users)  
**Update Frequency:** Updated as work progresses (progress logging)

**Structure:**
```
task_files/
├── README.md           # "Start here: how to use task files"
├── task-XXX.md         # Main task overview (parent)
└── task-XXX-Y.md       # Individual subtask (self-contained)
```

**Key Principle:** Each task-XXX-Y.md file is **completely self-contained**
- No need to read task-XXX.md first (optional for context only)
- No need to read related task-XXX-Z.md files
- No need to read other initiative files
- Everything needed is in that one file

**Example Workflow:**
```
Agent picks task-021-4.md (BranchClusterer)
├── Opens file, reads Purpose
├── Reviews Success Criteria
├── Reads What to Build (spec)
├── Follows Implementation Guide step-by-step
├── Runs Test Cases
├── Logs progress in Progress Tracking section
└── Marks complete when all Success Criteria checked

Meanwhile:
Agent B picks task-002-5.md (IntegrationTargetAssigner) 
└── Works independently, no coordination needed
```

---

### 💡 guidance/ (Architectural Guidance & Findings)

**Purpose:** Context, patterns, lessons learned  
**Access Pattern:** Referenced from "Implementation Considerations" section in each task file  
**Who Uses It:** Developers needing background or struggling with implementation  
**Update Frequency:** Rarely changes (reference material)

**Subdirectories:**

#### guidance/architecture_alignment/
```
├── HYBRID_APPROACH.md                # Service compatibility patterns
├── ARCHITECTURAL_PATTERNS.md         # Common patterns observed
├── SERVICE_COMPATIBILITY.md          # Factory pattern, adapter patterns
└── IMPORT_PATH_STANDARDS.md          # Directory structure conventions
```
**Referenced by:** Tasks 001-003 (Foundational phase)

#### guidance/merge_strategy/
```
├── FINAL_MERGE_STRATEGY.md           # Overall merge philosophy
├── HANDLING_INCOMPLETE_MIGRATIONS.md # What if a branch is incomplete?
├── CONFLICT_RESOLUTION.md            # Merge conflict patterns
└── BRANCH_TARGETING.md               # How to choose integration target
```
**Referenced by:** Tasks 002-020 (Core framework phase)

#### guidance/implementation_lessons/
```
├── IMPLEMENTATION_SUMMARY.md         # What we learned
├── BEST_PRACTICES.md                 # Do these things
├── COMMON_PITFALLS.md                # Avoid these mistakes
├── LESSONS_LEARNED.md                # Detailed experience report
└── PERFORMANCE_OPTIMIZATION.md       # Tips for speed
```
**Referenced by:** All tasks (general guidance)

#### guidance/phase_findings/
```
├── phase_001_framework_strategy/     # Research findings
├── phase_002_validation_framework/   # What we discovered
├── phase_003_pre_merge_validation/   # Patterns and insights
├── phase_004_branch_alignment/       # ...continues for all phases
├── phase_005_error_detection/
├── phase_006_backup_restore/
├── phase_007_branch_identification/
└── phase_008_documentation_automation/
```
**Referenced by:** Specific tasks in each phase

---

### 📅 execution/ (Execution Planning & Coordination)

**Purpose:** Answer "how do we execute all 26 tasks?"  
**Access Pattern:** Team lead picks execution strategy, allocates work, tracks progress  
**Who Uses It:** Project managers, team leads, architects  
**Update Frequency:** Updated weekly with progress

**Files:**

```
execution/
├── EXECUTION_STRATEGIES.md     # Choose your execution mode
│   ├── Sequential (1 person, 6-8 weeks)
│   ├── Parallel (5 people, 8-10 weeks)
│   └── Hybrid (3 people, 10-12 weeks)
│
├── CRITICAL_PATH.md           # Which tasks block which?
│   ├── Task 001 → blocks everything
│   ├── Task 002 → blocks Tasks 004-020
│   ├── Task 021 → can run parallel with Task 001
│   └── Tasks 022-026 → wait for Tasks 001 & 021
│
├── PARALLEL_EXECUTION.md      # Detailed team schedule
│   ├── Week 1: Teams A, B, C, D on parallel tasks
│   ├── Week 2: Integration and sync
│   ├── Week 3-4: Next wave
│   └── ... continues
│
├── TEAM_ALLOCATION.md         # Who does what
│   ├── Team A (Task 001 framework)
│   ├── Team B (Task 021 Stage One parallel)
│   ├── Team C (Task 002 validation)
│   ├── Team D (Task 021 Stage One parallel)
│   └── Team E (Task 021 Stage One parallel)
│
├── MILESTONE_DATES.md         # Weekly sync points
│   ├── Week 1 Friday: Stage One outputs ready
│   ├── Week 2 Friday: Framework validation
│   ├── Week 3 Monday: Stage Two starts
│   └── ... continues
│
├── RISK_ANALYSIS.md           # What could go wrong?
│   ├── Task 002 depends on Task 001 completion
│   ├── Task 021 Stage Two depends on Stage One outputs
│   ├── Tasks 022-026 blocked until 001 & 021 done
│   └── Mitigation strategies
│
└── DEPENDENCY_MATRIX.md       # All 26 tasks cross-referenced
    └── Shows which task blocks which
```

---

### 📊 progress/ (Team Progress Tracking - Optional)

**Purpose:** Track work in progress across all teams  
**Access Pattern:** Teams log progress daily/weekly, leads check for blockers  
**Who Uses It:** Team leads, project manager  
**Update Frequency:** Daily by working teams

**Structure:**
```
progress/
├── README.md                     # How to use progress tracking
├── COMPLETION_STATUS.md          # Master status: task → % complete
├── TEAM_A_TASK_001_PROGRESS.md   # Created when team starts
├── TEAM_B_TASK_021_PROGRESS.md   # One per active team/task combo
├── WEEKLY_SYNC_NOTES.md          # Friday sync meeting minutes
└── BLOCKERS_AND_ISSUES.md        # Open issues and resolutions
```

**Example COMPLETION_STATUS.md:**
```
| Task | Subtasks | Started | Complete | Status | Owner |
|------|----------|---------|----------|--------|-------|
| 001  | 4        | Jan 7   | Jan 10   | ✅ 100% | Team A |
| 002  | 9        | Jan 9   | Jan 18   | 45%    | Team C |
| 021  | 9        | Jan 7   | Jan 27   | 60%    | Teams B,D,E |
| ...  | ...      | ...     | ...      | ...    | ... |
```

---

### 📚 reference/ (Reference Materials - Archive)

**Purpose:** Historical and reference information  
**Access Pattern:** Occasional lookup (context on decisions, old IDs, etc.)  
**Who Uses It:** Integration specialists, architects  
**Update Frequency:** Never (frozen)

**Files:**
```
reference/
├── task_mapping.md                    # Old ID → New ID lookup
├── CLEAN_TASK_INDEX.md               # Task status matrix
├── complete_new_task_outline_ENHANCED.md  # Original full specs
├── INTEGRATION_EXECUTION_CHECKLIST.md # Week-by-week plan
├── HANDOFF_INDEX.md                  # Task 021 (old Task 75) strategy
└── TASK_STRUCTURE_STANDARD.md        # 14-section template (frozen)
```

---

### 🗂️ archive/ (Historical - Do Not Use)

**Purpose:** Previous versions, deprecated files  
**Access Pattern:** Reference only (why decisions were made)  
**Who Uses It:** Archivists, historians  
**Update Frequency:** Never

**Structure:**
```
archive/
├── v1_planning/           # Original task planning (before extraction)
├── v2_iteration/          # Iteration updates
└── deprecated/            # Files no longer used
```

---

## Complete Directory Creation Plan

### What to Create (Phase 1-2)

```bash
# Phase 1: Already exists, already in task_files/
mkdir -p new_task_plan/task_files/
# ... task-001.md through task-026.md (main overviews)
# ... task-001-1.md through task-026-4.md (subtasks, ~130+ files)

# Phase 2: Create guidance/ (extract from task_data/)
mkdir -p new_task_plan/guidance/
mkdir -p new_task_plan/guidance/architecture_alignment/
mkdir -p new_task_plan/guidance/merge_strategy/
mkdir -p new_task_plan/guidance/implementation_lessons/
mkdir -p new_task_plan/guidance/phase_findings/
# ... copy 9 guidance docs + 14 phase findings directories

# Phase 3: Create execution/ (new from analysis)
mkdir -p new_task_plan/execution/
# ... create 7 execution planning documents

# Phase 4: Create optional directories
mkdir -p new_task_plan/progress/          # For tracking
mkdir -p new_task_plan/reference/         # Archive current docs
mkdir -p new_task_plan/archive/           # Historical only

# Phase 5: Create navigation documents
# ... create QUICK_START.md, NAVIGATION_GUIDE.md
```

---

## Navigation Guide Structure (NEW)

**Create NAVIGATION_GUIDE.md** (to help agents find what they need):

```markdown
# How to Navigate new_task_plan/

## "I'm a developer who just picked up a task"

→ Go to task_files/task-XXX-Y.md
→ Read the entire file (it's self-contained)
→ If you need background, check "Implementation Considerations" section
→ Follow the "Implementation Guide" step-by-step
→ Log progress in "Progress Tracking" section

## "I'm a team lead planning execution"

→ Go to execution/EXECUTION_STRATEGIES.md
→ Choose your strategy (Sequential, Parallel, or Hybrid)
→ Use execution/TEAM_ALLOCATION.md to assign tasks
→ Use progress/COMPLETION_STATUS.md to track

## "I need to understand a previous decision"

→ Go to reference/task_mapping.md for old ID conversions
→ Go to reference/CLEAN_TASK_INDEX.md for task status
→ Go to guidance/ for architectural context

## "I'm blocked and need guidance"

→ Check your task file's "Common Pitfalls" section
→ Check your task file's "Implementation Considerations" section
→ Search guidance/GUIDANCE_INDEX.md for relevant topic
→ Ask in BLOCKERS_AND_ISSUES.md

## "I need to know dependencies"

→ Go to execution/CRITICAL_PATH.md for overall structure
→ Go to execution/DEPENDENCY_MATRIX.md for details
→ Go to task_files/task-XXX.md for task-specific dependencies
```

---

## Isolated Task Completion: Example Workflows

### Workflow 1: Developer Starting Task 021-4.md (BranchClusterer)

```
Step 1: Navigate to task-021-4.md
        └─ Location: new_task_plan/task_files/task-021-4.md

Step 2: Read the file completely (self-contained)
        ├─ Section: Purpose (understand what to build)
        ├─ Section: Success Criteria (understand when done)
        ├─ Section: Prerequisites (what must be done first)
        ├─ Section: What to Build (specification)
        ├─ Section: Implementation Guide (how to build it)
        ├─ Section: Test Cases (how to verify)
        └─ Section: Implementation Considerations (links to guidance/)

Step 3: Check dependencies (can I start immediately?)
        └─ task-021-4 depends on: task-021-1, task-021-2, task-021-3
        └─ Decision: Are 021-1, 021-2, 021-3 complete?
           - If YES → start immediately
           - If NO → wait or work on independent task

Step 4: Reference guidance if needed
        └─ See "Implementation Considerations" section
        └─ Follow links to guidance/
        └─ Example: "See guidance/merge_strategy/CONFLICT_RESOLUTION.md"

Step 5: Implement following the guide
        ├─ Step-by-step in "Implementation Guide"
        ├─ Code examples in "Code Examples" section
        ├─ Handle edge cases in "Edge Cases" section
        └─ Validate with "Test Cases"

Step 6: Log progress
        ├─ Update "Progress Tracking" section in file
        ├─ Check off completed "Success Criteria"
        └─ Optional: Update progress/TEAM_B_TASK_021_PROGRESS.md

Step 7: Mark complete
        └─ All Success Criteria checked
        └─ All Test Cases passing
        └─ Update progress/COMPLETION_STATUS.md
```

### Workflow 2: Team Lead Planning Parallel Execution

```
Step 1: Choose execution strategy
        └─ Go to execution/EXECUTION_STRATEGIES.md
        └─ Review 3 options (Sequential, Parallel, Hybrid)
        └─ Recommend: Parallel (5 teams, 8-10 weeks)

Step 2: Allocate teams to tasks
        └─ Go to execution/TEAM_ALLOCATION.md
        └─ Assign Team A to Task 001
        └─ Assign Teams B, C, D to Task 021 Stage One (parallel)
        └─ Hold Teams E, F for Task 002 (waits for 001)

Step 3: Review critical path
        └─ Go to execution/CRITICAL_PATH.md
        └─ Understand: Task 001 blocks everything
        └─ Understand: Task 021 can run parallel with 001
        └─ Understand: Task 022-026 wait for both 001 & 021

Step 4: Plan milestones
        └─ Go to execution/MILESTONE_DATES.md
        └─ Schedule: Week 1 Friday - Stage One outputs
        └─ Schedule: Week 2 Friday - Framework validation
        └─ Schedule: Week 3 Monday - Stage Two starts

Step 5: Track progress
        └─ Create progress/TEAM_A_TASK_001_PROGRESS.md
        └─ Create progress/TEAM_B_TASK_021_PROGRESS.md
        └─ Create progress/TEAM_C_TASK_021_PROGRESS.md
        └─ Weekly update progress/COMPLETION_STATUS.md

Step 6: Monitor for blockers
        └─ Go to execution/RISK_ANALYSIS.md
        └─ Watch for: Task 002 depending on Task 001
        └─ Watch for: Stage Two depending on Stage One
        └─ Update progress/BLOCKERS_AND_ISSUES.md
```

### Workflow 3: Integration Specialist Checking Dependencies

```
Step 1: Look up old task IDs
        └─ Go to reference/task_mapping.md
        └─ Find: old Task 75 → new Task 021
        └─ Find: old Task 7 → new Task 001

Step 2: Understand task structure
        └─ Go to reference/CLEAN_TASK_INDEX.md
        └─ See: which tasks are high priority
        └─ See: which tasks are blocked
        └─ See: initiative grouping

Step 3: Check full dependency matrix
        └─ Go to execution/DEPENDENCY_MATRIX.md
        └─ See: all 26 tasks cross-referenced
        └─ Understand: critical path

Step 4: Verify compliance with standard
        └─ Go to reference/TASK_STRUCTURE_STANDARD.md
        └─ Verify: each task file has 14 sections
        └─ Verify: all requirements met
```

---

## Isolated Completion Features

### 1. Self-Contained Files
**Feature:** Each task-XXX-Y.md has everything needed  
**Benefit:** No need to understand other tasks  
**Implementation:** 14 mandatory sections in TASK_STRUCTURE_STANDARD.md

### 2. Minimal Cross-References
**Feature:** Files reference others only when necessary  
**Benefit:** Reduces coordination overhead  
**Implementation:** Links in "Dependencies" section and "Integration Points"

### 3. Parallel Execution Clarity
**Feature:** execution/PARALLEL_EXECUTION.md shows which tasks can run together  
**Benefit:** Teams know they can work independently  
**Implementation:** Color-coded task matrix by week

### 4. Progress Tracking Independence
**Feature:** Each team logs progress in their own file  
**Benefit:** No central bottleneck for updates  
**Implementation:** progress/TEAM_X_TASK_Y_PROGRESS.md template

### 5. Searchable Guidance
**Feature:** guidance/GUIDANCE_INDEX.md indexes all 9 + 14 phase documents  
**Benefit:** Developers can find answers without asking  
**Implementation:** Keyword index and navigation map

---

## Implementation Checklist

### Phase 1: Extract & Standardize (Days 1-2)
- [ ] Create task-002-1.md through task-002-9.md (extract from task-002.md)
- [ ] Rename task-002-clustering.md → task-021.md
- [ ] Create task-021-1.md through task-021-9.md (extract from task-021.md)
- [ ] Apply 14-section standard to all files
- [ ] Verify dash notation (task-XXX-Y.md)
- [ ] Create task_files/README.md (overview and usage guide)

### Phase 2: Integrate Guidance (Days 2-3)
- [ ] Create guidance/ directory structure
- [ ] Copy 9 guidance documents from task_data/guidance/
- [ ] Copy 14 phase findings from task_data/findings/
- [ ] Add "Implementation Considerations" section to each task
- [ ] Create guidance/GUIDANCE_INDEX.md (searchable)
- [ ] Create guidance/README.md (overview)

### Phase 3: Create Execution Plans (Days 3-4)
- [ ] Create execution/ directory
- [ ] Create execution/EXECUTION_STRATEGIES.md
- [ ] Create execution/CRITICAL_PATH.md
- [ ] Create execution/PARALLEL_EXECUTION.md
- [ ] Create execution/TEAM_ALLOCATION.md
- [ ] Create execution/MILESTONE_DATES.md
- [ ] Create execution/RISK_ANALYSIS.md
- [ ] Create execution/DEPENDENCY_MATRIX.md
- [ ] Create execution/README.md

### Phase 4: Create Navigation (Day 4)
- [ ] Create NAVIGATION_GUIDE.md (in root)
- [ ] Create QUICK_START.md (in root)
- [ ] Update README.md with new structure
- [ ] Create reference/README.md
- [ ] Move old docs to reference/ (keep, don't delete)
- [ ] Create archive/README.md (explanation only)

### Phase 5: Finalization
- [ ] Create progress/ directory (optional)
- [ ] Create progress/README.md
- [ ] Create progress/COMPLETION_STATUS.md template
- [ ] Validate all links and cross-references
- [ ] Final verification: all files complete and consistent

---

## Success Criteria for Folder Structure

✅ **Isolation**
- [ ] Developer can pick any task-XXX-Y.md file and work independently
- [ ] No need to understand adjacent tasks or initiatives
- [ ] All context available in the single file

✅ **Navigation**
- [ ] New person can follow NAVIGATION_GUIDE.md to find anything
- [ ] QUICK_START.md explains how to begin
- [ ] All cross-references valid and helpful

✅ **Parallel Execution**
- [ ] execution/PARALLEL_EXECUTION.md shows clear team allocation
- [ ] Each team knows their start date and dependencies
- [ ] No ambiguity about who works on what

✅ **Progress Tracking**
- [ ] progress/COMPLETION_STATUS.md has master view
- [ ] Each team can log independently
- [ ] No bottlenecks in status updates

✅ **Guidance Access**
- [ ] Every task has "Implementation Considerations" section
- [ ] guidance/GUIDANCE_INDEX.md is searchable
- [ ] Developers can find answers without asking

---

## Example Isolated Team Workflow

**Scenario: 5 teams, all starting on Day 1, no dependencies on each other for first 2 weeks**

```
Team A (Task 001 Framework)
├─ Starts Day 1 at 9am
├─ Work location: task_files/task-001-1.md through task-001-4.md
├─ Self-sufficient: reads files, implements, logs progress
└─ Reports status Friday to execution/COMPLETION_STATUS.md

Team B (Task 021 Stage One Part 1)
├─ Starts Day 1 at 9am
├─ Work location: task_files/task-021-1.md (CommitHistoryAnalyzer)
├─ Self-sufficient: independent analyzer, no cross-team coordination
└─ Reports status Friday to progress/TEAM_B_TASK_021_PROGRESS.md

Team C (Task 021 Stage One Part 2)
├─ Starts Day 1 at 9am
├─ Work location: task_files/task-021-2.md (CodebaseStructureAnalyzer)
├─ Self-sufficient: independent analyzer, no coordination needed
└─ Reports status Friday to progress/TEAM_C_TASK_021_PROGRESS.md

Team D (Task 021 Stage One Part 3)
├─ Starts Day 1 at 9am
├─ Work location: task_files/task-021-3.md (DiffDistanceCalculator)
├─ Self-sufficient: independent analyzer, no coordination needed
└─ Reports status Friday to progress/TEAM_D_TASK_021_PROGRESS.md

Team E (Task 002 Validation)
├─ Starts Day 1 at 9am (but waits for Task 001)
├─ Work location: task_files/task-002-1.md through task-002-9.md
├─ Can do design/spec work while waiting for Task 001 completion
└─ Reports status Friday to progress/TEAM_E_TASK_002_PROGRESS.md

Friday Week 1:
├─ Team A reports Task 001 progress to COMPLETION_STATUS.md
├─ Teams B, C, D report Stage One progress
├─ Team E confirms ready for Task 002
└─ Weekly sync meeting with all teams (no blockers so far)

Monday Week 2:
├─ Team A continues with remaining subtasks
├─ Teams B, C, D integrate outputs for task-021-4.md
├─ Team E still waiting for Task 001 completion
└─ No cross-team dependencies blocking anyone
```

---

## Folder Structure at Completion

```
new_task_plan/                                    (Root: all integrated)
│
├── README.md                                     (Updated: new structure)
├── QUICK_START.md                               (NEW: quick reference by role)
├── NAVIGATION_GUIDE.md                          (NEW: where is everything?)
│
├── task_files/                                  (Main work area)
│   ├── README.md
│   ├── task-001.md through task-026.md          (26 main overviews)
│   ├── task-001-1.md through task-001-4.md      (4 subtasks)
│   ├── task-002-1.md through task-002-9.md      (9 subtasks)
│   ├── task-003-1.md through task-020-5.md      (~60+ subtasks)
│   ├── task-021-1.md through task-021-9.md      (9 subtasks)
│   └── task-022-1.md through task-026-4.md      (~15 subtasks)
│
├── guidance/                                    (Architectural guidance)
│   ├── README.md
│   ├── GUIDANCE_INDEX.md
│   ├── architecture_alignment/                  (4 docs)
│   ├── merge_strategy/                          (3 docs)
│   ├── implementation_lessons/                  (4 docs)
│   └── phase_findings/                          (14 phase dirs)
│
├── execution/                                   (Execution planning)
│   ├── README.md
│   ├── EXECUTION_STRATEGIES.md
│   ├── CRITICAL_PATH.md
│   ├── PARALLEL_EXECUTION.md
│   ├── TEAM_ALLOCATION.md
│   ├── MILESTONE_DATES.md
│   ├── RISK_ANALYSIS.md
│   └── DEPENDENCY_MATRIX.md
│
├── progress/                                    (Progress tracking, optional)
│   ├── README.md
│   ├── COMPLETION_STATUS.md
│   ├── TEAM_A_TASK_001_PROGRESS.md
│   ├── TEAM_B_TASK_021_PROGRESS.md
│   ├── ... (one per active team)
│   └── BLOCKERS_AND_ISSUES.md
│
├── reference/                                   (Historical reference)
│   ├── README.md
│   ├── task_mapping.md                 (Updated)
│   ├── CLEAN_TASK_INDEX.md             (Updated)
│   ├── complete_new_task_outline_ENHANCED.md
│   ├── INTEGRATION_EXECUTION_CHECKLIST.md
│   ├── HANDOFF_INDEX.md
│   └── TASK_STRUCTURE_STANDARD.md
│
└── archive/                                     (Historical only)
    ├── README.md
    ├── v1_planning/                    (Old planning docs)
    ├── v2_iteration/                   (Iteration updates)
    └── deprecated/                     (Don't use)
```

---

## Key Design Decisions

### Decision 1: Why Separate guidance/ Directory?
**Options considered:**
- A) Put guidance in each task file (duplicated, scattered)
- B) Keep guidance in task_data/ (separate from work area)
- C) Create new_task_plan/guidance/ (integrated, accessible)

**Decision: C**
- **Rationale:** Developers can find guidance without leaving new_task_plan/
- **Benefit:** Self-contained working directory
- **Tradeoff:** Small duplication (9 docs copied, not symlinked for independence)

### Decision 2: Why Separate execution/ Directory?
**Options considered:**
- A) Put in task files (clutters individual task files)
- B) Put in reference/ (suggests it's historical)
- C) Create separate execution/ (indicates it's active)

**Decision: C**
- **Rationale:** Team leads need to find execution planning quickly
- **Benefit:** Clear separation between work and planning
- **Tradeoff:** Slight duplication of info (task dependencies listed in 2 places)

### Decision 3: Why Optional progress/ Directory?
**Options considered:**
- A) Require all teams to update central status (bottleneck)
- B) Each team maintains local progress (no central visibility)
- C) Optional progress/ directory for teams that want it

**Decision: C**
- **Rationale:** Some teams may prefer project management tools (Jira, Asana)
- **Benefit:** Flexibility for different team preferences
- **Tradeoff:** Less central visibility if not all teams use it

### Decision 4: Why Not Symlinks for guidance/?
**Considered:** `ln -s ../task_data/guidance new_task_plan/guidance`

**Decision: Copy, not symlink**
- **Rationale:** new_task_plan must be independent and portable
- **Benefit:** Can be zipped/archived without external dependencies
- **Tradeoff:** Small duplication (9 docs, ~50KB total)

---

## Notes for Implementation

1. **Folder Creation Order:**
   - Phase 1: task_files/ (already exists, add task files)
   - Phase 2: guidance/ (create and extract)
   - Phase 3: execution/ (create and write)
   - Phase 4: reference/ (organize existing docs)
   - Phase 5: progress/, archive/ (optional, create as needed)

2. **Documentation in Each Folder:**
   - Every folder should have README.md
   - Explains purpose, contents, usage
   - Links to related documents

3. **Cross-References:**
   - task files → guidance/ (Implementation Considerations)
   - task files → task dependencies (within file)
   - execution/ → task files (which team does what)
   - progress/ → execution/ (tracking milestone dates)

4. **Search and Navigation:**
   - NAVIGATION_GUIDE.md is the entry point
   - QUICK_START.md is for quick reference
   - GUIDANCE_INDEX.md is for finding topics
   - task_files/README.md explains how to use individual files

---

## Validation Checklist

✅ Can a developer pick task-021-4.md and complete it without reading other files?
- [ ] Yes - all context is in the file
- [ ] All dependencies are listed
- [ ] All guidance is linked

✅ Can a team lead plan parallel execution?
- [ ] Yes - execution/PARALLEL_EXECUTION.md shows team allocation
- [ ] CRITICAL_PATH.md shows dependencies
- [ ] TEAM_ALLOCATION.md shows assignments

✅ Can a developer find guidance on a topic?
- [ ] Yes - guidance/GUIDANCE_INDEX.md is searchable
- [ ] task files link to relevant guidance
- [ ] No need to ask others

✅ Can a team track progress independently?
- [ ] Yes - progress/COMPLETION_STATUS.md has master view
- [ ] Each team can update their own file
- [ ] No central bottleneck

✅ Can someone understand old decisions?
- [ ] Yes - reference/ has all historical documents
- [ ] task_mapping.md explains old→new ID conversions
- [ ] Nothing is deleted, just archived

---

**Document Version:** 1.0  
**Created:** January 6, 2026  
**Status:** READY FOR IMPLEMENTATION  
**Purpose:** Folder structure for isolated task completion  
**Next Step:** Create folders following Phase 1-5 checklist
