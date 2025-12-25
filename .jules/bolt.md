# Bolt's Journal

## 2024-05-24 - Initial Journal Creation
**Learning:** Performance journals help track what works and what doesn't in a specific codebase context.
**Action:** Record all significant performance learnings here.

## 2024-05-24 - ContextIsolator Regex Optimization
**Learning:** Iterating over a list of compiled regex patterns for every file check is inefficient (O(M*N)). Python's `re` module can handle complex OR-ed patterns (`p1|p2|p3`) much more efficiently in C.
**Action:** Combined multiple glob patterns into a single compiled regex using `|`. Reduced overhead significantly (~6.6x speedup in benchmarks).
**Watch out:** `fnmatch.translate` produces anchored regexes (e.g. `(?s:.*\.py)\Z`). These are safe to join with `|`.
