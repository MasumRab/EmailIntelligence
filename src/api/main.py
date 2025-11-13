"""
FastAPI application with GraphQL integration
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
import time
from typing import Dict, Any

from ..config.settings import settings
from ..database.init import init_database, close_database, database_health_check
from ..graphql.schema import schema
from ..utils.caching import cache_manager
from ..utils.monitoring import monitor
from ..utils.rate_limit import rate_limiter

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting PR Resolution Automation API")

    try:
        # Initialize database
        db_initialized = await init_database()
        if not db_initialized:
            raise RuntimeError("Failed to initialize database")

        # Initialize cache
        await cache_manager.initialize()

        # Initialize rate limiter
        await rate_limiter.initialize()

        logger.info("Application startup completed successfully")
        yield
    except Exception as e:
        logger.error("Application startup failed", error=str(e))
        raise
    finally:
        # Shutdown
        logger.info("Shutting down PR Resolution Automation API")
        await close_database()
        await cache_manager.close()
        await rate_limiter.close()
        logger.info("Application shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="PR Resolution Automation API",
    description="GraphQL-based PR conflict resolution system with OpenAI integration",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Add rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    """Rate limiting middleware"""
    client_ip = request.client.host

    # Check rate limit
    if not await rate_limiter.check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    response = await call_next(request)
    return response


# Add monitoring middleware
@app.middleware("http")
async def monitoring_middleware(request, call_next):
    """Request monitoring middleware"""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Record metrics
    duration = time.time() - start_time
    monitor.record_request(
        method=request.method, path=request.url.path, status_code=response.status_code, duration=duration
    )

    return response


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "PR Resolution Automation API", "version": "0.1.0", "docs": "/docs", "graphql": "/graphql"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database health
        db_health = await database_health_check()

        # Check cache health
        cache_healthy = await cache_manager.health_check()

        # Overall health
        is_healthy = db_health.get("status") == "healthy" and cache_healthy

        health_status = "healthy" if is_healthy else "unhealthy"

        return {
            "status": health_status,
            "services": {"database": db_health, "cache": {"status": "healthy" if cache_healthy else "unhealthy"}},
            "timestamp": time.time(),
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return JSONResponse(status_code=503, content={"status": "unhealthy", "error": str(e), "timestamp": time.time()})


@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    try:
        return {
            "performance": monitor.get_performance_metrics(),
            "cache": await cache_manager.get_stats(),
            "rate_limits": await rate_limiter.get_stats(),
            "system": monitor.get_system_metrics(),
        }
    except Exception as e:
        logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/graphql")
async def graphql_endpoint(
    request: Dict[str, Any], client_ip: str = "127.0.0.1"  # This would be extracted from request in real implementation
):
    """GraphQL endpoint"""
    try:
        # Rate limiting (already applied by middleware, but double-checking)
        if not await rate_limiter.check_rate_limit(client_ip):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # Extract GraphQL query and variables
        query = request.get("query")
        variables = request.get("variables", {})
        operation_name = request.get("operationName")

        if not query:
            raise HTTPException(status_code=400, detail="GraphQL query is required")

        # Check query complexity
        complexity = monitor.analyze_query_complexity(query)
        if complexity > settings.graphql_max_query_complexity:
            logger.warning(
                "Query complexity too high", complexity=complexity, max_allowed=settings.graphql_max_query_complexity
            )
            raise HTTPException(status_code=400, detail="Query complexity too high")

        # Execute GraphQL query with caching
        cache_key = f"graphql:{hash(query)}:{hash(str(variables))}"

        # Try to get from cache (for read-only queries)
        if query.strip().upper().startswith("QUERY"):
            cached_result = await cache_manager.get(cache_key)
            if cached_result:
                logger.debug("GraphQL query served from cache")
                return cached_result

        # Execute query
        start_time = time.time()
        result = schema.execute(query, variables=variables, operation_name=operation_name)

        # Handle GraphQL errors
        if result.errors:
            logger.error("GraphQL execution error", errors=[str(error) for error in result.errors])
            return JSONResponse(status_code=400, content={"errors": [str(error) for error in result.errors]})

        response_data = {"data": result.data}

        # Cache read-only results
        if query.strip().upper().startswith("QUERY"):
            await cache_manager.set(cache_key, response_data, ttl=300)  # 5 minutes

        # Record query execution time
        execution_time = time.time() - start_time
        monitor.record_query_execution(execution_time)

        logger.info("GraphQL query executed", operation=operation_name, execution_time=execution_time)

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error("GraphQL endpoint error", error=str(e))
        return JSONResponse(status_code=500, content={"errors": [str(e)]})


@app.get("/graphql")
async def graphql_playground():
    """GraphQL playground endpoint (for development)"""
    if settings.debug:
        return {"message": "GraphQL Playground", "endpoint": "/graphql", "introspection": True}
    else:
        raise HTTPException(status_code=404, detail="Not found")


def create_app() -> FastAPI:
    """Factory function to create FastAPI application"""
    return app


if __name__ == "__main__":
    # Run with uvicorn when script is executed directly
    uvicorn.run(
        "src.api.main:app",
        host=settings.graphql_host,
        port=settings.graphql_port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )
