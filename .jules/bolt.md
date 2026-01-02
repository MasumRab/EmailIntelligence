## 2024-05-23 - Regex Optimization for File Pattern Matching
**Learning:** Python's `fnmatch` loop for checking file access against multiple patterns is significantly slower (O(N)) than compiling all patterns into a single regex joined by `|` (O(1) relative to pattern count).
**Action:** When matching against a static or semi-static list of glob patterns, convert them all to a single regex using `|`.join(fnmatch.translate(p) for p in patterns)`.
**Benchmark:** ~11.5x speedup (0.16s vs 1.90s for 100k iterations).
**Caveat:** Ensure to handle `fnmatch.translate` output which includes `\Z`. Joining `(?s:pat)\Z` with `|` works correctly.
