from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""

    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "frame-ancestors 'none'; form-action 'self';"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Apply Cache-Control no-store only to sensitive endpoints
        if request.url.path.startswith("/api/") or request.url.path.startswith("/context-control/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

        return response
