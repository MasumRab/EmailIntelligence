## 2024-05-22 - Regex Compilation Optimization
**Learning:** `fnmatch.translate` generates regex patterns that can be combined with `|` for O(1) matching complexity (delegated to regex engine) instead of O(N) iteration in Python. This reduced matching time by ~7x (3.6s -> 0.5s) for 1000 patterns.
**Action:** Always look for loops over regex matches and consider combining them into a single compiled regex, especially when checking file access or whitelists/blacklists.
