# Sentinel Security Journal

## 2024-04-09 Path Traversal in File Writing Operations
- **Vulnerability Discovered**: Unsanitized parameters (like `report_id`) were concatenated into filenames for file writing in `src/validation/reporting_engine.py`. This allows path traversal attacks (e.g., passing `../../etc/passwd` as the `report_id`).
- **Learning**: Even when file extensions are appended, an attacker could write arbitrary files (e.g., `../../target.json`) outside the intended directory.
- **Prevention**: Before using user-supplied or potentially untrusted strings in path construction, always sanitize them. A simple and effective approach for strictly filenames is `os.path.basename(str(input))` or `pathlib.Path(input).name` to ensure no directory traversal sequences are evaluated.
