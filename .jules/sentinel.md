## 2024-10-27 - Strengthen Security Headers and API Caching

**Vulnerability:** Weak HTTP Security Headers and risk of API data caching
**Learning:** Found that `Content-Security-Policy` lacked `frame-ancestors` and `form-action`, which could expose the app to Clickjacking (if X-Frame-Options is bypassed) or malicious form submissions. `Strict-Transport-Security` lacked `preload`, and API endpoints were not explicitly protected from client-side or intermediary caching, which could leak sensitive JSON data. A previous attempt to fix insecure deserialization via path validation was reverted due to the risk of breaking custom model loading and relying on missing dependencies.
**Prevention:** Implement defense-in-depth: add `preload` to HSTS, restrict `frame-ancestors` and `form-action` in CSP, and explicitly apply `Cache-Control: no-store` and `Pragma: no-cache` to all `/api/` routes in the middleware to prevent caching of sensitive data.

## 2026-08-28 - Insecure Deserialization Findings
**Vulnerability:** A previous fix for insecure deserialization in ML models "failed open" - allowing model loading to proceed if the hash file was missing.
**Learning:** Default-deny logic is critical for security checks like signature verification. We must reject missing signatures rather than simply logging a warning. Pickle/joblib usage in the repository is generally properly wrapped, but the enforcement step around `verify_model_safety` must fail safely and closed.
**Prevention:** Implement strict "fail-closed" paths for missing authentication/signature assets during deserialization.
