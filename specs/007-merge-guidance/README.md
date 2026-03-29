# Git Merge Guidance & Branch Strategy Spec

## Overview

This spec (`007-merge-guidance`) captures merge guidance and branch strategy documentation.

## What This Spec Covers

- **Merge Strategies**: Factory pattern, import standardization, incremental resolution
- **Failed Approaches**: Atomic merges, automated conflict resolution without semantic understanding
- **Incremental Resolution**: File-by-file conflict resolution with validation gates
- **Incomplete Migrations**: Handling and tracking partial migrations

## Directory Structure

```text
specs/007-merge-guidance/
├── spec.md                          # This spec
├── plan.md                          # Implementation plan
├── tasks.md                         # Reference tasks
├── README.md                        # This file
├── MERGE_GUIDANCE_DOCUMENTATION.md  # Full merge guidance
├── FINAL_MERGE_STRATEGY.md          # Final strategy decisions
└── HANDLING_INCOMPLETE_MIGRATIONS.md # Migration handling
```

## How to Use This Spec

1. Read `spec.md` for the merge strategy overview
2. Reference `MERGE_GUIDANCE_DOCUMENTATION.md` for detailed guidance
3. Use `FINAL_MERGE_STRATEGY.md` for specific strategy decisions
4. Follow `HANDLING_INCOMPLETE_MIGRATIONS.md` for gap tracking

## Status

**Completed Guidance Spec** — Ported from scientific branch `guidance/` directory.
