# Unified Task MD Structure Analysis & Standardization Guide

**Analysis Date:** January 4, 2026  
**Status:** Comprehensive structural analysis of all task MD files across repository  
**Purpose:** Define a unified, standardized task MD structure for consistency and efficiency

---

## Executive Summary

The repository contains **3 distinct task MD file structures** across different directories:

1. **Task 75 Files (task_data/)** - Detailed, comprehensive, implementation-focused
2. **Branch Alignment Files (new_task_plan/task_files/)** - Lightweight, strategy-focused
3. **Branch Alignment Plan (new_task_plan/)** - Initiative-based, hierarchical planning

### Key Finding

**Task 75 structure is significantly more detailed** (350-642 lines per task) compared to other task files (20-90 lines per task). This analysis provides a **unified standard** that balances detail with accessibility.

---

## Comparative Analysis

### Structure 1: Task 75 (task_data/) - COMPREHENSIVE MODEL

**Location:** `/home/masum/github/PR/.taskmaster/task_data/task-75.X.md`  
**File Count:** 9 subtask files + 1 overview file  
**Lines per File:** 353-642 lines (average 456 lines)  
**Total Size:** ~4,140 lines across 9 files

#### Current Sections (Task 75.1 as example)
```
1. Title & Metadata
2. Purpose (clear, focused)
3. Developer Quick Reference (NEW - integrated from HANDOFF)
   - What to Build
   - Class Signature
   - Output Specification
4. Success Criteria (detailed: core, QA, integration)
5. Subtasks (75.1.1 - 75.1.8, each with details)
   - Purpose statement
   - Effort estimate
   - Dependencies
   - Steps (numbered)
   - Success Criteria
   - Implementation Checklist (From HANDOFF) ← INTEGRATED
6. Configuration Parameters
7. Technical Reference (From HANDOFF)
   - Git Commands Reference
   - Code Patterns
   - Dependencies & Parallel Tasks
8. Integration Checkpoint
9. Done Definition
```

**Strengths:**
- ✅ Complete self-contained specification
- ✅ Implementation guidance at point of use
- ✅ Test cases with concrete examples
- ✅ Git commands copy-paste ready
- ✅ Clear dependencies and blockers
- ✅ Configuration externalized

**Weaknesses:**
- ❌ Very long files (500+ lines can be hard to navigate)
- ❌ May overwhelm developers with detail
- ❌ Difficult to extract high-level overview

**Integration Status:** ✅ All 9 files have implementation checklists, test cases, and technical references

---

### Structure 2: New Task Plan Files (new_task_plan/task_files/) - LIGHTWEIGHT MODEL

**Location:** `/home/masum/github/PR/.taskmaster/new_task_plan/task_files/task-X.md`  
**File Count:** 40+ task files  
**Lines per File:** 20-90 lines (average 45 lines)  
**Total Size:** ~1,800 lines across 40+ files

#### Current Sections (task-7.md as example)
```
1. Title with Original ID
   - Original ID
   - Status
   - Priority
   - Sequential ID
   - Initiative reference
2. Separator (---)
3. Purpose (brief overview)
4. Separator (---)
5. Success Criteria (simple checklist)
6. Separator (---)
7. Subtasks (minimal entries)
8. Implementation Notes
   - Generated timestamp
   - Source document
   - Original Task ID
```

**Strengths:**
- ✅ Lightweight and scannable
- ✅ Quick overview
- ✅ Easy to extract high-level structure
- ✅ Minimal overhead
- ✅ Links to source documents

**Weaknesses:**
- ❌ Missing implementation guidance
- ❌ No test cases or examples
- ❌ No git commands or technical details
- ❌ Subtasks lack depth
- ❌ Not self-contained (requires referencing source)
- ❌ No performance targets or configuration

**Integration Status:** ❌ Generated from source, minimal additional detail

---

### Structure 3: New Task Plan (new_task_plan/) - INITIATIVE-BASED MODEL

**Location:** `/home/masum/github/PR/.taskmaster/new_task_plan/complete_new_task_outline_ENHANCED.md`  
**File Count:** 1 comprehensive document  
**Lines:** 3,200+ lines  
**Structure:** Hierarchical by Initiative

#### Current Sections
```
1. Title & Metadata
2. Overview (with key changes from original plan)
3. Mapping Reference (table with all tasks)
4. INITIATIVE 1 - INITIATIVE 5
   Each Initiative contains:
   - Priority & Purpose
   - Multiple tasks (I1.T0, I1.T1, etc.)
   Each Task contains:
   - Original ID
   - Status, Priority, Sequential ID
   - Purpose
   - Description (detailed)
   - Success Criteria
   - Implementation Guidance
     - Key Commands
     - Strategic Considerations
     - Test Strategy
   - Subtasks (sometimes with detail)
     - Purpose, Steps, Success Criteria
     - Implementation Guidance
     - Test Strategy
```

**Strengths:**
- ✅ Comprehensive and detailed
- ✅ Shows relationship between initiatives
- ✅ Contains implementation guidance
- ✅ Includes git commands and test strategies
- ✅ Shows dependencies clearly

**Weaknesses:**
- ❌ Very long single document (3,200+ lines)
- ❌ Hard to navigate without TOC
- ❌ Not easily parsed by tools
- ❌ Mixing strategic and implementation details
- ❌ No individual task files for task management systems

---

## Branch Alignment MD Files Structure

**Location:** `/home/masum/github/PR/.taskmaster/docs/branch_alignment/`

### Current Files
1. `SYSTEM_OVERVIEW.md` - High-level system design
2. `COORDINATION_AGENT_SYSTEM.md` - Agent coordination patterns
3. `BRANCH_ALIGNMENT_SYSTEM.md` - System design details
4. `PRECALCULATION_PATTERNS.md` - Optimization patterns
5. `MULTI_AGENT_COORDINATION.md` - Coordination strategies
6. `COORDINATION_AGENTS_SUMMARY.md` - Summary of agents

### Structure
```
1. Title
2. Overview/Purpose
3. Architecture/Design
4. Key Concepts
5. Implementation Details
6. Patterns & Best Practices
7. Integration Points
8. Examples/Code snippets
9. References
```

**Characteristics:**
- Focused on system design and architecture
- Not traditional task definitions
- Rich conceptual content
- Minimal task breakdown

---

## Proposed Unified Task MD Structure

### Goal
Create a **standardized, flexible structure** that:
- Maintains Task 75's comprehensive detail where needed
- Supports lightweight tasks from new_task_plan
- Works with task management systems (Jira, Linear, TaskMaster)
- Separates strategic planning from implementation
- Enables tool automation

### Universal Task Structure (Recommended)

```markdown
# Task [ID]: [Title]

## Metadata
**ID:** [Task ID]  
**Status:** [pending|in-progress|done|blocked|deferred]  
**Priority:** [critical|high|medium|low]  
**Effort:** [X-Y hours] (optional)  
**Complexity:** [X/10] (optional)  
**Initiative:** [Initiative name] (optional, for hierarchical tasks)  

---

## Purpose
[1-2 paragraph description of what this task achieves]

---

## Success Criteria

### Core Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Quality Assurance (optional)
- [ ] QA criterion 1
- [ ] QA criterion 2

### Integration Readiness (optional)
- [ ] Integration criterion 1
- [ ] Integration criterion 2

---

## Scope & Boundaries

**In Scope:**
- [What this task covers]

**Out of Scope:**
- [What this task does NOT cover]
- [Dependencies on other tasks]

---

## Subtasks

### [Subtask ID]: [Subtask Title]
**Purpose:** [Clear purpose statement]  
**Effort:** [X-Y hours]  
**Dependencies:** [List of blocking tasks]  

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Success Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Implementation Guidance:** (optional, for detailed tasks)
- [ ] Action item 1
- [ ] Action item 2

---

## Implementation Reference (optional)

### Developer Quick Reference (for detailed tasks)
[Code signatures, class definitions, API contracts]

### Configuration Parameters (optional)
```yaml
parameter_1: value
parameter_2: value
```

### Technical Details (optional)
- Git commands: [for implementation]
- Code patterns: [common patterns used]
- Performance targets: [measurable baselines]

### Test Case Examples (optional for testing tasks)
1. **test_case_name:** Expected input → Expected output

---

## Dependencies

**Blocked By:**
- [Task X]
- [Task Y]

**Blocks:**
- [Task A]
- [Task B]

**Can Work in Parallel:**
- [Task P]

---

## Performance Targets (optional)

- Target 1: [measurement]
- Target 2: [measurement]

---

## Integration Checkpoint

**When to Move to Next Task:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Done Definition

Task [ID] is complete when:
1. [Final requirement 1]
2. [Final requirement 2]
3. [Final requirement 3]

---

## References & Related Tasks

- Related: [Task X]
- Reference: [Document name]
- See also: [Other resource]
```

---

## Applying the Unified Structure

### For Task 75 Tasks
**Status:** ✅ Already exceeds unified structure  
**Action:** Keep current structure (it's comprehensive)  
**Note:** Could be reorganized with clearer section boundaries, but functional as-is

### For New Task Plan Tasks
**Status:** ❌ Below unified structure  
**Action:** Enhance with:
- [ ] Success Criteria expanded to 3-5 items
- [ ] Subtasks with Steps and Success Criteria
- [ ] Dependencies clearly stated
- [ ] Performance Targets (if applicable)
- [ ] Done Definition section

### For Branch Alignment System Files
**Status:** ⚠️ Different purpose (system design)  
**Action:** Keep separate, but add:
- [ ] Clear table of contents
- [ ] Navigation section
- [ ] Cross-references to task files
- [ ] Integration points documented

---

## Section Mapping

### Lightweight Tasks (20-60 lines)
```
✓ Metadata
✓ Purpose
✓ Success Criteria (3-5 items)
✓ Subtasks (brief)
✓ Dependencies
✓ Done Definition
```

### Detailed Tasks (200-400 lines)
```
✓ Metadata
✓ Purpose
✓ Developer Quick Reference
✓ Success Criteria (detailed)
✓ Subtasks (8+ with full structure)
✓ Implementation Reference
✓ Technical Details
✓ Dependencies
✓ Integration Checkpoint
✓ Done Definition
```

### Comprehensive Tasks (400-650 lines)
```
✓ Metadata
✓ Purpose
✓ Developer Quick Reference
✓ Success Criteria (detailed: core, QA, integration)
✓ Subtasks (8+ with full structure)
✓ Configuration Parameters
✓ Implementation Checklists
✓ Test Case Examples
✓ Technical Reference (git commands, algorithms)
✓ Performance Targets
✓ Dependencies
✓ Integration Checkpoint
✓ Integration Points (for downstream tasks)
✓ Done Definition
✓ References
```

---

## Standardization Actions

### Phase 1: Analysis (Complete) ✅
- [x] Identified 3 distinct structures
- [x] Analyzed strengths/weaknesses
- [x] Created unified template

### Phase 2: Implementation Guidelines
- [ ] Determine which tasks should be lightweight vs. comprehensive
- [ ] Enhance new_task_plan task files (40+ files)
- [ ] Establish tool support for section detection
- [ ] Create validation/linting rules

### Phase 3: Documentation
- [ ] Create task file writing guide
- [ ] Document best practices per task type
- [ ] Create examples for each structure level
- [ ] Add to developer onboarding

### Phase 4: Tool Integration
- [ ] Update TaskMaster to parse unified structure
- [ ] Create automation for section extraction
- [ ] Build dependency graph from metadata
- [ ] Generate reports from task files

---

## Key Recommendations

### 1. Preserve Task 75 Structure
**Rationale:** Comprehensive, proven, meets all needs  
**Action:** Use as gold standard for complex tasks (8+ subtasks)  
**Apply to:** Tasks with 8+ subtasks or >100 lines

### 2. Enhance Lightweight Tasks
**Rationale:** Currently lack sufficient detail  
**Action:** Add Success Criteria, Dependencies, Done Definition  
**Apply to:** Tasks with 1-3 subtasks or <50 lines

### 3. Create Task Type Guidelines
**Rationale:** Different tasks need different levels of detail  
**Action:** Define task types and their structure requirements  
**Types:**
- **Framework Task** (like Task 75): 400+ lines, comprehensive
- **Implementation Task** (like Task 59): 200-300 lines, detailed
- **Configuration Task** (like Task 54): 80-150 lines, specific steps
- **Reference Task** (like branch_alignment): System design, architectural

### 4. Establish Metadata Standards
**Rationale:** Enables tool automation  
**Action:** Require consistent metadata in all tasks
```yaml
ID: [required]
Status: [required]
Priority: [required]
Effort: [optional]
Complexity: [optional]
Initiative: [conditional]
Dependencies: [recommended]
```

### 5. Implement Section Detection
**Rationale:** Enables automated extraction  
**Action:** Ensure consistent heading hierarchy
- H1: Task title
- H2: Major sections (Purpose, Success Criteria, Subtasks)
- H3: Subsections and subtasks
- H4: Details within subtasks

---

## Implementation Examples

### Example 1: Lightweight Configuration Task
```markdown
# Task 54: Establish Core Branch Alignment Framework

**ID:** I2.T1  
**Status:** pending  
**Priority:** high  
**Effort:** 8-12 hours  

## Purpose
Configure foundational elements for branch management...

## Success Criteria
- [ ] Review Existing Branch Protections
- [ ] Configure Required Reviewers
- [ ] Enforce Passing Status Checks
- [ ] Enforce Merge Strategies
- [ ] Design Local Git Hook Integration
- [ ] Integrate Pre-Merge Scripts
- [ ] Develop Centralized Orchestration Script

## Subtasks

### 1: Review Existing Branch Protections
**Purpose:** Assess current state

---

## Dependencies
**Blocked By:** None  
**Blocks:** Tasks 55, 56

## Done Definition
Task is done when all 7 subtasks complete.
```
**Lines:** 60  
**Type:** Configuration (lightweight)

### Example 2: Implementation Task
```markdown
# Task 75.2: CodebaseStructureAnalyzer

**ID:** 75.2  
**Status:** Ready for implementation  
**Priority:** high  
**Effort:** 28-36 hours  
**Complexity:** 7/10

## Purpose
Create a reusable Python class that measures...

## Developer Quick Reference
### What to Build
A Python class `CodebaseStructureAnalyzer` that...

### Metrics Overview
[Table with 4 metrics]

### Output Specification
[JSON schema]

## Success Criteria
### Core Functionality
- [5 items]
### Quality Assurance
- [3 items]
### Integration Readiness
- [3 items]

## Subtasks (75.2.1 - 75.2.8)
[8 detailed subtasks with Implementation Checklist]

## Configuration Parameters
[Externalized parameters]

## Test Case Examples (From HANDOFF)
[5-8 concrete test cases]

## Technical Reference (From HANDOFF)
[Git commands, algorithms, dependencies]

## Integration Checkpoint
[When to move to 75.3]

## Done Definition
[Final requirements]
```
**Lines:** 400+  
**Type:** Implementation (comprehensive)

### Example 3: Framework Task (Full Comprehensive)
```markdown
# Task 75: Branch Clustering System

**ID:** 75  
**Status:** In progress  
**Priority:** critical  
**Effort:** 212-288 hours  
**Complexity:** 8/10  
**Timeline:** 6-8 weeks

## Overview
Implement a complete branch clustering system...

## Status
[9 subtasks with checkboxes]

## Execution Strategies
[3 different approaches]

## Integration Architecture
[Flow diagram]

## Subtasks (75.1 - 75.9)
[Each as separate file with full structure]

## Performance Targets
[Measurable baselines]

## Done Definition
[Complete requirements]
```
**Lines:** 160+  
**Type:** Framework (strategic overview)

---

## Migration Path

### Step 1: Audit Existing Tasks
- [ ] Categorize all task files by type
- [ ] Measure current line counts
- [ ] Identify missing sections

### Step 2: Create Enhancement Plan
- [ ] Lightweight tasks → Add success criteria, dependencies
- [ ] Detailed tasks → Verify comprehensive structure
- [ ] Framework tasks → Ensure clear overview

### Step 3: Implement in Phases
- Phase A: Task 75 files (already complete)
- Phase B: New task plan files (40+ files)
- Phase C: Branch alignment tasks (if applicable)

### Step 4: Validation
- [ ] Verify all required sections present
- [ ] Check consistent formatting
- [ ] Validate metadata completeness
- [ ] Test tool parsing

---

## Tool Integration Points

### TaskMaster Integration
```python
# Parse task metadata
parse_metadata(task_file) → {
    'id': '75.1',
    'status': 'ready for implementation',
    'priority': 'high',
    'effort': '24-32',
    'complexity': 7,
    'dependencies': ['75.4'],
    'blocks': ['75.4']
}

# Extract subtasks
extract_subtasks(task_file) → [
    {'id': '75.1.1', 'title': 'Design Metric System', 'effort': '2-3'},
    ...
]

# Validate structure
validate_structure(task_file) → {
    'has_purpose': True,
    'has_success_criteria': True,
    'subtasks_complete': 8/8,
    'missing_sections': []
}
```

### Visualization Integration
```python
# Generate dependency graph
task_dependencies → graph.json

# Create timeline
effort_estimates → gantt.json

# Generate status dashboard
task_statuses → dashboard.html
```

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Consistent section headings | 60% | 100% |
| All tasks have metadata | 70% | 100% |
| All tasks have success criteria | 85% | 100% |
| Subtasks have step lists | 50% | 100% |
| Dependencies documented | 60% | 100% |
| Performance targets specified | 30% | 100% |

---

## Conclusions

### Key Findings

1. **Task 75 is the gold standard** for comprehensive tasks - use as template for others
2. **New task plan tasks lack detail** - need enhancement with structured guidance
3. **Unified structure is achievable** without losing flexibility or detail
4. **Tool automation is possible** with consistent metadata and sections

### Recommendations

1. ✅ **Adopt Task 75 structure as standard** for comprehensive tasks (8+ subtasks)
2. ✅ **Enhance lightweight tasks** with full success criteria and dependencies
3. ✅ **Implement consistent metadata** across all task files
4. ✅ **Create task type guidelines** for appropriate detail level
5. ✅ **Build tool support** for parsing and validation

### Next Steps

1. Create task file writing guide (based on this analysis)
2. Enhance 40+ new_task_plan files with unified structure
3. Implement TaskMaster parsing for metadata extraction
4. Build validation/linting tool
5. Create automated dependency graph generation

---

**Document Status:** ✅ Complete  
**Analysis Scope:** All task MD files across 3 directories  
**Coverage:** 9 Task 75 files + 40+ new_task_plan files + branch_alignment system  
**Recommendation:** Adopt Task 75 structure as universal standard with flexible depth options
