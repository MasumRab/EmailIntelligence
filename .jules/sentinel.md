# Sentinel Journal

## 2024-03-24: Overly Permissive CORS Allowed Origins
**Vulnerability Discovered**: Overly permissive CORS settings (`allow_origins=["*"]`) in `src/main.py`. This setup could allow malicious sites to perform Cross-Site Request Forgery (CSRF) or access sensitive endpoints on the backend without restriction.
**Learning**: FastAPI applications should configure CORS restrictively by default to mitigate cross-origin attacks. Relying on default broad permissions exposes the application to attack.
**Prevention**: Default to restrictive CORS settings, using environment variables (`ALLOWED_ORIGINS`) for overrides in specific environments to define precisely which clients are allowed to communicate with the service.