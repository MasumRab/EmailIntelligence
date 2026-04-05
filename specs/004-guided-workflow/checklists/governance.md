# Governance Logic Checklist: Orchestration Core

**Purpose**: Validate that the Governance requirements (AST Scanning, Constitution) are implementable and effective.
**Created**: 2026-01-14
**Feature**: [004-guided-workflow](../spec.md)

## Rule Definition & Scope

- [x] CHK001 Are the specific "Forbidden Patterns" (e.g., `import os` in scripts) defined in the Spec or delegated to Config? [Clarity, FR-004]
- [x] CHK002 Is the "Target Scope" for scanning (e.g., "only .py files in src/") explicitly defined? [Completeness, US4]
- [x] CHK003 Are requirements defined for handling "False Positives" (e.g., ` # noqa` comments)? [Usability, Edge Case]

## Violation Reporting

- [x] CHK004 Is the JSON schema for violations (FR-015) sufficient to pinpoint the error (Line, Column, Error Code)? [Measurability, FR-015]
- [x] CHK005 Are "Severity Levels" (Warning vs Critical) defined for different types of violations? [Clarity, Data Model]
- [x] CHK006 Is the behavior defined when the `constitution.md` file itself is missing or malformed? [Robustness, Edge Case]

## Enforcement Mechanics

- [x] CHK007 Is the "Block vs Warn" logic defined for the `install-hooks` pre-commit check? [Clarity, FR-017]
- [x] CHK008 Are requirements defined to ensure the scanner performance meets the "< 5 seconds" target? [Performance, SC-002]
- [x] CHK009 Is the scanner required to handle syntax errors in the target code gracefully (without crashing)? [Robustness, Edge Case]

## Notes
- Governance tools can be annoying if they are flaky. Use this checklist to ensure the spec demands robustness.
