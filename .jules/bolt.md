## 2025-02-23 - ContextIsolator Regex Performance
**Learning:** Iterating over hundreds of compiled regex patterns in Python for file access checks is significantly slower (~20x) than using a single combined regex with `|` alternation.
**Action:** When implementing pattern matching against many rules (like allowlists), compile them into a single regex engine call.
