## 2026-04-10 - Optimize Database I/O with EAFP Pattern
**Learning:** Using `os.path.exists()` before file operations introduces a blocking system call per email, which significantly degrades performance during batch processing or searches in asyncio applications.
**Action:** Replaced `os.path.exists()` checks with the EAFP (Easier to Ask for Forgiveness than Permission) pattern using `try...except FileNotFoundError` and trusted the in-memory `_content_available_index` to avoid unnecessary disk I/O.
