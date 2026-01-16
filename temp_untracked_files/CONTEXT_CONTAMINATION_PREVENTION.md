# Context Contamination Prevention Guide

## Overview

Context contamination is a critical issue in AI-assisted development where information from one task/conversation bleeds into another, causing the AI agent to apply incorrect assumptions, patterns, or state to unrelated work. This document provides comprehensive guidance for preventing and managing context contamination in the EmailIntelligence project.

## Definition

Context contamination occurs when:
- Information from one task/conversation influences reasoning in another
- Assumptions from previous work are incorrectly applied to new tasks
- State from completed operations persists and affects subsequent work
- Biased reasoning emerges from incomplete context isolation

### Impacts

- **Cross-task information pollution**: Mixing concerns from different features
- **Incorrect pattern matching**: Applying patterns from one feature to unrelated code
- **State leakage**: Persisting assumptions between independent operations
- **Biased reasoning**: Previous contexts influencing new analysis
- **Quality degradation**: Mistakes propagating across multiple changes

## Prevention Guidelines

### 1. Task Isolation

Every task must maintain its own isolated context with clear boundaries.

#### Implementation
- **Start fresh**: Begin each new task with explicit context reset
- **Scope confirmation**: Always confirm task scope before proceeding
- **Assumption declaration**: State any assumptions explicitly
- **Boundary marking**: Use clear delimiters between different work items

#### Best Practices
```
Task A: "Implement user authentication"
[Complete, test, and document Task A]
--- TASK BOUNDARY ---
Task B: "Add email filtering"
[Begin with fresh context, no assumptions from Task A]
```

#### Checklist
- [ ] Read task description thoroughly before starting
- [ ] Identify task-specific dependencies (not from previous work)
- [ ] Create new mental context separate from prior work
- [ ] Document assumptions specific to this task
- [ ] Close out previous task mentally before switching

### 2. Tool State Management

Keep tool usage stateless and verify environment at each task start.

#### Implementation
- **Environment verification**: Check current branch, working directory, and file states
- **State reset**: Explicitly reset any maintained state
- **Stateless operations**: Design tool usage to not rely on persistent state
- **State validation**: Verify expected state before operations

#### Best Practices
```bash
# At task start:
git status  # Verify current branch and clean state
git branch  # Confirm working branch
pwd         # Confirm working directory
```

#### Checklist
- [ ] Verify current git branch before making changes
- [ ] Check working directory is clean (no stray modifications)
- [ ] Re-verify file paths (don't assume locations)
- [ ] Confirm environment variables are set correctly
- [ ] Clear mental history of tool commands

### 3. Documentation Boundaries

Maintain clear boundaries between task-specific and shared documentation.

#### Implementation
- **Task-specific docs**: Keep requirements and notes separate per task
- **Shared references**: Use explicit links to shared patterns, not implicit memory
- **Clear sections**: Use headers and delimiters to separate concerns
- **Context pointers**: When referencing other work, use explicit file paths or links

#### Best Practices
```markdown
# Task: Email Filter Implementation

## Task-Specific Requirements
- Filter by sender domain
- Cache filter results

## Shared Patterns Used
- See AGENTS.md section "Code Style" for formatting rules
- Reference: /backend/services/analyzer.ts for similar pattern

## Not from other tasks
- Do not assume authentication patterns from Task A
```

#### Checklist
- [ ] Keep task requirements in separate section
- [ ] Link to shared patterns explicitly
- [ ] Don't reference previous task details from memory
- [ ] Document task-specific edge cases separately
- [ ] Avoid mixing concerns in documentation

### 4. Code Review Protection

Review code changes only in context of the current task.

#### Implementation
- **Task-focused review**: Evaluate code against current task requirements only
- **Dependency validation**: Verify all dependencies are intentional
- **Pattern questioning**: Require explicit justification for pattern choices
- **Side effect detection**: Verify changes don't affect unrelated modules

#### Best Practices
```typescript
// TASK: Add email filtering
// Review focuses on:
// - Does this implement the filter correctly?
// - Are dependencies intentional and documented?
// - Does this break any existing tests?

// Do NOT assume:
// - Patterns from authentication work (different task)
// - State management approaches from analytics (different task)
```

#### Checklist
- [ ] Review changes against current task requirements only
- [ ] Verify all imported modules are necessary
- [ ] Question any patterns from "similar" features
- [ ] Check for unintended modifications to unrelated files
- [ ] Validate no implicit dependencies between tasks

### 5. Communication Clarity

Explicitly manage context switches in communication and logging.

#### Implementation
- **Assumption declaration**: State what you're assuming at task start
- **Scope confirmation**: Always confirm understanding of task boundaries
- **Context switching**: Mark clear transitions between tasks
- **Session notes**: Log context changes during work session

#### Best Practices
```markdown
## Session Start: Feature X Implementation

### Current Context
- Working on: Email categorization feature
- Branch: feature/email-categories
- Related files: /backend/categorizer.py, /client/CategoryCard.tsx

### Assumptions
- Database schema for categories exists
- User authentication is already implemented (Task A)

---
## Context Switch: Bug Fix in Task Y

### New Context
- Switching to: Fix authentication edge case
- Branch: bugfix/auth-edge-case
- Related files: /backend/auth.ts

### Isolation Note
- This is independent of Task X
- Do not apply categorization patterns here
- Reset mental state for authentication context
```

#### Checklist
- [ ] Declare assumptions when starting task
- [ ] Confirm task scope with stakeholder
- [ ] Mark context switches explicitly
- [ ] Log session notes for context transitions
- [ ] Use clear delimiters between different work

### 6. Testing and Verification

Verify changes don't have unintended cross-module impacts.

#### Implementation
- **Isolation testing**: Test changes independently before integration
- **Regression testing**: Run affected test suites
- **Side effect detection**: Verify no modifications to unrelated modules
- **Impact documentation**: Record any discovered cross-module impacts

#### Best Practices
```bash
# Task A: Implement feature X
npm run test:feature-x  # Test only feature X
npm run test:related   # Test related components only

# Before merging to main
npm run test           # Full test suite to catch side effects

# Document results
# File: TASK_A_TEST_RESULTS.md
# - Feature X: ✓ Passing
# - Integration tests: ✓ Passing
# - No regressions detected in other modules
```

#### Checklist
- [ ] Test changes in isolation first
- [ ] Run full test suite before merging
- [ ] Document test results per task
- [ ] Verify no unintended file modifications
- [ ] Check for new dependencies introduced
- [ ] Validate no implicit state leakage

## Branch Management

### Branch Strategy for Context Isolation

```
main (stable)
├── feature/task-a (isolated context for Task A)
├── feature/task-b (isolated context for Task B)
└── bugfix/task-c (isolated context for Task C)
```

### Best Practices

1. **One task per branch**: Each feature/bugfix branch represents one task
2. **Clear naming**: Branch names reflect task scope
3. **Explicit merging**: Only merge when task is complete and isolated
4. **No cherry-picking**: Avoid mixing task contexts through selective commits

## Red Flags

Watch for these indicators of context contamination:

- [ ] Applying patterns from "similar" features without explicit justification
- [ ] Assuming database schema or API structure from other tasks
- [ ] Reusing variable names or function patterns from previous tasks
- [ ] Making changes to unrelated files during a focused task
- [ ] Referencing implementation details from memory instead of code
- [ ] Cross-feature dependencies not documented explicitly
- [ ] Test failures in unrelated modules after a change
- [ ] Difficulty explaining why a particular pattern was chosen

## Recovery Process

If context contamination is detected:

1. **Identify**: Note which task contexts were mixed
2. **Isolate**: Separate changes back into task-specific branches
3. **Review**: Examine each isolated change for correctness
4. **Test**: Run full test suite on separated changes
5. **Document**: Record how contamination occurred to prevent recurrence
6. **Reapply**: Merge isolated changes back to main systematically

## Tools and Practices

### Git Workflow for Isolation

```bash
# Start Task A
git checkout -b feature/task-a main
# ... complete Task A, test, commit ...
git push origin feature/task-a

# Start Task B (from clean main, not Task A branch)
git checkout main
git pull origin main
git checkout -b feature/task-b main
# ... complete Task B independently ...
```

### Documentation Templates

Use these templates to maintain clear context boundaries:

```markdown
# Task: [Task Name]

## Scope
- What: [Task description]
- Why: [Business justification]
- Files affected: [List of files]

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Dependencies
- External: [Dependencies outside this task]
- Internal: [Dependencies within this task]

## Testing Strategy
- [Test plan]

## Known Limitations
- [Limitations specific to this task]

## Completed
- [ ] Implementation
- [ ] Testing
- [ ] Documentation
- [ ] Code review
```

## Summary

Context contamination prevention is a shared responsibility requiring:
- **Mental discipline**: Actively isolate task contexts
- **Documentation rigor**: Explicitly document assumptions and boundaries
- **Systematic verification**: Test and review in isolation
- **Clear communication**: Declare context switches and assumptions
- **Continuous vigilance**: Watch for red flags and address early

By following these guidelines, the EmailIntelligence project can maintain high code quality and prevent the subtle bugs that arise from context contamination.
