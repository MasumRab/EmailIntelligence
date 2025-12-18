## 2024-12-18 - Optimized Regex Matching in ContextIsolator
**Learning:** Combining multiple regex patterns into a single compiled regex using `|` significantly outperforms iterating over a list of individual compiled regexes (O(1) vs O(N) matching complexity).
**Action:** When matching against a list of patterns (especially for high-frequency operations like file access checks), prefer compiling a single combined regex. Ensure proper handling of empty lists and pattern validity.
