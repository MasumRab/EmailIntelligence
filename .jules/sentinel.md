<<<<<<< HEAD
## 2024-10-27 - Strengthen Security Headers and API Caching

**Vulnerability:** Weak HTTP Security Headers and risk of API data caching
**Learning:** Found that `Content-Security-Policy` lacked `frame-ancestors` and `form-action`, which could expose the app to Clickjacking (if X-Frame-Options is bypassed) or malicious form submissions. `Strict-Transport-Security` lacked `preload`, and API endpoints were not explicitly protected from client-side or intermediary caching, which could leak sensitive JSON data. A previous attempt to fix insecure deserialization via path validation was reverted due to the risk of breaking custom model loading and relying on missing dependencies.
**Prevention:** Implement defense-in-depth: add `preload` to HSTS, restrict `frame-ancestors` and `form-action` in CSP, and explicitly apply `Cache-Control: no-store` and `Pragma: no-cache` to all `/api/` routes in the middleware to prevent caching of sensitive data.

## 2026-06-22 - [Insecure Deserialization via joblib.load]

**Vulnerability:** Arbitrary Code Execution via insecure model path loading (joblib.load)
**Learning:** `joblib.load` can execute malicious code during deserialization. Simply blocking paths outside a specific directory is too rigid and breaks custom model loading.
**Prevention:** Use a hybrid approach: verify model paths against an allowlist of known-safe directories (`models`, `artifacts`, `checkpoints`) and fallback to SHA256 signature verification for paths outside the allowlist. This preserves flexibility while preventing arbitrary code execution.

## 2025-05-22 - [CRITICAL] Prevent Command Injection via `shell=True`

**Vulnerability:** Several utility and deployment scripts (`scripts/branch_rename_migration.py`, `deployment/setup_env.py`, `deployment/migrate.py`) were passing strings directly to `subprocess.run(..., shell=True)`. This could allow attackers to execute arbitrary shell commands if variables (like branch names) were maliciously crafted.
**Learning:** Legacy utility scripts sometimes bypass strict linting or security reviews initially. `shell=True` was used for convenience with pipeline operators (`|| true`) or complex arguments, but it introduces critical injection risks when accepting untrusted or dynamically generated strings.
**Prevention:** Always use `subprocess.run(..., shell=False)` and parse strings into lists using `shlex.split(command)` or construct the list manually. Replace shell-native error suppression like `|| true` with Python equivalents like `check=False`.
