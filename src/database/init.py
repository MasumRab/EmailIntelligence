"""
Database initialization and health check utilities
"""

import time
import structlog
from ..database.connection import connection_manager, initialize_database_schema
from ..utils.caching import cache_manager

logger = structlog.get_logger()


async def init_database() -> bool:
    """Initialize database connections and schema"""
    try:
        # Connect to Neo4j
        await connection_manager.connect()
        
        # Initialize database schema
        await initialize_database_schema()
        
        logger.info("Database initialization completed successfully")
        return True
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        return False


async def close_database():
    """Close database connections"""
    try:
        await connection_manager.disconnect()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error("Error closing database connections", error=str(e))


async def database_health_check() -> dict:
    """Comprehensive database health check"""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {}
    }
    
    # Check Neo4j
    try:
        neo4j_healthy = await connection_manager.health_check()
        health_status["services"]["neo4j"] = {
            "status": "healthy" if neo4j_healthy else "unhealthy",
            "connection": neo4j_healthy
        }
        if not neo4j_healthy:
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["services"]["neo4j"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    # Check Redis
    try:
        redis_healthy = await cache_manager.health_check()
        health_status["services"]["redis"] = {
            "status": "healthy" if redis_healthy else "unhealthy",
            "connection": redis_healthy
        }
        if not redis_healthy:
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["services"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    return health_status