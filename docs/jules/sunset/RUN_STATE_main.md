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
