# Constitution Update Plan

## Overview

Update the project constitution (`.specify/memory/constitution.md`) to address weaknesses identified through comparison with real-world examples (OpenDataHub, Anthropic, ruflo/guidance).

## Current State

- **Version**: 1.5.0
- **Lines**: ~270
- **Location**: `.specify/memory/constitution.md`

## Weaknesses Identified

| # | Weakness | Impact |
|---|----------|--------|
| 1 | No rationale for key rules | Agents don't understand WHY |
| 2 | No MUST vs SHOULD hierarchy | Unclear what's non-negotiable |
| 3 | Verbose sections | Hard to scan |
| 4 | Agentic rules scattered | Should be more prominent |
| 5 | No explicit scope markers | Unclear what applies where |

---

## Detailed Tasks

### Task 1: Add Rationale to Key Rules (HIGH PRIORITY)

**What**: Add "Rationale:" explanation to each core principle section

**Sections to update**:
- [ ] I. Code Quality and Standards
- [ ] II. TDD (add why TDD is critical for AI)
- [ ] VII. API-First Design (add why critical for agents)
- [ ] XII. Agentic-First Tool Design

---

### Task 2: Add MUST vs SHOULD Hierarchy (HIGH PRIORITY)

**What**: Clarify mandatory vs recommended rules

**Add new subsection**:
```markdown
### 0. Rule Hierarchy

This constitution uses consistent language:

- **MUST** / **REQUIRED**: Non-negotiable rule. Violation = rejection.
- **SHOULD**: Strong recommendation. Deviation requires justification.
- **MAY** / **OPTIONAL**: Nice to have. Left to engineer judgment.
```

---

### Task 3: Condense Verbose Sections (MEDIUM PRIORITY)

**Target sections**:
- [ ] Section IV (Performance) - condense to 5 key metrics
- [ ] Section IX (Branching) - merge with existing patterns
- [ ] Remove duplicate content between Extension A and Section XII

**Goal**: Reduce from 270 to ~200 lines

---

### Task 4: Elevate Agentic-First to Core Principle (HIGH PRIORITY)

**What**: Move Section XII from position XII to Principle 0

**Add before Section I**:
```markdown
## 0. Agentic-First Design (PRIMARY)

All CLI/TUI tools MUST be designed for AI agent consumption as the primary use case.

**Rationale**: This project creates tools for autonomous agents. If other rules conflict, this takes precedence.
```

---

### Task 5: Add Explicit Scope Markers (MEDIUM PRIORITY)

**What**: Tag each rule with applicability scope

**Example**:
```markdown
### II. Test-Driven Development (TDD) [APPLIES: All Code]
### XII. Agentic-First Tool Design [APPLIES: CLI/TUI Tools Only]
```

---

### Task 6: Add Quick Reference Card (NEW)

**What**: Create TL;DR section at top

```markdown
## Quick Reference

| Symbol | Meaning |
|--------|---------|
| 🔴 MUST | Non-negotiable |
| 🟡 SHOULD | Strong recommendation |
| 🟢 MAY | Optional |
```

---

### Task 7: Update Version and Amendment Log (REQUIRED)

- Version: 1.6.0
- Date: 2026-03-15

---

## Execution Order

```
Wave 1: T4, T2, T6 (foundation)
Wave 2: T1, T5 (quality)
Wave 3: T3, T7 (cleanup)
```

---

## Success Criteria

- [ ] Length reduced to ~200 lines
- [ ] Every core rule has Rationale
- [ ] MUST vs SHOULD clearly distinguished
- [ ] Agentic-First is Principle 0
- [ ] Quick Reference card added
- [ ] Version: 1.6.0
