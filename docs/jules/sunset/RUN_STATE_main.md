# Run State - Base: main

**AUTHORITATIVE IN EI: This copy of RUN_STATE_main.md is authoritative for EmailIntelligence.**

- **Base:** main
- **Base SHA:** 897ba6db49f9ae98e7ccb791ebae2730c03e9bc8
- **Date:** 2026-11-10T07:34:24Z
- **PR Total:** 258
- **Deduped Total:** 252
- **Batches:** 13
- **NEXT:** B01
- **BASELINE_PYTEST:** Exit 1: 113 failed, 463 passed, 133 warnings, 13 errors in 82.14s
- **BASELINE_RUFF:** None (Skipped due to BASE-RED)
- **Verdict Counts:** CLEAN-GREEN: 3, CLEAN-RED: 0, CONFLICT: 14, ALREADY-IN-MAIN: 1, NO-OP: 1, FAILING-CHECKS: 1
- **Merges:** none
- **Open Review Threads:** none
- **Open CI Failures:** none

## Environment Notes
- **Baseline differing from S08:** S08 reported `76 failed, 361 passed, 1 skipped, 16 errors` (454 collected tests), while this session originally found `113 failed, 463 passed, 13 errors` (589 collected tests) and later `50 failed, 361 passed, 89 warnings, 11 errors`. 
  This divergence stems from two environmental factors:
  1. This session explicitly installed `scikit-learn` missing from the default venv configuration.
  2. The worktree was moved from `~/.cache` to `/tmp/jules-eval` to avoid failing `security.py`'s hidden-path validations.
  3. `tests/ src/ modules/` was queried in the first run, yielding more total discovered tests than querying `tests/` alone.
- Note that the CI's environment configuration might differ from this local sandbox regarding standard paths and default installed packages.

## SonarCloud Triaging (2026-11-11)
- **Unresolved Issues:** 1,004 (Gate failing on new_reliability C, new_security C, 3.9% duplication)
- **Ownership Gap:** 586 rows have no session charter today:
  - `modules/**`: 117 (34 files; e.g., modules/workflows/routes.py 15, python:S8415)
  - `src/**` (except src/cli and S12-named files): 394 (model_routes.py 54, plugin_routes.py 44, model_registry.py 25, plugin_manager.py 24, notmuch_data_source.py 22, multi_phase_generator.py 20)
  - `tests/**`: 23 (e.g., tests/core/test_factory.py 11; S5779)
  - `setup/**`: 36 (covered as security by S15, not maintainability)
  - `deployment/**`: 16 (covered as security by S15, not maintainability)
  - `root *.py`: 69 (emailintelligence_cli.py 32 goes to CLI session)
- **Routed Elsewhere:** scripts/ 161 -> S16, task_*.py 10 -> S10, client/ 42 -> S14, CLI 45 -> S09, security 112 -> S15, database.py+performance_monitor.py 29 -> S12, GFL 371 -> S17.
- **Triaged Verified Bugs:**
  - `src/core/enhanced_performance_monitor.py:193` (S3827 BLOCKER): UnboundLocalError (`return decorator` before nested def). Sent to S12.
  - `src/core/mfa.py:65` (S930 BLOCKER): `img.save(buffer, format="PNG")`; qrcode's PilImage.save accepts format=, so likely FALSE POSITIVE. Record as triaged, do not fix.
  - `src/main.py:577` (S8414 BLOCKER): CORSMiddleware is not outermost. Sent to S15.
