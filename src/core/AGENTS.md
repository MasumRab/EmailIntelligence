# src/core — Core Business Logic

**Parent:** [AGENTS.md](../../AGENTS.md)

## OVERVIEW

Primary location for backend business logic. Active development target. Use this instead of deprecated `src/backend/`.

## STRUCTURE

```
src/core/
├── database.py           # 942 lines — Core infrastructure
├── smart_filter_manager.py  # 891 lines — Business logic
├── advanced_workflow_engine.py  # 775 lines — DAG execution
├── workflow_engine.py    # 685 lines — Legacy workflow
├── model_registry.py     # 717 lines
├── security.py           # 640 lines
├── plugin_base.py        # 555 lines
├── notmuch_data_source.py # 750 lines
├── data/
│   ├── factory.py       # Factory pattern
│   └── data_source.py   # Abstract base class
└── tests/
```

## WHERE TO LOOK

| Task | File | Notes |
|------|------|-------|
| Database changes | `database.py` | Write-behind caching |
| Filters | `smart_filter_manager.py` | Business rules |
| Workflows | `advanced_workflow_engine.py` | DAG-based |
| Security | `security.py` | Auth, permissions |

## CONVENTIONS

- Follow parent conventions (black, flake8, mypy)
- Use async/await for I/O operations
- Import from `src.core` not `src.backend`

## ANTI-PATTERNS

- **DO NOT** use `src.backend` modules — deprecated
- Avoid adding to large files (split if >500 lines)
- Don't duplicate logic in `src/backend/`
