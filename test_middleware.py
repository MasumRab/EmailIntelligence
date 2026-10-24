from fastapi import FastAPI
from src.core.middleware import create_security_middleware

app = FastAPI()
app.add_middleware(
    create_security_middleware,
    enable_rate_limiting=True,
    enable_audit_logging=True,
    enable_performance_monitoring=True,
)
