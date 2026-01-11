# Bolt's Journal

## 2024-05-22 - Optimizing Database Search
**Learning:** Python's `str.lower()` + `in` operator is significantly faster (~7.7x) than `re.search(..., re.IGNORECASE)` for simple substring checks.
**Action:** Always prefer string methods over regex for simple matching in hot paths.

## 2024-05-23 - Pre-computing Search Indices
**Learning:** Pre-allocating and pre-processing search text (lowercasing, combining fields) into a separate index during load time beats processing it on-the-fly during search time, even with the memory overhead.
**Action:** Move O(N) processing out of search loops whenever possible.

## 2024-05-24 - List Comprehension vs Generator Expressions
**Learning:** For `find_first` type operations or limited results, generators with `itertools.islice` are vastly superior to list comprehensions because they allow early exit.
**Action:** Use generators for search/filter operations where we might stop early.

## 2024-05-24 - Context Isolator Regex Optimization
**Learning:** Compiling a single regex with `|` (OR) is much faster than iterating through a list of regex patterns and matching them one by one.
**Action:** Combine compatible regex patterns into a single compiled object.
