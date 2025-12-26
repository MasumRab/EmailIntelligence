# Bolt's Journal

## 2024-05-22 - [Initial Setup]
**Learning:** The codebase structure has `src/` at the root, not `backend/src/`.
**Action:** Always verify file structure with `ls` before assuming paths.

## 2024-05-22 - [Regex Optimization]
**Learning:** Combining multiple regex patterns with `|` (OR) into a single compiled regex is significantly faster (10x+) than iterating through a list of compiled regex objects.
**Action:** Always look for opportunities to combine regexes when matching against multiple patterns.
