## 2024-10-27 - Strengthen Security Headers and API Caching

**Vulnerability:** Weak HTTP Security Headers and risk of API data caching
**Learning:** Found that `Content-Security-Policy` lacked `frame-ancestors` and `form-action`, which could expose the app to Clickjacking (if X-Frame-Options is bypassed) or malicious form submissions. `Strict-Transport-Security` lacked `preload`, and API endpoints were not explicitly protected from client-side or intermediary caching, which could leak sensitive JSON data. A previous attempt to fix insecure deserialization via path validation was reverted due to the risk of breaking custom model loading and relying on missing dependencies.
**Prevention:** Implement defense-in-depth: add `preload` to HSTS, restrict `frame-ancestors` and `form-action` in CSP, and explicitly apply `Cache-Control: no-store` and `Pragma: no-cache` to all `/api/` routes in the middleware to prevent caching of sensitive data.

## 2026-07-22 - Fix command injection vulnerability in scripts

**Vulnerability:** Used `shell=True` in `subprocess.run` inside `scripts/branch_rename_migration.py`, `deployment/setup_env.py`, and `deployment/migrate.py`, which is a command injection risk when passing unsanitized variables.
**Learning:** Python scripts often use `subprocess.run(..., shell=True)` for convenience, but `shlex.split()` with `shell=False` is the secure way to execute commands. Note that converting to `shell=False` requires ensuring that commands relying on shell features (like pipes or chained commands) do not break.
**Prevention:** Always use `shlex.split()` and `shell=False` when wrapping command strings for `subprocess.run` as long as shell features are not needed.

## 2026-07-22 - Information Exposure Through Query Strings
**Vulnerability:** The `/token` login endpoint accepted username and password as query parameters instead of a JSON request body, exposing credentials in URLs and access logs (CWE-598).
**Learning:** FastAPI defaults to query parameters for primitive types without explicit `Body()` or Pydantic models. This is a common pattern in the framework that requires specific schema definition to be secure.
**Prevention:** Always use Pydantic models (`BaseModel`) or `OAuth2PasswordRequestForm` for sensitive POST endpoints in FastAPI to enforce secure request bodies.
