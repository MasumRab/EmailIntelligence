# Safety & Integrity Checklist: Orchestration Core

**Purpose**: Validate that requirements ensure "Zero Data Loss" and "Safe Execution" across all mutating operations.
**Created**: 2026-01-14
**Feature**: [004-guided-workflow](../spec.md)

## Destructive Action Safety

- [x] CHK001 Is the "Backup & Overwrite" requirement (FR-017) applied to *all* file overwrites (e.g., Syncing scripts), not just Hooks? [Consistency, FR-016 vs FR-017]
- [x] CHK002 Are "Dry-Run" requirements defined for every command that modifies the git index (Rebase, Sync)? [Completeness, FR-007]
- [x] CHK003 Is the "Zero Working Tree Modification" constraint (SC-003) explicitly verified by a requirement for `analyze`? [Coverage, US2]
- [x] CHK004 Are safeguards defined for "Binary File" merges to prevent corruption? [Edge Case, Research]

## State Resilience

- [x] CHK005 Is the "Atomic Write" requirement (FR-014) specified for *every* state transition, or just the final success? [Clarity, FR-014]
- [x] CHK006 Are requirements defined for detecting and handling a "Stale Lockfile" or "Corrupt State File"? [Edge Case, US7]
- [x] CHK007 Does the spec define behavior if the process is killed *during* a file write? [Recovery, FR-014]

## Git Integrity

- [x] CHK008 Are there requirements to verify the repo is clean *before* attempting operations that might dirty it? [Pre-condition, US3]
- [x] CHK009 Is the "Canonical Source" verification (FR-013) required to fail secure (abort) if the hash mismatches? [Security, FR-013]
- [x] CHK010 Are requirements defined to prevent `dev.py` from running on a detached HEAD state (unless intended)? [Safety, Edge Case]

## Notes
- "Safe by default" is a core design principle. Use this list to ensure specs mandate safety rails.
