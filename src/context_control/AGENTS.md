# src/context_control — Agent Context Isolation

**Parent:** [AGENTS.md](../../AGENTS.md)

## OVERVIEW

Well-structured context isolation system for multi-agent workflows. Use as pattern for new modules.

## STRUCTURE

```
src/context_control/
├── core.py       # Branch detection, profile matching, caching
├── isolation.py  # Allow/deny access control
└── agent.py      # Permission-based function adaptation
```

## WHERE TO LOOK

| Task | File | Notes |
|------|------|-------|
| Branch-based context | `core.py` | Auto-detects git branch |
| Access control | `isolation.py` | Glob/fnmatch patterns |
| Agent permissions | `agent.py` | Permission enforcement |

## CONVENTIONS

- Follow parent conventions
- Well-documented with type hints
- Clean separation of concerns

## PATTERNS

- **Glob matching**: `_matches_pattern()` for branch patterns
- **Allow/deny lists**: Access control in isolation.py
- **Dynamic extension**: Profile configs can be extended at runtime
