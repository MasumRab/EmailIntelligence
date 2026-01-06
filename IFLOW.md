# iFlow CLI Context File

## Project Overview

**Project Name:** EmailIntelligence - Branch Alignment & Integration System  
**Current Phase:** Phase 3 - Alignment Framework Specification Complete  
**Project Type:** Software Engineering Project (Python + Git Workflow Management System)  
**Primary Tech Stack:** Python 3.8+, Git, Task Master AI, Claude Code, MCP (Model Context Protocol)

### Project Core Objectives

The EmailIntelligence project is a branch alignment and integration system designed to solve multi-branch management, code alignment, and integration automation challenges in large Git repositories. The project is currently in Phase 3, having completed the specification definition for the alignment framework and ready to begin implementation.

### Current Status

- ✅ **Phase 1-2:** Code recovery + branch clustering pipeline (assumed complete)
- ✅ **Phase 3:** Specifications 100% complete and standardized
  - 9 task files fully retrofitted to TASK_STRUCTURE_STANDARD.md
  - Located in `/tasks/` directory
  - Task 007, Task 075.1-5, Task 079-083
  - All success criteria documented
  - All sub-subtasks detailed with effort estimates
  - Total effort: 92-120 hours
- 🔄 **Documentation cleanup:** 101 outdated files archived, 13 active files remain (6% of original)
- 🔄 **Consolidation planning:** GAP identified (tasks in `/tasks/` but should be in `new_task_plan/task_files/`)
- ⏭️ **Next steps:** Consolidate tasks (Phase 1-7, ~5 hours), then begin Phase 3 implementation

---

## Project Structure

```
.taskmaster/
├── archive/                    # Archived documentation (historical reference)
│   ├── ARCHIVE_MANIFEST.md
│   ├── cleanup_work/
│   ├── deprecated_numbering/
│   ├── integration_work/
│   ├── investigation_work/
│   ├── phase_planning/
│   ├── project_docs/
│   ├── retrofit_work/
│   └── task_context/
├── backups/                    # Backup files
├── docs/                       # Documentation directory
│   ├── AGENTIC_CONTAMINATION_ANALYSIS.md
│   ├── branch-alignment-aggregated-documentation.md
│   ├── branch-alignment-framework-prd.txt
│   ├── CODE_FORMATTING.md
│   ├── CONTAMINATION_DOCUMENTATION_INDEX.md
│   ├── CONTAMINATION_INCIDENTS_SUMMARY.md
│   ├── EXTERNAL_DATA_REFERENCES.md
│   ├── FORMATTING_STATUS.md
│   ├── master-prd.txt
│   ├── MERGE_GUIDANCE_DOCUMENTATION.md
│   ├── orchestration_summary.md
│   ├── PREVENTION_FRAMEWORK.md
│   ├── TASK_7_PURPOSE_CLARIFICATION.md
│   ├── TASK_CLASSIFICATION_SYSTEM.md
│   ├── TASK_INTERPRETATION_FINDING_TASK7.md
│   ├── archive/
│   ├── branch_alignment/
│   └── research/
├── guidance/                   # Guidance documentation
│   ├── ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md
│   ├── ARCHITECTURE_ALIGNMENT_IMPLEMENTATION_GUIDE.md
│   ├── COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md
│   ├── FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md
│   ├── FINAL_MERGE_STRATEGY.md
│   ├── HANDLING_INCOMPLETE_MIGRATIONS.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── MERGE_GUIDANCE_DOCUMENTATION.md
│   ├── OPERATIONAL_PROCEDURES_GUIDELINES.md
│   ├── QUICK_REFERENCE_GUIDE.md
│   ├── README.md
│   ├── SECURITY_ERROR_TESTING_GUIDELINES.md
│   ├── SUMMARY.md
│   ├── validate_architecture_alignment.py
│   └── src/
├── implement/                  # Implementation status
│   └── state.json
├── new_task_plan/              # New task plan
│   ├── COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md
│   ├── ISOLATED_ENVIRONMENT_SPECIFICATION.md
│   ├── LOGGING_GUIDE.md
│   ├── LOGGING_SYSTEM_PLAN.md
│   ├── SCRIPTS_AND_TOOLS_INTEGRATION.md
│   ├── SUBTASK_EXPANSION_TEMPLATE.md
│   ├── TASK_DEPENDENCY_VISUAL_MAP.md
│   ├── task_mapping.md
│   ├── TASK_NUMBERING_ANALYSIS.md
│   ├── task-001.md
│   ├── task-002-1.md through task-002-9.md
│   ├── task-002.md
│   ├── task-003.md through task-026.md
│   ├── archive/
│   ├── execution/
│   ├── guidance/
│   ├── planning_docs/
│   ├── progress/
│   └── reference/
├── refactor/                   # Refactoring status
│   └── state.json
├── reports/                    # Reports
│   └── task-complexity-report.json
├── scripts/                    # Automation scripts
│   ├── compare_task_files.py
│   ├── compress_progress.py
│   ├── compress_progress.sh
│   ├── disable-hooks.sh
│   ├── enhance_tasks_from_archive.py
│   ├── expand_subtasks.py
│   ├── find_lost_tasks.py
│   ├── format_code.sh
│   ├── generate_clean_tasks.py
│   ├── list_invalid_tasks.py
│   ├── list_tasks.py
│   ├── markdownlint_check.py
│   ├── next_task.py
│   ├── query_findings.py
│   ├── README_TASK_SCRIPTS.md
│   ├── README.md
│   ├── regenerate_tasks_from_plan.py
│   ├── reverse_sync_orchestration.sh
│   ├── search_tasks.py
│   ├── show_task.py
│   ├── split_enhanced_plan.py
│   ├── sync_setup_worktrees.sh
│   ├── task_summary.py
│   └── update_flake8_orchestration.sh
├── task_data/                  # Task data
│   ├── 00_START_HERE.md
│   ├── 00_TASK_STRUCTURE.md
│   ├── BRANCH_ALIGNMENT_TASKS.json
│   ├── branch_clustering_framework.md
│   ├── branch_clustering_implementation.py
│   ├── CLUSTERING_SYSTEM_SUMMARY.md
│   ├── DELIVERY_CHECKLIST.md
│   ├── HANDOFF_DELIVERY_SUMMARY.md
│   ├── HANDOFF_INDEX.md
│   ├── HANDOFF_INTEGRATION_PLAN.md
│   ├── INTEGRATION_COMPLETE.md
│   ├── INTEGRATION_COMPLETE.txt
│   ├── INTEGRATION_EXAMPLE.md
│   ├── INTEGRATION_PHASE_COMPLETE.txt
│   ├── INTEGRATION_QUICK_REFERENCE.md
│   ├── INTEGRATION_STRATEGY.md
│   ├── INTEGRATION_SUMMARY.txt
│   ├── orchestration_branches.json
│   ├── QUICK_START.md
│   ├── README.md
│   ├── TASK_BREAKDOWN_GUIDE.md
│   ├── TASK_MASTER_AI_WORKFLOW.md
│   ├── task-7.md
│   ├── validate_integration.sh
│   ├── archived/
│   ├── archived_handoff/
│   ├── backups/
│   ├── compressed/
│   └── findings/
├── task_scripts/               # Task scripts
├── tasks/                      # Task files
├── templates/                  # Template files
├── .agent_memory/              # Agent memory
├── .backups/                   # Backups
├── .git/                       # Git repository
├── .qwen/                      # Qwen configuration
├── .ruff_cache/                # Ruff cache
├── .taskmaster/                # Task Master configuration
├── AGENT.md                    # Agent integration guide
├── AGENTS.md                   # System agent guidance
├── ARCHIVE_INVESTIGATION_FINDINGS.md
├── ARCHIVE_INVESTIGATION_SUMMARY.md
├── CLAUDE.md                   # Auto-loaded context for Claude Code
├── config.json                 # AI model configuration
├── CURRENT_DOCUMENTATION_MAP.md
├── CURRENT_SYSTEM_STATE_DIAGRAM.md
├── DOCUMENTATION_CLEANUP_COMPLETE.md
├── execute_phases_2_4.py
├── EXECUTION_SUMMARY.txt
├── HANDOFF_HISTORY_AND_MISTAKES_ANALYSIS.md
├── IFLOW.md                    # This file
├── integrate_remaining_tasks.py
├── INVESTIGATION_SUMMARY_COMPLETE.md
├── MEMORY_API_FOR_TASKS.md
├── MIGRATION_STATUS_ANALYSIS.md
├── OLD_TASK_NUMBERING_DEPRECATED.md
├── opencode.json
├── PROJECT_STATUS_SUMMARY.md
├── pyproject.toml              # Python project configuration
├── READ_THIS_FIRST_INVESTIGATION_INDEX.md
├── README.md                   # Project overview
├── ROOT_DOCUMENTATION_CLEANUP_PLAN.md
├── SCRIPTS_IN_TASK_WORKFLOW.md
├── state.json                  # State file
├── SUBTASK_MARKDOWN_TEMPLATE.md
├── TASK_7_DELIVERY_SUMMARY.txt
├── TASK_7_ENHANCEMENT_SUMMARY.txt
├── TASK_EXPANSION_PLAN_BY_WEEK.md
├── TASK_STRUCTURE_STANDARD.md  # Task structure standard
├── TEMPLATE_MIGRATION_PATTERNS_AND_BLOCKERS.md
├── test_refactoring_modes.py
├── TODO_STRUCTURE.txt
└── VERIFICATION_SUMMARY.txt
```

---

## Key Files Description

### Configuration Files

- **config.json** - Task Master AI configuration file
  - Contains AI model configuration (main, research, fallback)
  - Uses Gemini 2.5 Flash models
  - Global settings: log level, default task count, priority, etc.

- **pyproject.toml** - Python project configuration
  - Black code formatting configuration (line length 100)
  - Ruff code checking configuration
  - Target Python versions: 3.8-3.12

- **state.json** - Project state file
  - Current tag: master
  - Branch tag mapping
  - Migration notice status

### Documentation Files

- **README.md** - Project overview and navigation
  - Task system restructuring documentation
  - Critical updates: task classification system
  - New workflow structure
  - Critical focus areas

- **PROJECT_STATUS_SUMMARY.md** - Project status summary (1-page)
  - Current state overview
  - Quick facts
  - Task structure
  - How to get started
  - Key documents
  - Risks and mitigations
  - Success criteria
  - Next actions

- **TASK_STRUCTURE_STANDARD.md** - Task structure standard
  - Detailed description of 14 required sections
  - One file per subtask
  - Naming convention: task_XXX.Y.md
  - Success criteria, prerequisites, sub-subtask breakdown, etc.

- **CURRENT_DOCUMENTATION_MAP.md** - Current documentation map
  - Reading guide by role
  - Project manager, developer, architect, AI agent
  - Categorized by document type
  - Quick lookup table
  - Active documentation checklist

- **AGENT.md** - Agent integration guide
  - Task Master AI core workflow commands
  - Key files and project structure
  - Claude Code integration files
  - MCP integration
  - Script integration
  - Best practices

- **CLAUDE.md** - Auto-loaded context for Claude Code
  - Similar content to AGENT.md
  - Optimized specifically for Claude Code

### Task Data

- **task_data/README.md** - Two-stage branch clustering system complete implementation package
  - Documentation overview
  - Key concepts (30-second summary)
  - System architecture at a glance
  - File structure
  - Implementation timeline
  - Success metrics
  - Integration points
  - Output specifications
  - Configuration parameters
  - Tag system reference
  - Quick start checklist

- **task_data/branch_clustering_framework.md** - Branch clustering framework design
  - Two-stage clustering approach in detail
  - Metric definitions and calculations
  - Heuristic rules and decision trees
  - Configuration and thresholds
  - Integration patterns

- **task_data/branch_clustering_implementation.py** - Production-ready Python implementation
  - 4000+ lines of production code
  - 5 main classes with full implementations
  - Error handling and logging
  - Ready for unit testing

### Script Files

- **scripts/README.md** - Scripts directory usage guide
  - Quick start
  - Script categories
  - Common workflows
  - Security considerations
  - Troubleshooting
  - File structure
  - Dependencies
  - Best practices

Script categories:
1. **Task Management Scripts (Python)**
   - list_tasks.py - List tasks
   - show_task.py - Show task details
   - next_task.py - Find next task
   - search_tasks.py - Search tasks
   - task_summary.py - Generate task summary
   - compare_task_files.py - Compare task files
   - list_invalid_tasks.py - List invalid tasks
   - generate_clean_tasks.py - Generate clean task files
   - enhance_tasks_from_archive.py - Enhance tasks from archive
   - split_enhanced_plan.py - Split enhanced plan
   - regenerate_tasks_from_plan.py - Regenerate tasks from plan
   - find_lost_tasks.py - Find lost tasks in git history

2. **Orchestration and Setup Scripts (Bash)**
   - disable-hooks.sh - Disable Git hooks
   - sync_setup_worktrees.sh - Sync setup files
   - reverse_sync_orchestration.sh - Reverse sync to orchestration-tools
   - update_flake8_orchestration.sh - Update .flake8 configuration

### Guidance Documentation

- **guidance/README.md** - EmailIntelligence architecture alignment and CLI integration guidance
  - Files overview
  - Usage instructions
  - Key principles
  - Common scenarios addressed
  - Best practices

---

## Building and Running

### Environment Requirements

- Python 3.8+
- Git
- Node.js (for MCP server)
- At least one AI API key:
  - ANTHROPIC_API_KEY (recommended)
  - PERPLEXITY_API_KEY (highly recommended)
  - OPENAI_API_KEY
  - GOOGLE_API_KEY
  - MISTRAL_API_KEY
  - OPENROUTER_API_KEY
  - XAI_API_KEY

### Installation and Configuration

1. **Initialize Task Master**
```bash
task-master init
```

2. **Configure AI Models**
```bash
task-master models --setup
```

3. **Parse PRD Document**
```bash
task-master parse-prd .taskmaster/docs/prd.md
```

4. **Analyze Complexity and Expand Tasks**
```bash
task-master analyze-complexity --research
task-master expand --all --research
```

### Daily Development Workflow

```bash
# View all tasks
task-master list

# Get next task
task-master next

# Show task details
task-master show <id>

# Mark task in progress
task-master set-status --id=<id> --status=in-progress

# Update subtask
task-master update-subtask --id=<id> --prompt="implementation notes..."

# Mark task complete
task-master set-status --id=<id> --status=done
```

### Using Scripts

```bash
# View next task
python scripts/next_task.py

# Search for tasks
python scripts/search_tasks.py "keyword"

# Generate task summary
python scripts/task_summary.py

# Sync setup files
./scripts/sync_setup_worktrees.sh --dry-run
./scripts/sync_setup_worktrees.sh

# Disable hooks
./scripts/disable-hooks.sh
```

### Code Formatting and Checking

```bash
# Format code with Black
black --line-length 100 .

# Check code with Ruff
ruff check .
ruff check --fix .

# Format all code
./scripts/format_code.sh
```

---

## Development Conventions

### Code Style

- **Python Code:**
  - Follow PEP 8 standards
  - Use Black for formatting (line length 100)
  - Use Ruff for code checking
  - Target test coverage: > 95%

- **Markdown Documentation:**
  - Use consistent heading structure
  - Include necessary metadata (status, date, version)
  - Use tables and lists for readability
  - Include code examples and usage instructions

### Task Structure

All tasks must follow the 14 sections defined in **TASK_STRUCTURE_STANDARD.md**:

1. Task Header
2. Overview/Purpose
3. Success Criteria (detailed)
4. Prerequisites & Dependencies
5. Sub-subtasks Breakdown
6. Specification Details
7. Implementation Guide
8. Configuration Parameters
9. Performance Targets
10. Testing Strategy
11. Common Gotchas & Solutions
12. Integration Checkpoint
13. Done Definition
14. Next Steps

### Naming Conventions

- **Task Files:** task_XXX.Y.md (e.g., task_002.1.md)
- **Branch Names:** feature/xxx, bugfix/xxx, refactor/xxx
- **Commit Messages:** feat:, fix:, docs:, style:, refactor:, test:, chore:
- **Variable Naming:** snake_case
- **Class Naming:** PascalCase
- **Constant Naming:** UPPER_CASE

### Git Workflow

1. **Feature Development:**
```bash
git checkout -b feature/your-feature
# Develop...
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

2. **Bug Fixes:**
```bash
git checkout -b bugfix/your-bugfix
# Fix...
git add .
git commit -m "fix: resolve the bug"
git push origin bugfix/your-bugfix
```

3. **Parallel Development with Worktrees:**
```bash
git worktree add ../project-auth feature/auth-system
git worktree add ../project-api feature/api-refactor
```

### Testing Practices

- **Unit Tests:** At least 8 test cases per feature
- **Integration Tests:** Verify cross-feature integration
- **End-to-End Tests:** Verify complete workflows
- **Coverage Target:** > 95%
- **Performance Tests:** Verify performance targets (e.g., < 2 seconds/branch)

### Documentation Practices

- **Code Documentation:** Use docstrings to describe functions and classes
- **Task Documentation:** Follow TASK_STRUCTURE_STANDARD.md
- **API Documentation:** Include usage examples
- **Architecture Documentation:** Describe design decisions and trade-offs
- **Change Logs:** Record important changes

---

## Phase 3 Task Overview

### Current Phase: Phase 3 - Alignment Framework Specification Complete

### Active Tasks (9)

1. **Task 007: Branch Alignment Strategy** (40-48 hours)
   - 007.1: Identify All Active Feature Branches
   - 007.2: Analyze Git History and Codebase Similarity
   - 007.3: Define Target Selection Criteria
   - 007.4: Propose Optimal Targets with Justifications
   - 007.5: Create ALIGNMENT_CHECKLIST.md
   - 007.6: Define Merge vs Rebase Strategy
   - 007.7: Create Architectural Prioritization Guidelines
   - 007.8: Define Safety and Validation Procedures

2. **Task 075.1-5: Alignment Analyzers** (120-152 hours)
   - 075.1: CommitHistoryAnalyzer (24-32 hours)
   - 075.2: CodebaseStructureAnalyzer (28-36 hours)
   - 075.3: DiffDistanceCalculator (32-40 hours)
   - 075.4: BranchClusterer (28-36 hours)
   - 075.5: IntegrationTargetAssigner (24-32 hours)

3. **Task 079: Parallel Alignment Orchestration Framework** (24-32 hours)

4. **Task 080: Pre-merge Validation Framework** (20-28 hours)

5. **Task 083: E2E Testing & Reporting Framework** (28-36 hours)

### Total Effort: 92-120 hours (2-3 weeks of team work)

---

## Key Concepts

### Task Classification System

**Critical Distinction: Process Tasks vs. Feature Development Tasks**

#### **Alignment Process Tasks (74-83):**
- **Are NOT** feature development tasks requiring individual branches
- **Define** procedures and tools for the core alignment workflow
- **Should be implemented** as part of the alignment process on target branches
- **Create** the framework that will be applied to other feature branches
- **Contribute to** the alignment infrastructure rather than being independent features

#### **Feature Development Tasks (All others):**
- **ARE** feature development work that typically requires dedicated branches
- **Implement** specific features, fixes, or refactoring as independent work items
- **Follow** standard development workflow with dedicated feature branches
- **Will be aligned** to primary branches using the framework created by Tasks 74-83

### Branch Clustering System

**Two-Stage Clustering Approach:**

**Stage One:** Cluster branches by similarity
- **Commit History** (35%): How long diverged, activity level, shared authors
- **Codebase Structure** (35%): What files changed, which core areas affected
- **Diff Distance** (30%): File overlap, change proximity, conflict probability

**Stage Two:** Assign targets and tags
- **Target Assignment:** main | scientific | orchestration-tools
- **Tagging System:** 30+ comprehensive tags (primary target, execution context, complexity, content types, validation needs, workflow)

### MCP (Model Context Protocol) Integration

Task Master provides an MCP server that Claude Code can connect to.

**MCP Tool Tiers:**
- **core** (7 tools): get_tasks, next_task, get_task, set_task_status, update_subtask, parse_prd, expand_task
- **standard** (14 tools): core + initialize_project, analyze_project_complexity, expand_all, add_subtask, remove_task, add_task, complexity_report
- **all** (44+ tools): standard + dependencies, tags, research, autopilot, scoping, models, rules

---

## How to Get Started

### For Implementation Team

1. Read: `PROJECT_STATE_PHASE_3_READY.md` (30 min)
2. Read: `TASK_STRUCTURE_STANDARD.md` (20 min)
3. Read: Your specific task file (in `/tasks/`) (30 min)
4. Begin implementation

### For Project Manager

1. Read: `PROJECT_STATE_PHASE_3_READY.md` (30 min)
2. Review: `CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md` (25 min)
3. Plan: 5-hour consolidation work
4. Allocate: 2-3 developers for 3-4 weeks

### For Architect

1. Read: `PROJECT_STATE_PHASE_3_READY.md` (30 min)
2. Review: `new_task_plan/task_files/task_007.md` + `new_task_plan/task_files/task_075.1-5.md` (30 min)
3. Review: `CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md` (25 min)
4. Approve: Task architecture and consolidation plan

---

## Frequently Asked Questions

### "What's the current status?"
See PROJECT_STATUS_SUMMARY.md - Phase 3 specs complete, ready to implement

### "When can we start?"
Immediately after consolidation (~5 hours of work)

### "How long will it take?"
3-4 weeks (with 2-3 developers)

### "What's the first task?"
Task 007: Branch Alignment Strategy

### "Where are the tasks?"
`/tasks/task_007.md`, `/tasks/task_075.1-5.md`, `/tasks/task_079-083.md`

### "What do I read first?"
PROJECT_STATE_PHASE_3_READY.md (30 min)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Teams use old task numbering (001-020) | Wrong task implementation | ✅ Deprecation notice in place |
| Confusion about task locations | Fragmented work | ✅ Consolidation planned |
| Old documentation contradicts new | Wrong decisions | ✅ Archive created, outdated docs removed |
| Task dependencies missed | Blocked work | ✅ Dependencies documented in PROJECT_STATE_PHASE_3_READY.md |

---

## Success Criteria

Phase 3 implementation is **successful when:**

1. ✅ All 9 tasks implemented and tested
2. ✅ > 95% unit test coverage
3. ✅ Cross-task integration verified
4. ✅ Code reviewed and approved
5. ✅ Performance targets met
6. ✅ E2E testing complete
7. ✅ Ready for Phase 4 execution

**Typical timeline:** 3-4 weeks (with 2-3 developers)

---

## Next Actions

### Immediate (This Week)
- [ ] Executive review of this summary
- [ ] Begin consolidation work (CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md)
- [ ] Allocate team members for Phase 3

### Short Term (Next Week)
- [ ] Complete consolidation (move tasks to `new_task_plan/task_files/`)
- [ ] Update all documentation references
- [ ] Begin Task 007 implementation
- [ ] Schedule weekly syncs for team coordination

### Medium Term (Weeks 2-4)
- [ ] Complete Task 007 (1 week)
- [ ] Complete Task 075.1-5 (2-3 weeks, parallelizable)
- [ ] Begin Task 079-083 (sequential)
- [ ] Code review & approval

---

## Resources and Links

### Core Documentation
- [README.md](./README.md) - Project overview
- [PROJECT_STATUS_SUMMARY.md](./PROJECT_STATUS_SUMMARY.md) - Project status summary
- [TASK_STRUCTURE_STANDARD.md](./TASK_STRUCTURE_STANDARD.md) - Task structure standard
- [CURRENT_DOCUMENTATION_MAP.md](./CURRENT_DOCUMENTATION_MAP.md) - Current documentation map

### Agent Documentation
- [AGENT.md](./AGENT.md) - Agent integration guide
- [AGENTS.md](./AGENTS.md) - System agent guidance
- [CLAUDE.md](./CLAUDE.md) - Claude Code context

### Script Documentation
- [scripts/README.md](./scripts/README.md) - Scripts usage guide

### Guidance Documentation
- [guidance/README.md](./guidance/README.md) - Architecture alignment and CLI integration guidance

### Task Data
- [task_data/README.md](./task_data/README.md) - Branch clustering system implementation package

---

## Last Updated

**Date:** January 6, 2026  
**Status:** ✅ Ready for Phase 3 Implementation  
**Next Step:** Create Task Master subtasks and begin implementation

---

**This file provides necessary context for iFlow CLI to effectively assist with project development in future interactions.**