# PR Duplicate Families Report

| Family / Target | Members | Proposed Survivor | Evidence / Rationale |
|-----------------|---------|-------------------|----------------------|
| `verify_password` exceptions in `src/core/auth.py` | #248, #258, #259 | **#259** | Byte-identical to #258 (+4/-3). Uses proper `except InvalidHashError` syntax. #248 adds a base import instead. Target function shape already overwritten on `main`. |
| `_get_searchable_text` in `src/core/database.py` | #252 | **UNMEASURED** | Only one member mapped so far (+26/-16). Target function already rewritten. |
| `search_emails_with_limit` in `src/core/database.py` | #257 | **UNMEASURED** | Only one member mapped so far (+9/-1). Target logic already merged. |
| `MemoryCacheBackend` in `src/core/caching.py` | #262 | **UNMEASURED** | Only one member mapped so far (+11/-18). Optimization merged previously. |
| `authenticate_user` timing attack (`src/core/auth.py`) | #526, #943 | **#943** | Superset of #526 (+97/-16). #526 introduces an invalid, instant-fail dummy hash that exacerbates the timing leak (0.08ms vs 130ms). #943 includes proper edge-case guarding and a valid hash. |
| Shell escape injection (`scripts/test_orchestration.sh`, etc.) | #622, #872 | **#622** | Both migrate from `echo -e`. #622 uses robust `%b%s` printf format (+12/-12). #872 (+59/-17) uses `%q`, which destructively backslash-escapes all standard terminal output text. |

*Notes:* All PRs 248-262 exhibit the exact same automated habit of unconditionally appending `.DISABLED` to 12 workflow files in `.github/workflows/`, and these changes should be dropped during any resolution.
