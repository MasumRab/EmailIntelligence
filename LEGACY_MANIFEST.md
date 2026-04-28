# Legacy Manifest

This file serves as the single source of truth for legacy components maintained for backward compatibility.
Files listed here must not be removed by automated agents or CI without explicit human approval.

## Active Legacy Files

| File | Subsystem | Owner/Maintainer | Migration Tracker / Notes |
|---|---|---|---|
| `src/backend/python_backend/*` | Legacy Monolithic Backend | core-team | Migrating to `src/core/` and `modules/` |
| `src/backend/extensions/example/*` | Extension examples | core-team | Needs migration to new extension architecture |
| `src/backend/data/*.json` | JSON Data store | core-team | Handled via SQLite in new arch, kept for PR compatibility |
| `tests/deprecated/*` | Legacy tests | core-team | Migrating to modular testing strategy |

## Policy
* Do not delete files matching the patterns above.
* Do not reformat them in ways that break open PRs.
* Any tool or agent attempting to clean up "dead code" must exclude these paths.
