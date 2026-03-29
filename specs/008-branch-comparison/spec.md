# Feature Specification: Scientific Branch vs Other Branches Comparison

**Feature Branch**: `008-branch-comparison`
**Created**: 2025-10-28
**Status**: Completed (Analysis Spec)
**Source**: Ported from scientific branch `guidance/` directory

## Overview

This spec documents the comparison between the scientific branch and other branches (orchestration-tools, main, etc.) in the EmailIntelligence project. It highlights the enhancements and features available in the scientific branch that are not present in other branches, and provides a basis for merge decisions and feature prioritization.

## Clarifications

### Session 2025-10-28

- Q: What makes the scientific branch different from orchestration-tools? → A: Scientific has full factory pattern, interface-based architecture, advanced CLI, complete module structure, constitutional engine, auto resolution, and strategy generation
- Q: What is missing in orchestration-tools? → A: Minimal structure, no factory pattern, basic CLI only, no constitutional analysis
- Q: What is the relationship with main branch? → A: Scientific is ahead of main by ~83 commits, behind by ~1652 (many divergence points)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Feature Gap Analysis (Priority: P1)

As a developer, I want to understand what features the scientific branch has that other branches don't, so that I can plan feature ports and merge strategies.

**Independent Test**: Complete gap analysis document comparing all branches.

### User Story 2 - Merge Planning (Priority: P1)

As a developer, I want to plan merges from scientific to other branches, so that I can sequence work and estimate effort.

**Independent Test**: Merge plan exists with estimated effort for each target branch.

## Requirements *(mandatory)*

- **Gap Analysis**: Complete feature comparison across all active branches
- **Merge Sequencing**: Ordered list of target branches with dependencies
- **Effort Estimation**: Per-feature effort estimates for porting

## References

See content files:
- `SCIENTIFIC_BRANCH_ENHANCEMENTS_COMPARISON.md` — Full comparison (252 lines)
- `IMPLEMENTATION_SUMMARY.md` — Implementation summary and status
