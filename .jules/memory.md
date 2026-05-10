## Legacy Code Protection

When establishing minimal viable protection systems to protect legacy components from automated cleanups:
1.  **Centralize Configurations:** Use a single source of truth configuration file (like `.legacy-code-protect`) for simple exclusions rather than hardcoding paths.
2.  **Performance Matters in Recursive Operations:** When hooking into deep, recursive directory walking operations (like `rglob` cleanup logic), ensure the configuration file is parsed and cached once into memory (e.g. `_load_protected_legacy_patterns`), rather than reading it from disk repeatedly in the inner loop.
3.  **Strict Path Checking:** When doing path exclusions, perform proper path-prefix checks (e.g., `rel_path == dir_pattern or rel_path.startswith(dir_pattern + '/')`) instead of simple string checks (`rel_path.startswith(dir_pattern)`) to avoid false positives on similarly named directories. Ensure slashes are normalized (`replace('\\', '/')`) to be cross-platform compatible.
