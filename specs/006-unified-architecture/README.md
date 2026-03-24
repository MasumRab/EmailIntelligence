# Unified Architectural Plan Spec

## Overview

This spec (`006-unified-architecture`) outlines the consolidation of three competing workflow systems into a unified architecture.

## What This Spec Covers

- **Three Workflow Systems**: Basic System, Node Engine, Advanced Core
- **Consolidation**: Unified architecture using Node Engine as target
- **Security**: Enterprise-grade security (path traversal, input sanitization, audit logging)
- **Performance**: Sub-200ms response times, async execution
- **Compatibility**: Backward compatibility with existing APIs

## Directory Structure

```text
specs/006-unified-architecture/
├── spec.md                            # This spec (speckit format)
├── plan.md                            # Implementation plan
├── tasks.md                           # Task breakdown
├── README.md                          # This file
└── architecture-docs/                 # Detailed architecture documents
    ├── UNIFIED_ARCHITECTURAL_PLAN.md
    ├── node_architecture.md
    ├── workflow_system_analysis.md
    ├── advanced_workflow_system.md
    ├── technology_stack.md
    ├── architecture_summary.md
    └── architecture_overview.md
```

## How to Use This Spec

1. Read `spec.md` for the full specification
2. Reference `architecture-docs/UNIFIED_ARCHITECTURAL_PLAN.md` for the consolidation plan
3. Use `plan.md` for technical context and approach
4. Follow `tasks.md` for phased implementation

## Status

**Completed Architecture Spec** — Ported from scientific branch `docs/architecture/` directory.
