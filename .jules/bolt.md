## 2024-02-23 - Regex Compilation for Glob Patterns
**Learning:** Compiling a list of glob patterns into a single regex using `|` (OR) is significantly faster than iterating through a list of compiled regex objects.
**Action:** When handling multiple glob patterns that need to be checked against a single string, combine them into a single regex `(?s:pattern1)\Z|(?s:pattern2)\Z` using `fnmatch.translate` and `|` join. This delegates the optimization to the regex engine's state machine. Benchmarks showed ~38% improvement.
