# modules — Modular Feature Architecture

**Parent:** [AGENTS.md](../../AGENTS.md)

## OVERVIEW

New modular architecture. Add new features here. Migration target from deprecated `src/backend/`.

## STRUCTURE

```
modules/
├── auth/           # Authentication
├── categories/     # Email categorization
├── dashboard/      # Dashboard features
├── email/          # Email processing
├── workflows/      # Workflow automation
└── new_ui/         # Gradio scientific UI
```

## WHERE TO LOOK

| Task | Module | Notes |
|------|--------|-------|
| New features | Any subdir | Preferred location |
| Auth logic | `auth/` | JWT, MFA |
| Email handling | `email/` | Processing |
| UI components | `new_ui/app.py` | Gradio entry |

## CONVENTIONS

- Follow parent conventions
- Each module should be self-contained
- Use `modules/` for new code, not `src/backend/`
