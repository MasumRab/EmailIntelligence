from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional
import uuid
from ..services.auth_service import AuthService
from ..lib.error_handling import handle_exception, AuthenticationError
from ..models.user import User


# Global auth service instance
auth_service = AuthService()


def get_correlation_id(x_correlation_id: Optional[str] = Header(None)) -> str:
    """
    Get correlation ID from header or generate a new one
    
    Args:
        x_correlation_id: Correlation ID from request header
        
    Returns:
        Correlation ID string
    """
    return x_correlation_id or str(uuid.uuid4())


def authenticate_user(authorization: Optional[str] = Header(None)) -> User:
    """
    Authenticate user based on Authorization header
    
    Args:
        authorization: Authorization header value
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Extract API key from Bearer token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    api_key = authorization[7:]  # Remove "Bearer " prefix
    
    # Authenticate user
    user = auth_service.authenticate(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return user


app = FastAPI(
    title="Orchestration Tools Verification API",
    description="API for verifying orchestration tools changes",
    version="0.1.0"
)


@app.middleware("http")
async def add_correlation_id(request, call_next):
    """Middleware to add correlation ID to request state"""
    correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["x-correlation-id"] = correlation_id
    return response


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Orchestration Tools Verification API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}