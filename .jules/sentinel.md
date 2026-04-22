## 2026-04-22 - [Sentinel] Fixed missing authentication on model and plugin API endpoints

**Vulnerability:** The routers in `src/core/model_routes.py` and `src/core/plugin_routes.py` were missing authentication dependencies, leaving sensitive plugin and model management endpoints entirely unprotected.
**Learning:** FastAPI `APIRouter`s instantiated globally do not automatically inherit application-level authentication middleware unless specifically configured during instantiation or injection. Relying on middleware alone can lead to oversight if endpoints bypass it or are meant to be authenticated granularly.
**Prevention:** Always instantiate sensitive global API routers with the explicit `dependencies=[Depends(get_current_active_user)]` (or equivalent) directly at the router level.
