## 2026-07-19 - Add Security Headers Middleware and restrict CORS

**Vulnerability:** Fast API application was lacking Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), and Cache-Control headers for sensitive endpoints. Additionally, the CORS setup in src/main.py was overly permissive relying on wildcard ('*') for methods and headers.
**Learning:** Security middleware can be modularized and added conditionally based on the route or globally. Applying Cache-Control globally can affect static assets, so it's critical to apply no-store to only sensitive API endpoints.
**Prevention:** Establish a default secure-by-design template for new FastAPI apps that injects these headers and configures strict CORS out-of-the-box rather than appending them later.
