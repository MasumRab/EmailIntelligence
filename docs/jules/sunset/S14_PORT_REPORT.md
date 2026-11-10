# S14 Port Report

## Branch Analysis

1. `rebase-875`: Ported successfully to `port-rebase-875`.
   * **Commit:** `3a7fd28fb10d87b0a3785f969d1cac298af8d393`
   * **Verdict:** The change in `client/src/components/email-list.tsx` (using `Array.from` instead of `[...Array()]` and ensuring string fallbacks for keys) is still highly relevant to avoid React warnings and improve code quality (addressing SonarCloud findings). The changes were cherry-picked and conflicts resolved, and tests were added ensuring proper compilation and rendering.
2. `rebase-ei610` (from `rebase/ei610`): Ported successfully to `port-rebase-ei610`.
   * **Commit:** `90228b814d1ab98238628202da419cc6c0260ae9`
   * **Verdict:** The `_EmailContext` lazy-evaluation change in `src/core/smart_filter_manager.py` still cleanly applies. It remains a valid performance optimization for filtering emails because if an email is rejected early on by its domain or sender, we do not waste CPU cycles calculating `.lower()` on the possibly large content body. Tests were added to verify correct lazy initialization and fallback logic.
3. `sim-ot-wave1` (from `sim/ot-wave1`): 
   * **Size:** 328 files, +48749 lines.
   * **Verdict:** **archive**. It is heavily superseded by orchestration-tools on `main` and represents massive, diverging experimental CLI tooling and sequencing logic that would be far too massive and messy to attempt porting.
4. `complex-branch-analysis`: 
   * **Size:** 2 commits, 269 behind.
   * **Verdict:** **archive**. The branch contains scratch tooling and large refactoring footprints (`analyze_complex_branch.py`). It is not suitable for inclusion into the main pipeline.

## Execution

- **`port-rebase-875`**: Cherry-picked, fixed the `null` label mapping bug, added vitest coverage, passing suite.
- **`port-rebase-ei610`**: Cherry-picked cleanly, added pytest coverage to verify `_EmailContext` lazy initialization, passing suite.
