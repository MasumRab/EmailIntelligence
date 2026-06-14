## 2025-04-16 - [Add missing authentication to endpoints]

**Vulnerability:** Several endpoints across various router files (`ai_routes.py`, `performance_routes.py`, `src/core/model_routes.py`, `src/core/plugin_routes.py`, `routes/v1/category_routes.py`, `routes/v1/email_routes.py`) were missing authentication checks.
**Learning:** These endpoints were either missing the `Depends(get_current_active_user)` entirely or were missing it from their respective `APIRouter` initializations, leaving them exposed to unauthenticated access.
**Prevention:** Ensure all `APIRouter` instances are created with the `dependencies=[Depends(get_current_active_user)]` parameter by default unless explicitly meant to be public, or add the dependency to each individual endpoint.
