# EmailIntelligence CLI Integration & Architecture Alignment Spec

## Overview

This spec (`005-cli-architecture`) captures the CLI integration and architecture alignment guidance from the EmailIntelligence project.

## What This Spec Covers

- **Factory Pattern**: `create_app()` implementation for service startup compatibility
- **CLI Framework**: Advanced CLI with constitutional analysis and conflict resolution
- **Interface-Based Design**: Contract-based abstractions (`IConflictDetector`, etc.)
- **Import Path Standardization**: Consistent `src/` prefix across codebase
- **Hybrid Architecture**: Bridging local and remote branch patterns

## Directory Structure

```text
specs/005-cli-architecture/
├── spec.md                              # This spec (speckit format)
├── plan.md                              # Implementation plan
├── tasks.md                             # Task reference list
├── SUMMARY.md                           # Executive summary
├── QUICK_REEFERENCE_GUIDE.md            # Quick reference
└── architecture-guides/                 # Detailed guidance documents
    ├── COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md
    ├── FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md
    ├── ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md
    └── ARCHITECTURE_ALIGNMENT_IMPLEMENTATION_GUIDE.md
```

## How to Use This Spec

1. Start with `SUMMARY.md` or `QUICK_REFERENCE_GUIDE.md` for a quick overview
2. Read `spec.md` for the full specification in speckit format
3. Reference `architecture-guides/*.md` for detailed implementation guidance
4. Use `plan.md` and `tasks.md` for implementation planning

## Status

**Completed Guidance Spec** — All content ported from scientific branch `guidance/` directory.
